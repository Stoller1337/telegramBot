from ast import keyword
from turtle import delay
from asyncio.windows_events import NULL
from selenium import webdriver
from selenium.webdriver.common.by import By
import telebot
from telebot import types
import buttons as bt

token = "5299924776:AAFA0SR5YSrGCX1NDx_r3dSWWz4yBCoUNdA"

bot = telebot.TeleBot(token)

key_word = ''

date = 1

@bot.message_handler(commands=['start'])
def start(message: types.Message):
     bot.send_message(message.chat.id, "Привет! Я бот Яндекс-Новости.\n\nНажмите на кнопку 'Новый запрос' для того что бы получить информацию.", reply_markup=bt.mainMenu)


print("key до функции request = " + key_word)

@bot.message_handler(content_types=['text'])
def request(message):

    if message.text == 'Новый запрос':
        msg = bot.send_message(message.chat.id, 'Введите ключевое слово: ')
 
    bot.register_next_step_handler(msg, save_keyword)

print("key после функции request = " + key_word)
print("key до функции save = " + key_word)

def save_keyword(message: types.Message):

    global key
    key = message.text
    print(type(message.text))
    print(message.text)

    msg1 = bot.send_message(message.chat.id, 'Отлично, выберите период: ', reply_markup=bt.otherMenu)
    bot.register_next_step_handler(msg1, choose_date)

print("key после функции save = " + key_word)
print("key до функции date = " + key_word)


def choose_date(message: types.Message):

    global date
    date = message.text

    if date == 'За все время':
        ans_date = 'За все время'
    elif date == 'Сегодня':
        ans_date = 'Сегодня'
    elif date == '3 дня':
        ans_date = '3 дня'
    elif date == 'Неделя':
        ans_date = 'Неделя'

    #string = "Новость: " + keyword + "\nПериод: " + date
    
    msg1 = bot.send_message(message.chat.id, "Новость: " + key + "\nПериод: " + ans_date)
    bot.register_next_step_handler(msg1, parsingRequest)
    array = ['[Google](http://www.google.com/)', '[VK](https://www.vk.com/)']
    for i in range (len(array)):
        bot.send_message(message.chat.id, array[i] , parse_mode='Markdown')

print("key после функции date = " + key_word)

def parsingRequest(message: types.Message):
    
    driver = webdriver.Firefox()
    driver.get("https://yandex.ru/news")
    if driver.title == 'Ой!':
        capcha = driver.find_element(By.CLASS_NAME, "CheckboxCaptcha")
        capcha.find_element(By.CLASS_NAME, "CheckboxCaptcha-Button").click()
        driver.implicitly_wait(1)

    request = key
    #print("Колличество выводимых новостей: ", end="")
    temp  = 5

    # for i in range(len(temp)):
    #     if temp[i] < '0' or temp[i] > '9':
    #         print("Введено не число")
    #         exit(0)

    count = int(temp)
    #
    # if count < 1:
    #     print("Неверное колличество новостей")
    #     exit(0)

    print("Выберите перод:","1) За всё время","2) Сегодня", "3) 3 дня", "4) Неделя", sep="\n")
    print("Введите номер (1-4): ", end="")
    temp = date

    for i in range(len(temp)):
        if temp[i] < '1' or temp[i] > '4':
            print("Неверный номер периода")
            exit(0)

    choosePeriod = int(temp)

    text_box    = driver.find_element(By.CLASS_NAME, "input__control")
    find_button = driver.find_element(By.CLASS_NAME, "websearch-button")

    text_box.send_keys(request)
    find_button.click()

    driver.implicitly_wait(3)

    if choosePeriod > 1:
        periods = driver.find_elements(By.CLASS_NAME, "Radiobox-Control")
        period = periods[choosePeriod-1]
        period.click()

    news = driver.find_elements(By.CLASS_NAME, "news-search-story")

    if len(news) == 0:
        print("Новостей по такому запросу не найдено")
        driver.quit()
        exit(0)

    if len(news) < count:
        count = len(news)

    newsItem = news.pop(0)

    print()

    for i in range(count):
        bot.send_message(message.chat.id, "request is complet")
        bot.send_message(message.chat.id, str(i+1, ') ', newsItem.find_element(By.CLASS_NAME, "mg-snippet__title").text))
        print(i+1, ') ', newsItem.find_element(By.CLASS_NAME, "mg-snippet__title").text)
        print(newsItem.find_element(By.CLASS_NAME, "mg-snippet__url").get_attribute("href"))
        print()
        newsItem = news.pop(0)

    

    driver.quit()

bot.polling()

