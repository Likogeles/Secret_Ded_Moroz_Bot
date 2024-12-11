import asyncio
import random

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.types import Message
from aiogram.filters import CommandStart

from config import TOKEN, mainUserId
from user import User
from userState import UserState
from users import UsersList

bot = Bot(token=TOKEN)
dp = Dispatcher()

usersList = UsersList()


commands = ["/info", "/start_game"]


async def new_user(user: User):
    usersList.addUser(user)
    await bot.send_message(mainUserId, f"Новый пользователь:\n{getUserLink(user.getId(), user.getFirstName(), user.getSecondName())}", parse_mode=ParseMode.HTML)


def getUserLink(user_id, first_name, second_name) -> str:
    return f'<a href="tg://user?id={user_id}">{first_name} {second_name}</a>'


def shuffle_users():
    user_ids = []
    for i in usersList.getUsers():
        user_ids.append(i.getId())

    random.shuffle(user_ids)

    usersList.getUserById(user_ids[0]).setGiftUserId(user_ids[-1])
    for i in range(1, len(user_ids)):
        usersList.getUserById(user_ids[i]).setGiftUserId(user_ids[i-1])


@dp.message(CommandStart())
async def process_start_command(msg: Message):
    if not usersList.getUserById(msg.from_user.id):
        await new_user(User(msg.from_user.id, msg.from_user.first_name, msg.from_user.last_name, "UserState.setName"))
        await bot.send_message(msg.from_user.id, "Приветствую и добро пожаловать на Тайного Деда Мороза в Точке кипения УлГТУ!\n\n"
                                                 "Рекомендованная цена подарка: от 500 до 700 рублей.\n\n"
                                                 "Сейчас тебе надлежит ответить на три вопроса.\n\nОтвечай внимательно, "
                                                 "ибо второй попытки не будет!\n\n1) Какими именем и фамилией кличут тебя?")
    else:
        await bot.send_message(msg.from_user.id, "Твой профиль уже подключен.")


@dp.message()
async def get_text_message(msg: Message):
    if msg.from_user.id == mainUserId:
        if msg.text in commands:
            if msg.text == "/info":
                await bot.send_message(mainUserId, str(usersList), parse_mode=ParseMode.HTML)
                return
            if msg.text == "/start_game":
                shuffle_users()
                for i in usersList.getUsers():
                    gift_user = usersList.getUserById(i.getGiftUserId())
                    text = f'<span class="tg-spoiler">{gift_user.getUserLink()}</span> ждёт твоего дара!\n\n' \
                           f'🟩 Этот человек желает:\n<span class="tg-spoiler">{gift_user.getWant()}</span>\n\n' \
                           f'🟥 Этот человек не желает:\n<span class="tg-spoiler">{gift_user.getNotWant()}</span>'
                    await bot.send_message(i.getId(), text, parse_mode=ParseMode.HTML)
                    usersList.getUserById(i.getId()).setState(UserState.inGame)
                await bot.send_message(mainUserId, "Игра начата", parse_mode=ParseMode.HTML)
                return

    user = usersList.getUserById(msg.from_user.id)
    match user.getState():
        case UserState.setName:
            usersList.getUserById(user.getId()).setRealName(msg.text)
            usersList.getUserById(user.getId()).setState(UserState.setWant)
            await bot.send_message(msg.from_user.id, "2) Что бы ты хотел получить в дар?")
        case UserState.setWant:
            usersList.getUserById(user.getId()).setWant(msg.text)
            usersList.getUserById(user.getId()).setState(UserState.setNotWant)
            await bot.send_message(msg.from_user.id, "3) Чего ты точно не желаешь получить в дар?")
        case UserState.setNotWant:
            usersList.getUserById(user.getId()).setNotWant(msg.text)
            usersList.getUserById(user.getId()).setState(UserState.waiting)
            kb = [
                [types.KeyboardButton(text="Заполнить профиль заново")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await bot.send_message(msg.from_user.id, "Отлично!\n\nВ ближайшее время ты узнаешь имя того, кто будет ждать твоего подарка!", reply_markup=keyboard)
        case UserState.waiting:
            kb = [
                [types.KeyboardButton(text="Заполнить профиль заново")],
            ]
            keyboard = types.ReplyKeyboardMarkup(keyboard=kb, resize_keyboard=True)
            await bot.send_message(msg.from_user.id, "Ожидание жеребьёвки.", reply_markup=keyboard)
        case _:
            await bot.send_message(msg.from_user.id, "Игра идёт.")
    if msg.text:
        if msg.text == "Заполнить профиль заново" and user.getState() == UserState.waiting:
            usersList.getUserById(user.getId()).setState(UserState.setName)
            await bot.send_message(msg.from_user.id, "1) Какими именем и фамилией кличут тебя?", reply_markup=types.ReplyKeyboardRemove())

    return


async def main():
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
