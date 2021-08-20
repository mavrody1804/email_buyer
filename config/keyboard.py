from aiogram.types import ReplyKeyboardMarkup,KeyboardButton




#Кнопки меню

menu_btn1 = KeyboardButton(text='➕ Зарегистрировать новый аккаунт')
menu_btn2 = KeyboardButton(text='📋 Мои аккаунты')
menu_btn3 = KeyboardButton(text='💰 Баланс')
menu_btn4 = KeyboardButton(text='💬 Помощь')

#Клавиатура меню
menu_keyboard = ReplyKeyboardMarkup().add(menu_btn1,menu_btn2,menu_btn3,menu_btn4)

#Кнопки регистрации почты

register_btn1 = KeyboardButton(text='✔️ Готово')
register_btn2 = KeyboardButton(text='🚫 Отменить регистрацию')



#Клавиатура регистрации почты
register_keyboard = ReplyKeyboardMarkup().add(register_btn1,register_btn2)


# register_valid_step1 кнопки
register_valid_step1_btn1 = KeyboardButton(text='🔑 Я подтверждаю корректность пароля')


# register_valid_step1 клавиатура
register_valid_step1_keyboard = ReplyKeyboardMarkup().add(register_valid_step1_btn1)

# register_valid_step2 кнопки
register_valid_step2_btn1 = KeyboardButton(text='📴 Я подтверждаю, что в профиле указан верный телефон')

# register_valid_step1 клавиатура
register_valid_step2_keyboard = ReplyKeyboardMarkup().add(register_valid_step2_btn1)

# register_valid_step2 кнопки
register_valid_step3_btn1 = KeyboardButton(text='📨 Я подтверждаю, что в профиле нет резервной почты')

# register_valid_step1 клавиатура
register_valid_step3_keyboard = ReplyKeyboardMarkup().add(register_valid_step3_btn1)


#register_cancel кнопки

register_cancel_btn1 = KeyboardButton(text='🚫 Да, отменить')
register_cancel_btn2 = KeyboardButton(text='🔙 Назад')

# register_cancel клавиатура

register_cancel_keyboard = ReplyKeyboardMarkup().add(register_cancel_btn1,register_cancel_btn2)

# баланс кнопки
balans_btn1 = KeyboardButton(text='💳 Вывести')
balans_btn2 = KeyboardButton(text='📝 История баланса')
balans_btn3 = KeyboardButton(text='🔙 Назад')

# баланс клавиатура
balans_keyboard = ReplyKeyboardMarkup().add(balans_btn1,balans_btn2,balans_btn3)

# withdraw кнопки
withdraw_btn1 = KeyboardButton(text='payer')
withdraw_btn2 = KeyboardButton(text='webmoney')
withdraw_btn3 = KeyboardButton(text='карта')

# withdraw клавиатура

withdraw_keyboard = ReplyKeyboardMarkup().add(withdraw_btn1,withdraw_btn2,withdraw_btn3)