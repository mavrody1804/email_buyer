 # -*- coding: utf8 -*-
from os import stat
from sqlite3.dbapi2 import Row
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton,ReplyKeyboardRemove
from threading import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from config.keyboard import *
import requests
import sqlite3 as sq
import threading
import time
import datetime


# запуск и инициализация бота
API_TOKEN = '1966287693:AAGkUszbRQ-Qsmi5YJ81T7mBiVrnn29i68A'
logging.basicConfig(level=logging.INFO)
bot = Bot(API_TOKEN)


# Раабота с машиной состояний
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class admin_form(StatesGroup):
    menu=State()
    register_new_email = State()
    check =  State()
class menu_form(StatesGroup):
    main_menu = State()

class register_form(StatesGroup):
    cancel = State()
    process = State()
    valid_step1 = State()
    valid_step2 = State()
    valid_step3 = State()
    invalid = State()
    finish = State()

class help_form(StatesGroup):
    help = State()


class balans(StatesGroup):
    check = State()
    withdraw = State()
    write = State()
# Запускаем стартовое меню

@dp.message_handler(commands=['start'], state='*')
async def menu_start(message: types.Message):
    with sq.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("""CREATE TABLE IF NOT EXISTS users (
            balans  INTEGER DEFAULT 0,
            hold  INTEGER DEFAULT 0,
            history  TEXT,
            accounts  TEXT,
            user_id INTEGER DEFAULT 1
        )  """)
        r = cur.execute('SELECT * FROM users').fetchall()
        for row in r:
            if row[4] == message.from_user.id:
                break
        else:
            cur.execute('INSERT INTO users (user_id) VALUES (?)', (message.from_user.id,))
        con.commit()
        await message.answer('Регистрируйте аккаунты Gmail и получайте за это оплату.\nЗа каждый аккаунт вы получите: 2.0₽',reply_markup=menu_keyboard)
        await menu_form.main_menu.set()


#Админ вход
@dp.message_handler(commands=['admin'], state='*')
async def admin_login(message: types.Message):
    print(message.from_user.id)
    if message.from_user.id == 703170971:
        await bot.send_message(message.from_user.id,'Здравствуйте админ.',reply_markup=admin_keyboard)
        await admin_form.menu.set()
    else:
        pass

#Меню админа
@dp.message_handler(state=admin_form.menu)
async def admin_menu(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == 'Добавить в базу данных аккаунт':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS emails (
                email_id INTEGER NOT NULL PRIMARY KEY,
                email_value TEXT NOT NULL,
                given  INTEGER DEFAULT 1,
                given_to  INTEGER DEFAULT 1,
                valid  INTEGER DEFAULT 1
            )  """)
            con.commit()
            await bot.send_message(message.from_user.id,'Введите аккаунт в формате email:телефон:имя:фамилия:пароль',reply_markup=types.ReplyKeyboardRemove())
            await admin_form.register_new_email.set()
    elif answer == 'Проверить аккаунты после холда':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM holding',).fetchall()
            for row in r:
                email_id = row[0]
                if row[4] == 2 and row[5] == 1:
                   r_2 = cur.execute('SELECT * FROM emails',).fetchall()
                   for row_2 in r_2:
                       email = str(row_2[1]).split(':')[0]
                       if row[1] == email:
                           await bot.send_message(message.from_user.id,f'{row_2[1]}',reply_markup=admin_check_keyboard)
                           await state.update_data(email_state = email)
                           await state.update_data(email_id_state = email_id)
                           await admin_form.check.set()
                           con.commit()
                           break
                else:
                    await bot.send_message(message.from_user.id,'Нет аккаунтов для проверки') 
    else:
        pass

#Проверка на валидность
@dp.message_handler(state=admin_form.check)
async def admin_check(message: types.Message,state : FSMContext):
    answer = message.text
    data = await state.get_data()
    email_id_state = data.get('email_id_state')
    email = data.get('email')
    if answer == 'Валид':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('UPDATE emails SET valid=2 WHERE email_id=?', (email_id_state,))
            r = cur.execute('SELECT * FROM emails',).fetchall()
            for row in r:
                if row[0] == email_id_state:
                    user_id = row[3]
                    r_2 = cur.execute('SELECT * FROM users',).fetchall()
                    for row_2 in r_2:
                        hold_2 = int(row_2[1])-2
                        balans_2 = int(row_2[0])+2
                        if user_id == row_2[4]:
                            cur.execute('UPDATE users SET hold=? WHERE user_id=?', (hold_2,user_id))
                            cur.execute('UPDATE users SET balans=? WHERE user_id=?', (balans_2,user_id))
                            cur.execute('UPDATE holding SET payed=2 WHERE account=?', (email,))
                            con.commit()
                            break
        await state.finish()
        await bot.send_message(message.from_user.id,'Меню админа',reply_markup=admin_keyboard)
        await admin_form.menu.set()
    elif answer == 'Не валид':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM users',).fetchall()
            for row in r:
                if row[4] == message.from_user.id:
                    hold_2 = int(row[1])-2
                    cur.execute('UPDATE users SET hold=? WHERE user_id=?', (hold_2,row[4]))
                    cur.execute('UPDATE emails SET valid=3 WHERE email_id=?', (email_id_state,))
                    cur.execute('UPDATE holding SET payed=2 WHERE account=?', (email,))  
                    con.commit()
                    break
        await state.finish()
        await bot.send_message(message.from_user.id,'Меню админа',reply_markup=admin_keyboard)
        await admin_form.menu.set()
#Вписываем в базу данных почту
@dp.message_handler(state=admin_form.register_new_email)
async def admin_register_email(message: types.Message,state : FSMContext):
    answer = message.text
    print(answer)
    with sq.connect('database.db') as con:
        cur = con.cursor()
        cur.execute("INSERT INTO emails (email_value) VALUES (?)", (answer,))
        con.commit()
        await bot.send_message(message.from_user.id,'Меню админа',reply_markup=admin_keyboard)
        await admin_form.menu.set()
#Логика меню

@dp.message_handler(state=menu_form.main_menu)
async def menu(message : types.Message,state : FSMContext):
    answer = message.text
    if answer == '➕ Зарегистрировать новый аккаунт':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM emails').fetchall()
            for row in r:
                email_id = row[0]
                email_value = row[1]
                given = row[2]
                given_to = row[3]
                valid = row[4]
                if given == 1 and given_to == 1 and valid == 1:
                    email = str(email_value).split(':')[0]
                    phone = str(email_value).split(':')[1]
                    name = str(email_value).split(':')[2]
                    sur_name = str(email_value).split(':')[3]
                    password = str(email_value).split(':')[4]
                    await message.answer(f'Зарегистрируйте аккаунт Gmail используя указанные данные, и получите 2.0₽\n\nEmail:{email}\nТелефон:{phone}\nИмя: {name}\nФамилия: {sur_name}\n\nПароль: {password}\n\n🔐 Обязательно используйте указанный пароль, иначе аккаунт не будет оплачен',reply_markup=register_keyboard)
                    cur.execute('UPDATE emails SET given=2 WHERE email_id=?', (email_id,))
                    cur.execute('UPDATE emails SET given_to=? WHERE email_id=?', (message.from_user.id,email_id))
                    await state.update_data(email_state = email)
                    await register_form.process.set()
                    break
            else:
                await bot.send_message(message.from_user.id,'Нет аккаунтов в базе данных для регистрации,обратитесь к админу пусть пополнит!')
    elif answer == '💰 Баланс':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM users',).fetchall()
            for row in r:
                if row[4] == message.from_user.id:
                    balans_db = row[0]
                    hold_db = row[1]
                    await bot.send_message(message.from_user.id,f'Баланс: {balans_db}₽\nХолд: {hold_db}₽',reply_markup=balans_keyboard)
                    await balans.check.set()
                    break

    elif answer == '📋 Мои аккаунты':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM users',).fetchall()
            for row in r:
                if row[4] == message.from_user.id:
                    accounts_db = row[3]
                    await bot.send_message(message.from_user.id,f'{accounts_db}')
                    break
    elif answer == '💬 Помощь':
        await bot.send_message(message.from_user.id,'Переходим в разде помощь',reply_markup=types.ReplyKeyboardRemove())
        await bot.send_message(message.from_user.id,'Наиболее распространенные вопросы:',reply_markup=help_keyboard)
        await help_form.help.set()
    else:
        pass



#Регистрация

@dp.message_handler(state=register_form.process)
async def register_process(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '✔️ Готово':
        await bot.send_message(message.from_user.id,'🔄 Проверка аккаунта. Подождите')
        data = await state.get_data()
        email_state = data.get('email_state')
        email_address = f"{email_state}"
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email_address})
        status = response.json()['status']
        if status == "valid":
            await bot.send_message(message.from_user.id,'❔Вы уверены, что при регистрации указали верный пароль?\n\n❗️Если вы ошиблись, аккаунт не будет оплачен',reply_markup=register_valid_step1_keyboard)
            await register_form.valid_step1.set()
        else:
            data = await state.get_data()
            email_state = data.get('email_state')
            await bot.send_message(message.from_user.id,f'‼️ Gmail аккаунт {email_state} не существует\n\n❕ Возвращайтесь после окончания регистрации',reply_markup=register_keyboard)
            await register_form.process.set()
    elif answer == '🚫 Отменить регистрацию':
        await bot.send_message(message.from_user.id,'Вы уверены, что хотите отменить регистрацию?',reply_markup=register_cancel_keyboard)
        await register_form.cancel.set()




#Отмена регистрации

@dp.message_handler(state=register_form.cancel)
async def register_cancel(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '🚫 Да, отменить':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute('UPDATE emails SET given=1 WHERE given_to=?', (message.from_user.id,))
            cur.execute('UPDATE emails SET given_to=1 WHERE given_to=?', (message.from_user.id,))
            await bot.send_message(message.from_user.id,'Регистрация отменена',reply_markup=menu_keyboard)
            await menu_form.main_menu.set()
    elif answer == '🔙 Назад':
        data = await state.get_data()
        email_state = data.get('email_state')
        await bot.send_message(message.from_user.id,f'Продолжайте регистрацию аккаунта:\n\n {email_state}',reply_markup=register_keyboard)
        await register_form.process.set()




#Подтверждения того что ввели верный пароль

@dp.message_handler(state=register_form.valid_step1)
async def register_valid_step2(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '🔑 Я подтверждаю корректность пароля':
        await bot.send_message(message.from_user.id,'☎️Вы уверены, что при регистрации указали верный телефон?\n\n❗️Если вы ошиблись, аккаунт не будет оплачен',reply_markup=register_valid_step2_keyboard)   
        await register_form.valid_step2.set()




#Подтверждения того что ввели верный телефон

@dp.message_handler(state=register_form.valid_step2)
async def register_valid_sterp3(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '📴 Я подтверждаю, что в профиле указан верный телефон':
        await bot.send_message(message.from_user.id,'📩 Если при регистрации аккаунта вы указывали резервную почту, перейдите по ссылке и удалите ее\n\n❗️ Если в безопасности профиля останется резервная почта, аккаунт не будет оплачен',reply_markup=register_valid_step3_keyboard)   
        await register_form.valid_step3.set()




#Подтверждения того что ввели верный телефон

@dp.message_handler(state=register_form.valid_step3)
async def register_valid_sterp3(message: types.Message,state : FSMContext):
    answer = message.text 
    if answer == '📨 Я подтверждаю, что в профиле нет резервной почты':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM users',).fetchall()
            for row in r:
                if row[4] == message.from_user.id:
                    data = await state.get_data()
                    email_state = data.get('email_state')
                    history = row[2]
                    hold = row[1]
                    account_holding = f'{email_state}'
                    if hold =='NONE':
                        history_2 = str(history)+f'{email_state}\n'
                        cur.execute('UPDATE users SET history=? WHERE user_id=?', (history_2,message.from_user.id))
                        cur.execute('UPDATE users SET hold=? WHERE user_id=?', (hold,message.from_user.id))
                        cur.execute('UPDATE users SET accounts=? WHERE user_id=?', (history_2,message.from_user.id))
                        cur.execute('INSERT INTO holding (account,user_id) VALUES (?,?)', (account_holding,message.from_user.id))
                        con.commit()
                        await bot.send_message(message.from_user.id,'Аккаунт принят в обработку\n\n2.0₽ будут переведены на основной баланс после 7-ми дневного холда\n\nПока можете приступить к регистрации новых аккаунтов',reply_markup=menu_keyboard)
                        await state.finish()
                        await menu_form.main_menu.set()
                        break
                    else:
                        history_2 = f'{email_state}\n'
                        hold_2 = int(hold)+2
                        cur.execute('UPDATE users SET history=? WHERE user_id=?', (history_2,message.from_user.id))
                        cur.execute('UPDATE users SET hold=? WHERE user_id=?', (hold_2,message.from_user.id))
                        cur.execute('UPDATE users SET accounts=? WHERE user_id=?', (history_2,message.from_user.id))
                        cur.execute('INSERT INTO holding (account,user_id) VALUES (?,?)', (account_holding,message.from_user.id))
                        con.commit()
                        await bot.send_message(message.from_user.id,'Аккаунт принят в обработку\n\n2.0₽ будут переведены на основной баланс после 7-ми дневного холда\n\nПока можете приступить к регистрации новых аккаунтов',reply_markup=menu_keyboard)
                        await state.finish()
                        await menu_form.main_menu.set()
                        break




#Меню баланса

@dp.message_handler(state=balans.check)
async def balans_menu(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '💳 Вывести':
        await bot.send_message(message.from_user.id,'Выберите способ вывода',reply_markup=withdraw_keyboard)
        await balans.withdraw.set()
    elif answer == '📝 История баланса':
        with sq.connect('database.db') as con:
            cur = con.cursor()
            r = cur.execute('SELECT * FROM users',).fetchall()
            for row in r:
                if row[4] == message.from_user.id:
                    history = row[2]
                    await bot.send_message(message.from_user.id,f'🟠 Окончание регистрации аккаунта:\n{history}')
                    break
    elif answer == '🔙 Назад':
        await bot.send_message(message.from_user.id,'Выберите действие из списка меню',reply_markup=menu_keyboard)
        await menu_form.main_menu.set()


# Вывод 
@dp.message_handler(state=balans.withdraw)
async def withdraw(message: types.Message,state : FSMContext):
    answer = message.text
    with sq.connect('database.db') as con:
        cur = con.cursor()
        r = cur.execute('SELECT * FROM users',).fetchall()
        for row in r:
            if row[4] == message.from_user.id:
                if row[1] == 0:
                    await bot.send_message(message.from_user.id,'На балансе нет денег')
                    await bot.send_message(message.from_user.id,'Выберите действие из списка меню',reply_markup=menu_keyboard)
                    await menu_form.main_menu.set()
            else:
                if answer == 'payer':
                    await state.update_data(payment = 'payer')
                    await bot.send_message(message.from_user.id,'Введите номер кошелька payer',reply_markup=types.ReplyKeyboardRemove())
                    await balans.write.set()
                elif answer == 'webmoney':
                    await state.update_data(payment = 'webmony')
                    await bot.send_message(message.from_user.id,'Введите номер кошелька webmoney',reply_markup=types.ReplyKeyboardRemove())
                    await balans.write.set()
                elif answer == 'карта':
                    await state.update_data(payment = 'карта')
                    await bot.send_message(message.from_user.id,'Введите номер карты',reply_markup=types.ReplyKeyboardRemove())
                    await balans.write.set()



# Вписываем данные
@dp.message_handler(state=balans.write)
async def balans_write(message: types.Message,state : FSMContext):
    with sq.connect('database.db') as con:
        cur = con.cursor()
        r = cur.execute('SELECT * FROM users',).fetchall()
        for row in r:
            if row[4] == message.from_user.id:
                balans = row[0]
                answer = message.text
                data = await state.get_data()
                payment = data.get('payment')
                await bot.send_message(703170971,f'Вывод на {payment} : {answer}, {balans} рублей.')
                await bot.send_message(message.from_user.id,'Заявка на вывод создана',reply_markup=menu_keyboard)
                cur.execute('UPDATE users SET balans=0 WHERE user_id=?', (message.from_user.id,))
                await state.finish()
                await menu_form.main_menu.set()
                break

@dp.callback_query_handler(text='help_1',state=help_form.help)
async def help_1(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'"Холд" - это 7-ми дневный  период, в течении которого "отлеживается" аккаунт Gmail. Дело в том, что в течении 5-ти дней после создания аккаунта, Google может его заблокировать. По истечению  "отлежки", аккаунт попадает на модерацию, после которой происходит начисление средств на "Баланс".',reply_markup=help_keyboard_cancel)

@dp.callback_query_handler(text='help_2',state=help_form.help)
async def help_2(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'Что бы Google при регистрации не попросил вас подтвердить номер телефона, следует придерживаться некоторых рекомендаций:\n\n✖️Не регистрируйте более двух аккаунтов в сутки, из одного браузера.\n✖️Не регистрируйте более двух аккаунтов в сутки, с одного IP-адреса.\n✖️Не устанавливайте в браузер расширения.\n✖️Не используйте VPN.\n\n✅ Используйте браузерный режим "Инкогнито" (или очищайте кэш браузера, после каждой регистрации).\n✅ Используйте эмуляторы андроид устройств.\n✅ Используйте несколько "Portable" браузеров.\n\n❕Если ваш интернет-провайдер предоставляет динамические IP-адреса, отключите и включите модем. Данная операция сменит ваш IP-адрес\n❕При регистрации через мобильную сеть, отключите и включите интернет. Данная операция сменит ваш IP-адрес.\n\nЕсли вышеописанные действия не помогают обойти sms подтверждение, то вам придется указать номер на который вы сможете принять sms. Вы можете использовать как свой личный номер, так и номер полученный на сервисах "sms-активаций". После подтверждения номера, его необходимо удалить из аккаунта.',reply_markup=help_keyboard_cancel)

@dp.callback_query_handler(text='help_3',state=help_form.help)
async def help_3(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'В течении 7-ми дней после регистрации, Google может заблокировать подозрительные аккаунты, или аккаунты идентифицированные как "связанные с подозрительными". Такие аккаунты не оплачиваются и помечаются как "Недоступные".\n\nЕсли вы попытаетесь войти в такой аккаунт, вы поймете в чем дело, этим аккаунтом невозможно пользоваться.',reply_markup=help_keyboard_cancel)

@dp.callback_query_handler(text='help_4',state=help_form.help)
async def help_4(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'Что бы Google не заблокировал ваш аккаунт, следует придерживаться некоторых рекомендаций:\n\n✖️Не входите в аккаунт после регистрации.\n✖️Не регистрируйте более двух аккаунтов в сутки, из одного браузера.\n✖️Не регистрируйте более двух аккаунтов в сутки, с одного IP-адреса.\n✖️Не устанавливайте в браузер расширения.\n✖️Не используйте VPN.\n\n✅ Используйте браузерный режим "Инкогнито" (или очищайте кэш браузера, после каждой регистрации).\n✅ Используйте эмуляторы андроид устройств.\n✅ Используйте несколько "Portable" браузеров.\n\n❕Если ваш интернет-провайдер предоставляет динамические IP-адреса, отключите и включите модем. Данная операция сменит ваш IP-адрес.\n❕При регистрации через мобильную сеть, отключите и включите интернет. Данная операция сменит ваш IP-адрес.',reply_markup=help_keyboard_cancel)

@dp.callback_query_handler(text='help_5',state=help_form.help)
async def help_5(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'Бот примет любое количество аккаунтов, которое вы сможете зарегистрировать. Главное, что бы Google не заблокировал их в период 7-ми дневного холда.',reply_markup=help_keyboard_cancel)

@dp.callback_query_handler(text='help_6',state=help_form.help)
async def help_6(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer('Выберите действие из списка меню',reply_markup=menu_keyboard)
    await menu_form.main_menu.set()


@dp.callback_query_handler(text='cancel',state=help_form.help)
async def help_7(call: types.CallbackQuery, state: FSMContext):
    await call.message.edit_text(text=f'Наиболее распространенные вопросы:',reply_markup=help_keyboard)

def check_hold():
    t1 = datetime.datetime.now()
    while True:
        with sq.connect('database.db') as con:
            cur = con.cursor()
            cur.execute("""CREATE TABLE IF NOT EXISTS holding (
                id INTEGER NOT NULL PRIMARY KEY,
                account  TEXT,
                holding_day  INTEGER DEFAULT 0,
                user_id  INTEGER DEFAULT 1,
                holded INTEGER DEFAULT 1,
                payed INTEGER DEFAULT 1
            )  """)
            t2 = datetime.datetime.now()
            if t1>t2:
                r = cur.execute('SELECT * FROM holding',).fetchall()
                for row in r:
                    ids = row[0]
                    holding_day = int(row[2])+1
                    if row[3] == 7:
                        cur.execute('UPDATE holding SET holded=2 WHERE id=?', (ids,))
                    else:
                        try:
                            cur.execute('UPDATE holding SET holding_day=? WHERE id=?', (holding_day,ids))
                        except Exception as ex:
                            print(ex)
                con.commit()
            else:
                pass
        time.sleep(3600)
if __name__ == '__main__':
    t1 = Thread(target=check_hold,args=[])
    t1.start()
    executor.start_polling(dp, skip_updates=True)

    