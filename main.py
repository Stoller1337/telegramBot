import string
import time
from telnetlib import EC

import emoji
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import telebot
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from telebot import types
import buttons as bt

token = "5299924776:AAFA0SR5YSrGCX1NDx_r3dSWWz4yBCoUNdA"

bot = telebot.TeleBot(token)
key= ''
array = []
date = 1
count = 5
download_file = None
flag = True
src = ''
choosePeriod = None
city = 'Санкт-Петербург'
driver = webdriver.Firefox()
bt.mainMenu
@bot.message_handler(commands=['start'])
def start(message: types.Message):
     bot.send_message(message.chat.id, "Привет! Я бот Яндекс-Новости.\n\n"
                                       "Нажмите на кнопку 'Новый запрос' для того что бы отправить запрос\n"
                                       "или нажми на 'Запрос из файла' для получения новостей \nпо ключевым словам из файла!",
                      reply_markup=bt.mainMenu)


@bot.message_handler(content_types=['text'])
def request(message):

    if message.text == 'Выбрать город':
        msg = bot.send_message(message.chat.id, 'Введите город для поиска новостей: ')
        bot.register_next_step_handler(msg, choose_city)
        time.sleep(1)
    elif message.text == 'Новый запрос':
        msg = bot.send_message(message.chat.id, 'Введите ключевое слово: ')
        bot.register_next_step_handler(msg, save_keyword)
    elif message.text == 'Запрос из файла':
        msg = bot.send_message(message.chat.id, 'Пожалуйста отправьте мне файл с расширением .txt')
        bot.register_next_step_handler(msg, save_keyword)


def choose_city(message):
    global city
    global driver
    city = message.text
    bot.send_message(message.chat.id, "Ищу город...")

    driver.get("https://yandex.ru/tune/geo")
    driver.implicitly_wait(1)
    try:
        check_box = driver.find_element(By.CLASS_NAME, "checkbox__control")
        check_box.click()

    except NoSuchElementException:
        print("Переход на страницу геолокации не был выполнен")
        #driver.quit()
        #exit(1)

    region_box = driver.find_element(By.CLASS_NAME, "input__control")
    region_box.send_keys(city)

    driver.implicitly_wait(3)

    try:
        popup_window = driver.find_element(By.CLASS_NAME, "b-autocomplete-item")
        print("Выбранный вами город:         ", driver.find_element(By.CLASS_NAME, "b-autocomplete-item__reg").text)
        popup_window.click()
    except NoSuchElementException:
        msg = bot.send_message(message.chat.id, "Неверное название города")
        bot.register_next_step_handler(msg, choose_city)
        #driver.quit()
        #exit(1)

    # Сохранение нового города
    save_button = driver.find_elements(By.CLASS_NAME, "button")[1]
    save_button.click()

    time.sleep(1)

    msg = bot.send_message(message.chat.id, 'Отлично, настройки сохранены!', reply_markup=bt.mainMenu)
    bot.register_next_step_handler(msg, request)


# @bot.message_handler(content_types=['document'])
# def request_from_file(message):
#     # global key
#     # key = ''
#     fileFrom = bot.get_file(message.document.file_id)
#     print('------')
#     print('name = ', message.document.file_name)
#     fileOpen = open(fileFrom, 'r', encoding='utf8')
#     print('------')
#     key = fileOpen.readline()
#     print('key = ', key)
# #     fileFrom = bot.get_file(message.document.file_id)
# #     download_file = bot.download_file(fileFrom.file_path)
# #     src = 'D:/BPA/files/' + message.document.file_name
# #     with open(src, 'rb', encoding='utf8') as file:
# # #        file = open(src, "rb", "utf_8_sig")
# #         key = file.readline()
#     msg = bot.send_message(message.chat.id, 'Открываю файл...Пожалуйста подождите')
#     bot.register_next_step_handler(msg, save_keyword)
#

@bot.message_handler(content_types=['document'])
def save_keyword(message):
    global key
    global array
    global flag
    global download_file
    if message.document:
        flag = True
        fileFrom = bot.get_file(message.document.file_id)
        download_file = bot.download_file(fileFrom.file_path)
        src = 'D:/BPA/files/' + message.document.file_name
        with open(src, 'r', encoding='utf8') as file:
            array = [row.strip() for row in file]
            print('key = ', array)
        bot.send_message(message.chat.id, 'Открываю файл...Пожалуйста подождите')
        msg1 = bot.send_message(message.chat.id, 'Введите количество выводимых новостей: ')
        bot.register_next_step_handler(msg1, choose_count_news)

    else:
        key = message.text
        print('format = ', type(key))
        msg1 = bot.send_message(message.chat.id, 'Введите количество выводимых новостей: ')
        bot.register_next_step_handler(msg1, choose_count_news)
        flag = False
def choose_count_news(message: types.Message):

    global count
    count = int(message.text)
    global flag
    if count < 0 or count > 30:
        bot.send_message(message.chat.id, 'Неверный ввод, попробуйте еще раз...')
        msg1 = bot.send_message(message.chat.id,
                            'Введите количество выводимых новостей: ')

        bot.register_next_step_handler(msg1, choose_count_news)
        count = int(message.text)
    else:
        msg1 = bot.send_message(message.chat.id, 'Выберите период: ', reply_markup=bt.otherMenu)
        if flag == False:
            bot.register_next_step_handler(msg1, choose_date)
        else:
            bot.register_next_step_handler(msg1, choose_date_file)


def choose_date_file(message):

    global date
    global date_num
    global array
    global choosePeriod
    global driver
    date = message.text

    match date:
        case 'За все время':
            ans_date = 'За все время'
            date_num = 1
        case 'Сегодня':
            ans_date = 'Сегодня'
            date_num = 2
        case '3 дня':
            ans_date = '3 дня'
            date_num = 3
        case 'Неделя':
            date_num = 4
            ans_date = 'Неделя'
        case _:
            date_num = -1

    if date_num == -1:
        bot.send_message(message.chat.id, "Неверный период\nПожалуйста, используйте кнопки",
                         reply_markup=bt.otherMenu)
        msg1 = bot.send_message(message.chat.id, 'Выберите период: ')
        bot.register_next_step_handler(msg1, choose_date)

    else:
        print('PERIOD = ', date_num)
        choosePeriod = date_num

        msg1 = bot.send_message(message.chat.id,
                                "Город: " + city + "\nНовость: " + str(array) + "\nПериод: " + ans_date + "\nКоличество новостей: " + str(
                                    count))
        # bot.register_next_step_handler(msg1, parsingRequest)
        bot.send_message(message.chat.id, 'Обрабатываю запрос...Пожалуйста подождите ' + '⏳')

        #driver = webdriver.Firefox()
        driver.get("https://yandex.ru/news")
        driver.implicitly_wait(1)

        if driver.title == 'Ой!':
            capcha = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha")
            capcha.find_element(By.CLASS_NAME, "CheckboxCaptcha-Button").click()
            driver.implicitly_wait(1)

        file_write = open('ans.txt', 'w')

        for i in range(len(array)):

            req = array[i]
            print('[*] REQUEST = ', req)
            print('[*] TYPE = ', type(req))
            # temp = 5
            # count = int(temp)

            text_box = driver.find_element(By.CLASS_NAME, "input__control")
            find_button = driver.find_element(By.CLASS_NAME, "websearch-button")

            text_box.clear()
            text_box.send_keys(req)
            #print('TEXT_BOX_SEND_KEYS = ', text_box.send_keys(req))
            find_button.click()

            driver.implicitly_wait(3)

            if choosePeriod > 1:
                periods = driver.find_elements(By.CLASS_NAME, "Radiobox-Control")
                period = periods[choosePeriod - 1]
                period.click()
                #WebDriverWait(driver, timeout=100).until(EC.element_to_be_clickable(period)).click()

            #Получение списка нвоостей
            news = driver.find_elements(By.CLASS_NAME, "news-search-story")

            if len(news) == 0:
                bot.send_message(message.chat.id, "Новостей по такому запросу не найдено\nПопробуйте еще раз",
                                 reply_markup=bt.mainMenu)
                msg = bot.send_message(message.chat.id, "Введите ключевое слово: ", reply_markup=bt.mainMenu)
                bot.register_next_step_handler(msg, save_keyword)
                #driver.quit()
                continue

            count2 = count

            if len(news) < count2:
                count2 = len(news)

            dictOfNews = {}

            for k in range(count2):
                someNews = news.pop(0)
                dictOfNews[someNews.find_element(By.CLASS_NAME, "mg-snippet__title").text] = someNews.find_element(
                    By.CLASS_NAME, "mg-snippet__url").get_attribute("href")

            dictOfNews2 = []
            slovo = ''
            num = 1
            for Name, Link in dictOfNews.items():
                word = str(num) + ') ' + '[' + Name + ']' + '(' + Link + ')' + '\n' + ''
                dictOfNews2.append(word)
                slovo += word
                num += 1

            print('[*] iter = ', i)
            print('slovo = ', slovo)

            file_write.write('[*] REQUEST = ' + array[i] + '\n')
            file_write.write(slovo)
            file_write.write('\n')
            for j in range(len(dictOfNews2)):
                print('dict = ', dictOfNews2[j], '\n')
                # file_write = open('ans.txt', 'w')
                # file_write.write(dictOfNews2[i])

            bot.send_message(message.chat.id, slovo, parse_mode='Markdown', reply_markup=bt.mainMenu)
            time.sleep(1)

def choose_date(message: types.Message):

    global date
    global date_num
    date = message.text

    match date:
        case 'За все время':
            ans_date = 'За все время'
            date_num = 1
        case 'Сегодня':
            ans_date = 'Сегодня'
            date_num = 2
        case '3 дня':
            ans_date = '3 дня'
            date_num = 3
        case 'Неделя':
            date_num = 4
            ans_date = 'Неделя'
        case _:
            date_num = -1

    if date_num == -1:
        bot.send_message(message.chat.id, "Неверный период\nПожалуйста, используйте кнопки",
                         reply_markup=bt.otherMenu)
        msg1 = bot.send_message(message.chat.id, 'Выберите период: ')
        bot.register_next_step_handler(msg1, choose_date)

    else:
        choosePeriod = date_num

        msg1 = bot.send_message(message.chat.id, "Город: " + city + "\nНовость: " + str(key) + "\nПериод: " + ans_date + "\nКоличество новостей: " + str(count))
        #bot.register_next_step_handler(msg1, parsingRequest)
        bot.send_message(message.chat.id, 'Обрабатываю запрос...Пожалуйста подождите ' + '⏳')
        #driver = webdriver.Firefox()
        driver.get("https://yandex.ru/news")

        if driver.title == 'Ой!':
            capcha = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha")
            capcha.find_element(By.CLASS_NAME, "CheckboxCaptcha-Button").click()
            driver.implicitly_wait(1)

        request = key
        # temp = 5
        # count = int(temp)

        text_box = driver.find_element(By.CLASS_NAME, "input__control")
        find_button = driver.find_element(By.CLASS_NAME, "websearch-button")

        text_box.send_keys(request)
        find_button.click()

        driver.implicitly_wait(3)

        if choosePeriod > 1:
            periods = driver.find_elements(By.CLASS_NAME, "Radiobox-Control")
            period = periods[choosePeriod - 1]
            period.click()

        news = driver.find_elements(By.CLASS_NAME, "news-search-story")

        if len(news) == 0:
            bot.send_message(message.chat.id, "Новостей по такому запросу не найдено\nПопробуйте еще раз", reply_markup=bt.mainMenu)
            msg = bot.send_message(message.chat.id, "Введите ключевое слово: ", reply_markup=bt.mainMenu)
            bot.register_next_step_handler(msg, save_keyword)
            #driver.quit()

        count2 = count

        if len(news) < count2:
            count2 = len(news)

        else:

            dictOfNews = {}

            for i in range(count2):
                someNews = news.pop(0)
                dictOfNews[someNews.find_element(By.CLASS_NAME, "mg-snippet__title").text] = someNews.find_element(
                    By.CLASS_NAME, "mg-snippet__url").get_attribute("href")


            dictOfNews2 = []
            slovo = ''
            global num
            num = 1
            for Name, Link in dictOfNews.items():
                word = str(num) + ') '+'[' + Name + ']' + '(' + Link + ')' + '\n' + ''
                dictOfNews2.append(word)
                slovo += word
                num += 1
            print(slovo)
            for i in range(len(dictOfNews2)):
                print(dictOfNews2[i], '\n')

            # for i in range(len(dictOfNews2)):
            #     bot.send_message(message.chat.id, dictOfNews2[i], parse_mode='Markdown', reply_markup=bt.mainMenu)

            bot.send_message(message.chat.id, slovo, parse_mode='Markdown', reply_markup=bt.mainMenu)
bot.polling()
