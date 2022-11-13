from telebot.types import KeyboardButton, ReplyKeyboardMarkup

city = KeyboardButton("Выбрать город")
request = KeyboardButton("Новый запрос")
openFile = KeyboardButton("Запрос из файла")

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(city, request, openFile)

#openFileKeybord = ReplyKeyboardMarkup(resize_keyboard=True).add(openFile)

answer1 = KeyboardButton("Да")
answer2 = KeyboardButton("Нет")

answers = ReplyKeyboardMarkup(resize_keyboard=True).add(answer1, answer2)

range1 = KeyboardButton("За все время")
range2 = KeyboardButton("Сегодня")
range3 = KeyboardButton("3 дня")
range4 = KeyboardButton("Неделя")

otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(range2, range3, range4, range1)

