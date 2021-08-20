from os import stat
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from threading import *
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
import logging
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from config.keyboard import *
import requests



# запуск и инициализация бота
API_TOKEN = '1966287693:AAGkUszbRQ-Qsmi5YJ81T7mBiVrnn29i68A'
logging.basicConfig(level=logging.INFO)
bot = Bot(API_TOKEN)


# Раабота с машиной состояний
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


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

class balans(StatesGroup):
    check = State()
    withdraw = State()
    write = State()
# Запускаем стартовое меню

@dp.message_handler(commands=['start'], state='*')
async def menu_start(message: types.Message):
    await message.answer('Регистрируйте аккаунты Gmail и получайте за это оплату.\nЗа каждый аккаунт вы получите: 2.0₽',reply_markup=menu_keyboard)
    await menu_form.main_menu.set()



#Логика меню

@dp.message_handler(state=menu_form.main_menu)
async def menu(message : types.Message,state : FSMContext):
    answer = message.text
    print(answer)
    if answer == '➕ Зарегистрировать новый аккаунт':
        await message.answer('Зарегистрируйте аккаунт Gmail используя указанные данные, и получите 2.0₽\n\nEmail:<blank>@gmail.com\nИмя: <blank>\nФамилия: <blank>\n\nПароль: <blank>\n\n🔐 Обязательно используйте указанный пароль, иначе аккаунт не будет оплачен',reply_markup=register_keyboard)
        await register_form.process.set()
    elif answer == '💰 Баланс':
        await bot.send_message(message.from_user.id,'Баланс: <blank>₽\nХолд: <blank>₽',reply_markup=balans_keyboard)
        await balans.check.set()
    else:
        pass



#Регистрация

@dp.message_handler(state=register_form.process)
async def register_process(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '✔️ Готово':
        await bot.send_message(message.from_user.id,'🔄 Проверка аккаунта. Подождите')
        email_address = f"hetohaddoivu8639@gmail.com"
        response = requests.get("https://isitarealemail.com/api/email/validate",params = {'email': email_address})
        status = response.json()['status']
        if status == "valid":
            await bot.send_message(message.from_user.id,'❔Вы уверены, что при регистрации указали верный пароль?\n\n❗️Если вы ошиблись, аккаунт не будет оплачен',reply_markup=register_valid_step1_keyboard)
            await register_form.valid_step1.set()
        else:
            await bot.send_message(message.from_user.id,'‼️ Gmail аккаунт <blank> не существует\n\n❕ Возвращайтесь после окончания регистрации',reply_markup=register_keyboard)
            await register_form.process.set()
    elif answer == '🚫 Отменить регистрацию':
        await bot.send_message(message.from_user.id,'Вы уверены, что хотите отменить регистрацию?',reply_markup=register_cancel_keyboard)
        await register_form.cancel.set()




#Отмена регистрации

@dp.message_handler(state=register_form.cancel)
async def register_cancel(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '🚫 Да, отменить':
        await bot.send_message(message.from_user.id,'Регистрация отменена',reply_markup=menu_keyboard)
        await menu_form.main_menu.set()
    elif answer == '🔙 Назад':
        await bot.send_message(message.from_user.id,'Продолжайте регистрацию аккаунта:\n\n <blank>',reply_markup=register_keyboard)
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
        await bot.send_message(message.from_user.id,'Аккаунт принят в обработку\n\n2.0₽ будут переведены на основной баланс после 7-ти дневного холда\n\nПока можете приступить к регистрации новых аккаунтов',reply_markup=menu_keyboard)
        await menu_form.main_menu.set()




#Меню баланса

@dp.message_handler(state=balans.check)
async def balans_menu(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == '💳 Вывести':
        await bot.send_message(message.from_user.id,'Выберите способ вывода',reply_markup=withdraw_keyboard)
        await balans.withdraw.set()
    elif answer == '📝 История баланса':
        pass
    elif answer == '🔙 Назад':
        pass


# Вывод 
@dp.message_handler(state=balans.withdraw)
async def withdraw(message: types.Message,state : FSMContext):
    answer = message.text
    if answer == 'payer':
        await bot.send_message(message.from_user.id,'Введите номер кошелька payer')
        await balans.write.set()
    elif answer == 'webmoney':
        await bot.send_message(message.from_user.id,'Введите номер кошелька webmoney')
        await balans.write.set()
    elif answer == 'карта':
        await bot.send_message(message.from_user.id,'Введите номер карты')
        await balans.write.set()



# Вписываем данные
@dp.message_handler(state=balans.write)
async def balans_write(message: types.Message,state : FSMContext):
    answer = message.text
    await bot.send_message(703170971,f'Вывод на <blank> {answer}, <blank> рублей.')
    await bot.send_message(message.from_user.id,'Заявка на вывод создана',reply_markup=menu_keyboard)
    await menu_form.main_menu.set()





if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)