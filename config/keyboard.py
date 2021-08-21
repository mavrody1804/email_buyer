from aiogram.types import ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardButton,InlineKeyboardMarkup
from aiogram.types.base import T




#Кнопки меню

menu_btn1 = KeyboardButton(text='➕ Зарегистрировать новый аккаунт')
menu_btn2 = KeyboardButton(text='📋 Мои аккаунты')
menu_btn3 = KeyboardButton(text='💰 Баланс')
menu_btn4 = KeyboardButton(text='💬 Помощь')

#Клавиатура меню
menu_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(menu_btn1,menu_btn2,menu_btn3,menu_btn4)

#Кнопки регистрации почты

register_btn1 = KeyboardButton(text='✔️ Готово')
register_btn2 = KeyboardButton(text='🚫 Отменить регистрацию')



#Клавиатура регистрации почты
register_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(register_btn1,register_btn2)


# register_valid_step1 кнопки
register_valid_step1_btn1 = KeyboardButton(text='🔑 Я подтверждаю корректность пароля')


# register_valid_step1 клавиатура
register_valid_step1_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(register_valid_step1_btn1)

# register_valid_step2 кнопки
register_valid_step2_btn1 = KeyboardButton(text='📴 Я подтверждаю, что в профиле указан верный телефон')

# register_valid_step1 клавиатура
register_valid_step2_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(register_valid_step2_btn1)

# register_valid_step2 кнопки
register_valid_step3_btn1 = KeyboardButton(text='📨 Я подтверждаю, что в профиле нет резервной почты')

# register_valid_step1 клавиатура
register_valid_step3_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(register_valid_step3_btn1)


#register_cancel кнопки

register_cancel_btn1 = KeyboardButton(text='🚫 Да, отменить')
register_cancel_btn2 = KeyboardButton(text='🔙 Назад')

# register_cancel клавиатура

register_cancel_keyboard = ReplyKeyboardMarkup(resize_keyboard=True).add(register_cancel_btn1,register_cancel_btn2)

# баланс кнопки
balans_btn1 = KeyboardButton(text='💳 Вывести')
balans_btn2 = KeyboardButton(text='📝 История баланса')
balans_btn3 = KeyboardButton(text='🔙 Назад')

# баланс клавиатура
balans_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(balans_btn1,balans_btn2,balans_btn3)

# withdraw кнопки
withdraw_btn1 = KeyboardButton(text='payer')
withdraw_btn2 = KeyboardButton(text='webmoney')
withdraw_btn3 = KeyboardButton(text='карта')

# withdraw клавиатура

withdraw_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,row_width=2).add(withdraw_btn1,withdraw_btn2,withdraw_btn3)

# Помощь кнопки

help_btn1 = InlineKeyboardButton(text='Что такое холд?',callback_data='help_1')
help_btn2 = InlineKeyboardButton(text='Как избежать sms подтверждения?',callback_data='help_2')
help_btn3 = InlineKeyboardButton(text='Почему аккаунт "Недоступен"?',callback_data='help_3')
help_btn4 = InlineKeyboardButton(text='Как избежать блокировки аккаунта Gmail?',callback_data='help_4')
help_btn5 = InlineKeyboardButton(text='Сколько аккаунтова может принять бот?',callback_data='help_5')
help_btn6 = InlineKeyboardButton(text='🚫 В главное меню 🚫',callback_data='help_6')
#help_btn7 = InlineKeyboardButton(text='Тех.поддержка',callback_data='help_7')


#Помощь клавиатура

help_keyboard = InlineKeyboardMarkup(row_width=1).add(help_btn1,help_btn2,help_btn3,help_btn4,help_btn5,help_btn6)


#Помощь отмена кнопки

help_cancel_btn1 = InlineKeyboardButton(text='🔙 Назад',callback_data='cancel')

#Помощь отмена клавиатура

help_keyboard_cancel = InlineKeyboardMarkup(row_width=1).add(help_cancel_btn1)

#Кнопки админа
admin_btn1 = KeyboardButton(text='Добавить в базу данных аккаунт')
admin_btn2 = KeyboardButton(text='Проверить аккаунты после холда')

#Клавиатура админа
admin_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(admin_btn1,admin_btn2)

#Проверка валидности
admin_check_btn1 = KeyboardButton(text='Валид')
admin_check_btn2 = KeyboardButton(text='Не валид')

#Клавиатура проверки валидности
admin_check_keyboard = ReplyKeyboardMarkup(resize_keyboard=True,row_width=1).add(admin_check_btn1,admin_check_btn2)