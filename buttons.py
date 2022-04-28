from telebot.types import KeyboardButton, ReplyKeyboardMarkup

request = KeyboardButton("Новый запрос")

mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(request)

range1 = KeyboardButton("За все время")
range2 = KeyboardButton("Сегодня")
range3 = KeyboardButton("3 дня")
range4 = KeyboardButton("Неделя")

otherMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(range1, range2, range3, range4)

