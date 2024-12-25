import random
import datetime
import telebot
from telebot.types import Message, ReplyKeyboardMarkup as rkm, InlineKeyboardMarkup as ikm, InlineKeyboardButton as ikb, \
    ReplyKeyboardRemove as rkr, CallbackQuery
import asyncio
from cfg import TOKEN
from datapack import *

kent = telebot.TeleBot(TOKEN)
temp = {}
clear = rkr()


class Opps:
    opps = {
        "Zlodey": (700, 66, 1),
        "Dunhen": (1, 1500, 2),
        "Squore": (1350, 120, 3),
        "BoSinn": (2222, 222, 4),
        "Grailed": (9000, 45, 5),
        "Babytron": (5000, 250, 6),
        "Freeman": (7575, 348, 7),
        "Executor": (10000, 500, 8),
        "lazer_dim700": (25000, 15000, 9),
        "Unbeatable": (9999999, 999999, 10)

    }

    def __init__(self, herolvl):
        for KEY in self.opps:
            if herolvl == self.opps[KEY][2]:
                self.name = KEY
                break
        self.hp = self.opps[self.name][0]
        self.dmg = self.opps[self.name][1]


@kent.message_handler(["start"])
def start(m: Message):
    if newplayer(m):
        temp[m.chat.id] = {}
        register(m)
    else:
        menu(m)


@kent.message_handler(["menu"])
def menu(m: Message):
    try:
        print(temp[m.chat.id])
    except KeyError:
        temp[m.chat.id] = {}
    txt = "Что будешь делать?\n/square - на площадь\n/home - домой\n/stats - статистика"
    kent.send_message(m.chat.id, txt)


@kent.message_handler(["home"])
def home(m: Message):
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row("Пожрать", "Дрыхнуть")
    kent.send_message(m.chat.id, "Ты в хапре, чем ты хочешь заняться?", reply_markup=kb)
    kent.register_next_step_handler(m, homehandler)


@kent.message_handler(["stats"])
def stats(m: Message):
    player = bars.read("userId", m.chat.id)
    txt = f"Твое хп👅👅👅: {player[3]}\nТвой урон: {player[4]}\nУровень: {player[6]}\nТвой опыт: {player[5]}"
    kent.send_message(m.chat.id, txt)
    asyncio.run(asyncio.sleep(3))
    menu(m)
    return


@kent.message_handler(["square"])
def square(m: Message):
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row("Тренировка", "Испытания", "Махыч")
    kent.send_message(m.chat.id, "Выбирай", reply_markup=kb)
    kent.register_next_step_handler(m, squarehandler)


@kent.message_handler(["fooddispencer"])
def dispencer(m: Message):
    id, food = hpbars.read("userId", m.chat.id)
    print(food)
    food["Бубалех"] = [3, 37]
    hpbars.write([id, food])
    print("jjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjjj")


@kent.callback_query_handler(func=lambda call: True)
def callback(call: CallbackQuery):
    print(call.data)

    if call.data.startswith("food_"):
        a = call.data.split("_")
        eating(call.message, a[1], a[2])
        id, food = hpbars.read("userId", call.message.chat.id)
        kb = ikm()
        if food == {}:
            kent.send_message(call.message.chat.id, "Иди спи", reply_markup=clear)
            kent.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
            asyncio.run(asyncio.sleep(1))
            menu(call.message)
            return
        for x in food:
            if food[x][0] > 0:
                kb.row(ikb(f"{x} - {food[x][0]}pcs +{food[x][1]}", callback_data=f"food_{x}_{food[x][1]}"))
        kent.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=kb)
    if call.data.startswith("sleep_"):
        a = call.data.split("_")
        t = int(a[1]) / 4.9
        kent.send_message(call.message.chat.id, f"Ты лег спать на {round(t)} секунд")
        asyncio.run(asyncio.sleep(t))
        healing(call.message, a[1])
        kent.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        menu(call.message)
        return
    if call.data == "menu":
        kent.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        menu(call.message)
        return
    if call.data == "workout":
        player = bars.read("userId", call.message.chat.id)
        player[4] += player[6] / 10
        player[4] = round(player[4], 2)
        bars.write(player)
        kent.answer_callback_query(call.id, f"growin upp! \nTeперь ты наносишь {player[4]}", True)


def eat(m: Message):
    id, food = hpbars.read("userId", m.chat.id)
    kb = ikm()
    if food == {}:
        kent.send_message(m.chat.id, "Иди спи", reply_markup=clear)
        asyncio.run(asyncio.sleep(1))
        menu(m)
        return
    for x in food:
        if food[x][0] > 0:
            kb.row(ikb(f"{x} - {food[x][0]}pcs +{food[x][1]}", callback_data=f"food_{x}_{food[x][1]}"))
    kent.send_message(m.chat.id, "Что хочешь?", reply_markup=kb)


def eating(m: Message, ft, hp):
    id, food = hpbars.read("userId", m.chat.id)
    player = bars.read("userId", m.chat.id)
    if food[ft][0] == 1:
        del food[ft]
    else:
        food[ft][0] -= 1
    hpbars.write([m.chat.id, food])

    player[3] += int(hp)
    bars.write(player)
    print("Ты поел")


def sleep(m: Message):
    player = bars.read("userId", m.chat.id)
    underhalf = (heroes[player[2]][0] + (player[-1] - 1) * 22) // 2 - player[3]
    belowhalf = (heroes[player[2]][0] + (player[-1] - 1) * 22) - player[3]
    kb = ikm()
    if underhalf > 0:
        kb.row(ikb(f"Покумарить + {underhalf}hp", callback_data=f"sleep_{underhalf}"))
    if belowhalf > 0:
        kb.row(ikb(f"Поспи + {belowhalf}hp", callback_data=f"sleep_{belowhalf}"))
    if len(kb.keyboard) == 0:
        kent.send_message(m.chat.id, "Я думаю ты бодр", reply_markup=clear)
        menu(m)
        return
    kent.send_message(m.chat.id, "Спать", reply_markup=kb)


def healing(m: Message, hp):
    player = bars.read("userId", m.chat.id)
    player[3] += int(hp)
    bars.write(player)
    print('игрок поспал')


def workout(m: Message):
    kb = ikm()
    kb.row(ikb("Тренить", callback_data="workout"))
    kb.row(ikb("Назад", callback_data="menu"))
    kent.send_message(m.chat.id, "Жми это", reply_markup=kb)


def block(m: Message):
    try:
        print(temp[m.chat.id])
    except KeyError:
        temp[m.chat.id] = {}
    try:
        print(temp[m.chat.id]["win"])
    except KeyError:
        temp[m.chat.id]["win"] = 0
    kent.send_message(m.chat.id, "Будьте на готове...", reply_markup=clear)
    asyncio.run(asyncio.sleep(3))
    sides = ["Слева", "Справа", "Сверху", "Снизу"]
    random.shuffle(sides)
    side = random.choice(sides)

    kb = rkm(True, False)
    kb.row(sides[0], sides[3])
    kb.row(sides[1], sides[2])

    kent.send_message(m.chat.id, f"Защищайся! Удар {side}!", reply_markup=kb)
    temp[m.chat.id]["start"] = datetime.datetime.now().timestamp()
    kent.register_next_step_handler(m, blockhandler, side)


def blockhandler(m: Message, side):
    temp[m.chat.id]["end"] = datetime.datetime.now().timestamp()
    timer = temp[m.chat.id]["end"] - temp[m.chat.id]["start"]
    if timer > 3:
        temp[m.chat.id]["win"] = 0
        kent.send_message(m.chat.id, text="ЛОХ!!", reply_markup=clear)
        asyncio.run(asyncio.sleep(2))
        menu(m)
        return
    else:
        if side != m.text:
            temp[m.chat.id]["win"] = 0
            kent.send_message(m.chat.id, text="ЛОХ!!", reply_markup=clear)
            asyncio.run(asyncio.sleep(2))
            menu(m)
            return
        else:
            temp[m.chat.id]["win"] += 1
            if temp[m.chat.id]["win"] < 5:
                kent.send_message(m.chat.id, "Давай дальше", reply_markup=clear)
                block(m)
            else:
                temp[m.chat.id]["win"] = 0
                kent.send_message(m.chat.id, "Кроссовок!", reply_markup=clear)
                player = bars.read("userId", m.chat.id)
                player[3] += 150
                bars.write(player)
                menu(m)
                return


def fight(m: Message):
    player = bars.read("userId", m.chat.id)
    enemy = Opps(player[-1])
    kent.send_message(m.chat.id, f"Твой враг {enemy.name}")
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    kb.row("Атаковать", "Сбежать")
    kent.send_message(m.chat.id, "Что выбираешь?", reply_markup=kb)
    kent.register_next_step_handler(m, fighthandler, enemy, kb)


def fighthandler(m: Message, enemy: Opps, kb: rkm):
    if m.text == "Атаковать":
        pvp(m, enemy)
    elif m.text == "Сбежать":
        pass
    else:
        kent.send_message(m.chat.id, "Ты по-моему перепутал ", reply_markup=kb)
        kent.register_next_step_handler(m, fighthandler, enemy, kb)


def pvp(m: Message, enemy: Opps):
    asyncio.run(asyncio.sleep(1))
    if playerattack(m, enemy):
        if enemyattack(m, enemy):
            pvp(m, enemy)
    else:
        asyncio.run(asyncio.sleep(2))
        menu(m)
        return


def playerattack(m: Message, enemy: Opps):
    player = bars.read("userId", m.chat.id)
    enemy.hp -= player[4]
    if enemy.hp <= 0:
        kent.send_message(m.chat.id, "Ты победил")
        player[-1] += 1
        bars.write(player)
        return False
    else:
        kent.send_message(m.chat.id, f"У врага {enemy.hp} здоровья")
        return True


def enemyattack(m: Message, enemy: Opps):
    player = bars.read("userId", m.chat.id)
    player[3] -= enemy.dmg
    bars.write(player)
    if player[3] <= 0:
        player[3] = 0
        bars.write(player)
        kent.send_message(m.chat.id, "Ты проиграл!")
        asyncio.run(asyncio.sleep(2))
        menu(m)
        return
    else:
        kent.send_message(m.chat.id, f"У тебя {player[3]} здоровья")
        return True


def newplayer(m: Message):
    prayers = bars.read_all()
    for id in prayers:
        if m.chat.id == id[0]:
            return False
    return True


def register(m: Message):
    txt = f"Привет, {m.from_user.first_name}. Введи свой никнейм"
    kent.send_message(m.chat.id, text=txt)
    kent.register_next_step_handler(m, regist3r)


def regist3r(m: Message):
    name = m.text
    temp[m.chat.id]["name"] = name
    kb = rkm(resize_keyboard=True, one_time_keyboard=True)
    for key in list(heroes):
        kb.row(key)

    kent.send_message(m.chat.id, text="Выбирай за кого будешь играть.", reply_markup=kb)
    kent.register_next_step_handler(m, sizo)


def sizo(m: Message):
    hero = m.text
    hp, dmg = heroes[hero]
    bars.write([m.chat.id, temp[m.chat.id]["name"], hero, hp, dmg, 0, 1])
    hpbars.write([m.chat.id, {}], )
    print("загастрирован")
    menu(m)


def homehandler(m: Message):
    if m.text == "Пожрать":
        eat(m)
    if m.text == "Дрыхнуть":
        sleep(m)


def squarehandler(m: Message):
    if m.text == "Тренировка":
        workout(m)
    if m.text == "Испытания":
        block(m)
    if m.text == "Махыч":
        fight(m)


kent.infinity_polling()
