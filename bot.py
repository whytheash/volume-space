import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.ext import Updater

#Подклчение к базе данных
from datetime import datetime

from pymongo import MongoClient

# Подключение к MongoDB
MONGODB_URI = os.environ.get("MONGO_URI")
client = MongoClient(MONGODB_URI)
db = client["volume-space"]  # Название базы
users_collection = db["users_data"]  # Коллекция для пользователей
results_collection = db["test_results"]  # Коллекция для результатов

# import gspread
# from google.oauth2.service_account import Credentials

# from datetime import datetime

# # Авторизация в Google Sheets
# scope = [
#     "https://www.googleapis.com/auth/spreadsheets",  # Доступ к таблицам
#     "https://www.googleapis.com/auth/drive"          # Доступ к Google Drive
# ]
# creds = Credentials.from_service_account_file("credentials.json", scopes=scope)
# client = gspread.authorize(creds)

# Открытие таблиц
# users_sheet = client.open("vlmbot-data").worksheet("users_data")
# results_sheet = client.open("vlmbot-data").worksheet("test_results")    

# from flask import Flask
# import os

# app = Flask(__name__)

# @app.route('/')
# def home():
#     return "Bot is running"

# if __name__ == "__main__":
#     app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 3000)))


TOKEN = os.environ.get("TELEGRAM_TOKEN")  # Токен на railway

bot = Bot(token=TOKEN)
dp = Dispatcher()

TYPES = {
    "Чилл гай": {"Выносливость": 1, "Креативность": 7, "Гибкость": 6, "Ответственность": 2, "Стрессоустойчивость": 1, "Клиенты в день": 1, "Рабочие дни": 1},
    "Тру артист": {"Выносливость": 8, "Креативность": 11, "Гибкость": 10, "Ответственность": 7, "Стрессоустойчивость": 9, "Клиенты в день": 2, "Рабочие дни": 2},
    "Неформал": {"Выносливость": 6, "Креативность": 10, "Гибкость": 9, "Ответственность": 4, "Стрессоустойчивость": 2, "Клиенты в день": 1, "Рабочие дни": 1},
    "Блэкворкер": {"Выносливость": 10, "Креативность": 5, "Гибкость": 1, "Ответственность": 11, "Стрессоустойчивость": 5, "Клиенты в день": 1, "Рабочие дни": 2},
    "Коммерческий": {"Выносливость": 4, "Креативность": 1, "Гибкость": 11, "Ответственность": 5, "Стрессоустойчивость": 8, "Клиенты в день": 4, "Рабочие дни": 5},
    "Опоздун": {"Выносливость": 7, "Креативность": 6, "Гибкость": 8, "Ответственность": 1, "Стрессоустойчивость": 4, "Клиенты в день": 2, "Рабочие дни": 2},
    "Реальный хард": {"Выносливость": 11, "Креативность": 9, "Гибкость": 7, "Ответственность": 10, "Стрессоустойчивость": 10, "Клиенты в день": 4, "Рабочие дни": 7},
    "В тихом омуте": {"Выносливость": 3, "Креативность": 4, "Гибкость": 4, "Ответственность": 3, "Стрессоустойчивость": 7, "Клиенты в день": 2, "Рабочие дни": 2},
    "Мини-тату": {"Выносливость": 2, "Креативность": 2, "Гибкость": 3, "Ответственность": 9, "Стрессоустойчивость": 6, "Клиенты в день": 5, "Рабочие дни": 3},
    "Ночная бабочка": {"Выносливость": 9, "Креативность": 3, "Гибкость": 5, "Ответственность": 6, "Стрессоустойчивость": 11, "Клиенты в день": 1, "Рабочие дни": 3},
    "Только начал": {"Выносливость": 5, "Креативность": 8, "Гибкость": 2, "Ответственность": 8, "Стрессоустойчивость": 3, "Клиенты в день": 1, "Рабочие дни": 1}
}

DESCRIPTIONS = {
    "Чилл гай": "для тебя татуировка больше походит на хобби, ты работаешь в своем размеренном темпе, без ущерба здоровью и своему состоянию, так держать!",
    "Тру артист": "ты — настоящий художник индустрии! тобой движет желание выделяться, твой стиль.",
    "Неформал": "у тебя свой взгляд на индустрию, любишь эксперименты и смелые решения!",
    "Блэкворкер": "ты настоящий дзен-мастер! ровный плотный покрас — непростая задачка!",
    "Коммерческий": "что-то про тату-завод слышали? это про тебя! наверняка за твоими плечами большое количество работ.",
    "Опоздун": "с кем не бывает! ситуации разные, но ты рискуешь потерять лояльность клиентов, не стоит расстраиваться! эту ситуацию можно исправить немного поработав с дисциплиной!",
    "Реальный хард": "ты настоящий фанат своего дела! но не забывай отдыхать и иногда ходить на массажи!",
    "В тихом омуте": "черти водятся… иногда ты берешься за проекты неочевидные для тебя и твоего стиля, эксперименты это круто!",
    "Мини-тату": "ты - мастер миниатюр! дело, которое дано далеко не каждому!",
    "Ночная бабочка": "кажется ты перепутал день с ночью! а может у тебя слишком много проектов и тебе приходится жертвовать сном? верю что твои старания дадут большой результат!",
    "Только начал": "все с чего-то начинают, возможно тебе нужно больше практики, не сдавайся - только вперед!"
}

class TestStates(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()
    Q6 = State()
    Q7 = State()
    Q8 = State()
    Q9 = State()
    Q10 = State()
    Q11 = State()
    Q12 = State()

QUESTIONS = {
    TestStates.Q1: (
        "1. ты открываешь расписание, а там 5 клиентов подряд. \n что сделаешь?",
        ["A. глаза боятся - а руки делают", "B. распределю часть работы на другие дни", "C. забьюсь в истерике в угол"]
    ),
    TestStates.Q2: (
        "2. ты решил сделать перерыв с клиентом. \n сколько он продлится?",
        ["A. 15 минут — хватит с головой", "B. не меньше 30 минут", "C. час, а то и два, нужно же набраться сил"]
    ),
    TestStates.Q3: (
        "3. твой клиент хочет эскиз из пинтереста, твои действия?",
        ["A. работаем, деньги не пахнут", "B. предложу свою альтернативу", "C. *заблокировать*"]
    ),
    TestStates.Q4: (
        "4. теперь клиент полностью меняет концепт татуировки в день сеанса",
        ["A. я за любые идеи, фрихенд - вперед!", "B. предложу альтернативу из свободных эскизов", "C. это не нормально... перенесу сеанс, чтобы успеть подготовить эскиз"]
    ),
    TestStates.Q5: (
        "5. твой клиент начал активно жаловаться на боль, что будем делать?",
        ["A. сорри, не на массаж пришел", "B. предложу обезболить кожу", "C. буду страдать вместе с ним"]
    ),
    TestStates.Q6: (
        "6. ты приходишь в студию, а там плотная посадка. места для вас не нашли...",
        ["A. возьму себя в руки и найду другую студию", "B. перенесу сеанс на другой день", "C. устрою скандал на студии"]
    ),
    TestStates.Q7: (
        "7. друг зовет в бар на всю ночь, но завтра у тебя сеанс. \n как будем действовать?",
        ["A. не пойду, мне еще на завтра эскиз готовить", "B. класс, оттянусь после сеанса!", "C. возьму клиента с собой, вместе веселее!"]
    ),
    TestStates.Q8: (
        "8. кажется, ты опаздываешь на сеанс на 30 минут...",
        ["A. вызову такси, приеду как можно раньше", "B. предупрежу, принесу извинения, предложу скидку", "C. как приду, так и приду"]
    ),
    TestStates.Q9: (
        "9. до сеанса 15 минут. клиент пишет, что его не будет и просит перенести сеанс. \nчто будем делать?",
        ["A. обозлюсь, но не подам вида", "B. «освободилось окошко, отдам со скидкой»", "C. больше не буду с ним работать, со мной так нельзя"]
    ),
    TestStates.Q10: (
        "10. рабочий день близится к концу, ты уже довольно уставший. \n и тут клиент начинает задавать очень много вопросов...",
        ["A. объясню все нюансы и успокою", "B. буду задавать много вопросов в ответ", "C. сяду в наушники"]
    ),
    TestStates.Q11: (
        "11. каким бы был твой идеальный график?",
        ["A. 1-2 клиента — не спеша", "B. 3-4 клиента — день прошел продуктивно", "C. 5+ клиентов — и это не предел!"]
    ),
    TestStates.Q12: (
        "12. в неделю ты хотел(а) бы работать...",
        ["A. 1-2 дня — и достаточно!", "B. 3-4 дня — на балансе", "C. 5-7 дней — работаю без остановки"]
    )
}

user_data = {}
start_message = "привет татуер! на связи волюм! \n\n" \
"мы проделали большой путь вместе с командой, чтобы в итоге этот тест дошел до тебя. надеемся, что он тебе понравится, а может даже вдохновит на что-то новое! \n результаты могут помочь понять в каком направлении развиваться, даже если сейчас ты новичок или вовсе не знаком с индустрией. \n\n" \
"хотим напомнить: этот тест создан исключительно в целях развлечения и самопознания. он примерно определяет твой тип по твоим действиям в тату-индустрии и позволяет посмотреть на свое искусство по-новому.\n но не является профессиональной оценкой или руководством к действию. \n\n" \
"поехали!"


@dp.message(Command("start"))
async def start_test(message: types.Message, state: FSMContext):

    #Внесение пользователя в БД
    user = message.from_user
    registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    def save_user(user):
        user_data = {
            "user_id": user.id,
            "username": user.username,
            "first_name": user.first_name,
            "last_name": user.last_name,
            "registration_date": datetime.now()
        }
        users_collection.update_one(
            {"user_id": user.id},
            {"$setOnInsert": user_data},
            upsert=True
        )

    save_user(user)

    await message.answer(start_message)
    await state.set_state(TestStates.Q1)
    await ask_question(message, state)

async def ask_question(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    text, buttons = QUESTIONS[current_state]
    builder = InlineKeyboardBuilder()
    for btn in buttons:
        button_text = btn.split(". ", 1)[1]
        builder.add(types.InlineKeyboardButton(text=button_text, callback_data=btn[0]))
    builder.adjust(1)
    await message.answer(text, reply_markup=builder.as_markup())

@dp.callback_query(F.data.in_(['A', 'B', 'C']))
async def handle_button(callback: types.CallbackQuery, state: FSMContext):
    current_state = await state.get_state()
    user_id = callback.from_user.id
    
    # Обновляем сообщение с выбранным ответом
    text, buttons = QUESTIONS[current_state]
    chosen_answer = next(btn for btn in buttons if btn.startswith(callback.data))
    await callback.message.edit_text(
        text=f"{text}\n\n Ваш выбор: {chosen_answer.split('. ', 1)[1]}",
        reply_markup=None
    )
    
    # Сохраняем ответ
    user_data.setdefault(user_id, {"answers": {}})
    user_data[user_id]["answers"][current_state] = callback.data
    
    # Переход к следующему вопросу
    next_states = {
        TestStates.Q1: TestStates.Q2,
        TestStates.Q2: TestStates.Q3,
        TestStates.Q3: TestStates.Q4,
        TestStates.Q4: TestStates.Q5,
        TestStates.Q5: TestStates.Q6,
        TestStates.Q6: TestStates.Q7,
        TestStates.Q7: TestStates.Q8,
        TestStates.Q8: TestStates.Q9,
        TestStates.Q9: TestStates.Q10,
        TestStates.Q10: TestStates.Q11,
        TestStates.Q11: TestStates.Q12,
        TestStates.Q12: None
    }
    next_state = next_states.get(current_state)
    
    if next_state:
        await state.set_state(next_state)
        await ask_question(callback.message, state)
    else:
        await calculate_result(callback.message, user_id)
        await state.clear()

async def calculate_result(message: types.Message, user_id: int):
    answers = user_data[user_id]["answers"]
    scores = {
        "Выносливость": 0, "Креативность": 0, "Гибкость": 0,
        "Ответственность": 0, "Стрессоустойчивость": 0,
        "Клиенты в день": 0, "Рабочие дни": 0
    }
    
    scoring_rules = {
        TestStates.Q1: {'A': {"Выносливость":7}, 'B': {"Выносливость":5}, 'C': {"Выносливость":-2}},
        TestStates.Q2: {'A': {"Выносливость":4}, 'B': {"Выносливость":2}, 'C': {"Выносливость":1}},
        TestStates.Q3: {'A': {"Креативность":5}, 'B': {"Креативность":7}, 'C': {"Креативность":-2}},
        TestStates.Q4: {'A': {"Креативность":4}, 'B': {"Креативность":2}, 'C': {"Креативность":1}},
        TestStates.Q5: {'A': {"Гибкость":-2}, 'B': {"Гибкость":3}, 'C': {"Гибкость":1}},
        TestStates.Q6: {'A': {"Гибкость":6}, 'B': {"Гибкость":3}, 'C': {"Гибкость":0}},
        TestStates.Q7: {'A': {"Ответственность":6}, 'B': {"Ответственность":3}, 'C': {"Ответственность":0}},
        TestStates.Q8: {'A': {"Ответственность":5}, 'B': {"Ответственность":1}, 'C': {"Ответственность":-3}},
        TestStates.Q9: {'A': {"Стрессоустойчивость":5}, 'B': {"Стрессоустойчивость":7}, 'C': {"Стрессоустойчивость":-2}},
        TestStates.Q10: {'A': {"Стрессоустойчивость":4}, 'B': {"Стрессоустойчивость":2}, 'C': {"Стрессоустойчивость":1}},
        TestStates.Q11: {'A': {"Клиенты в день":1}, 'B': {"Клиенты в день":3}, 'C': {"Клиенты в день":5}},
        TestStates.Q12: {'A': {"Рабочие дни":2}, 'B': {"Рабочие дни":4}, 'C': {"Рабочие дни":6}}
    }
    
    for state, answer in answers.items():
        for key, value in scoring_rules[state][answer].items():
            scores[key] += value

    # Фильтрация "Чилл гая"
    filtered_types = TYPES.copy()
    if scores["Выносливость"] < 2 or scores["Стрессоустойчивость"] < 1:
        del filtered_types["Чилл гай"]

    # Фильтрация "Мини-тату" при низкой ответственности
    filtered_types = TYPES.copy()
    if scores["Ответственность"] < 3:  # Если ответственность < 3
        del filtered_types["Мини-тату"]
    
    # Взвешенное сравнение
    weights = {"Выносливость": 1.0, "Стрессоустойчивость": 1.0, "Креативность": 1.0, "Гибкость": 1.0, "Ответственность": 1.0}
    best_match = None
    min_diff = float('inf')
    
    for type_name, params in filtered_types.items():
        diff = sum(
            abs(scores[k] - params[k]) * weights.get(k, 1)
            for k in ["Выносливость", "Креативность", "Гибкость", "Ответственность", "Стрессоустойчивость"]
        )
        diff += abs(scores["Клиенты в день"] - params["Клиенты в день"]) * 5
        diff += abs(scores["Рабочие дни"] - params["Рабочие дни"]) * 5
        
        if diff < min_diff:
            min_diff = diff
            best_match = type_name
    

    #Результаты в БД
    def save_test_result(user_id, best_match, scores):
        test_data = {
            "user_id": user_id,
            "test_date": datetime.now(),
            "best_match": best_match,
            "scores": scores
        }
        results_collection.insert_one(test_data)

    save_test_result(user_id, best_match, scores)

    await message.answer(
        f"Ваш тип: {best_match}!\n\n{DESCRIPTIONS[best_match]}\n\n"
        "чтобы пройти тест заново, нажмите /start \n"
        "если у тебя есть комментарии или пожелания оставь их тут @vlmsupport"
    )
    del user_data[user_id]

if __name__ == "__main__":
    dp.run_polling(bot)