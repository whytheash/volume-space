import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from telegram.ext import Updater
import os

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
    "Чилл гай": "Мастер-медитатор! Твоя студия — дзен-сад. Совет: купи новый блокнот!",
    "Тру артист": "Фанат своего дела! Клиенты ждут годами. Не забывай поесть!",
    "Неформал": "Творишь как вихрь! Добавь немного структуры!",
    "Блэкворкер": "Мастер мрачных шедевров! Выходи иногда на солнце!",
    "Коммерческий": "Тату-конвейер! Добавь креатива в рутину!",
    "Опоздун": "Гений с опозданиями! Заведи будильник!",
    "Реальный хард": "Робот-татуировщик! Людям нужно внимание!",
    "В тихом омуте": "Мастер-ниндзя! Показывайся в соцсетях!",
    "Мини-тату": "Мастер миниатюр! Попробуй большой формат!",
    "Ночная бабочка": "Творец ночи! Выспись хоть раз!",
    "Только начал": "Росток таланта! Больше практики!"
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
        "1. Как реагируете на 5 клиентов подряд?",
        ["A. Беру энергетик и в бой!", "B. Соглашусь, но потом вырублюсь", "C. Откажусь — качество важнее"]
    ),
    TestStates.Q2: (
        "2. Друг зовет в поход после работы:",
        ["A. Пойду — природа восстановит силы!", "B. Только в гамаке с книжкой", "C. Останусь дома рисовать эскизы"]
    ),
    TestStates.Q3: (
        "3. Клиент хочет «космического кота»:",
        ["A. Создам 3D-шедевр с неоном!", "B. Предложу что-то попроще", "C. Придумаем новую концепцию!"]
    ),
    TestStates.Q4: (
        "4. Отношение к трендам:",
        ["A. Беру шаблоны — это быстро!", "B. Иногда вдохновляюсь", "C. Творю вне времени и трендов!"]
    ),
    TestStates.Q5: (
        "5. Клиент перенес сеанс за 2 часа:",
        ["A. Без проблем — займусь своими делами!", "B. Разозлюсь, но промолчу", "C. Больше не буду с ним работать"]
    ),
    TestStates.Q6: (
        "6. Нужно сменить стиль:",
        ["A. Научусь за ночь и сделаю!", "B. Мой стиль — ищите другого мастера!", "C. Попробую, но это эксперимент"]
    ),
    TestStates.Q7: (
        "7. Клиент жалуется на заживление:",
        ["A. Бесплатно исправлю и помогу!", "B. Это его вина — не ухаживал!", "C. Некогда разбираться"]
    ),
    TestStates.Q8: (
        "8. Подготовка к сеансу:",
        ["A. За день стерилизую всё!", "B. В день сеанса: 'Где машинка?'", "C. Клиент придет — тогда подготовлюсь"]
    ),
    TestStates.Q9: (
        "9. Клиент плачет от боли:",
        ["A. Успокою и сделаю перерыв!", "B. 'Красота требует жертв!'", "C. Сама запаникую"]
    ),
    TestStates.Q10: (
        "10. Сорвались 3 клиента:",
        ["A. Пожалуюсь в Stories", "B. Ищу новых и делаю скидки!", "C. Хочу бросить тату-сферу"]
    ),
    TestStates.Q11: (
        "11. Идеальный график:",
        ["A. 1-2 клиента — не спеша", "B. 3-4 клиента — золотая середина", "C. 5+ клиентов — работаю на потоке"]
    ),
    TestStates.Q12: (
        "12. Рабочие дни в неделю:",
        ["A. 1-2 дня — нужен отдых!", "B. 3-4 дня — баланс работы и жизни", "C. 5-7 дней — работаю без остановки"]
    )
}

user_data = {}

@dp.message(Command("start"))
async def start_test(message: types.Message, state: FSMContext):

    # #Внесение пользователя в БД
    # user = message.from_user
    # registration_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # # Запись в users_data
    # users_sheet.append_row([
    #     user.id,
    #     user.username if user.username else "N/A",
    #     user.first_name if user.first_name else "N/A",
    #     user.last_name if user.last_name else "N/A",
    #     registration_date
    # ])


    await message.answer("Ответь на 12 вопросов, чтобы узнать свой тип тату-мастера!")
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
        TestStates.Q1: {'A': {"Выносливость":5, "Стрессоустойчивость":2}, 'B': {"Выносливость":2, "Стрессоустойчивость":-1}, 'C': {"Выносливость":-3, "Стрессоустойчивость":-3}},
        TestStates.Q2: {'A': {"Выносливость":3, "Стрессоустойчивость":1}, 'B': {"Стрессоустойчивость":-2, "Креативность":1}, 'C': {"Креативность":2}},
        TestStates.Q3: {'A': {"Креативность":3}, 'B': {"Креативность":1}, 'C': {"Гибкость":3}},
        TestStates.Q4: {'A': {"Креативность":-1}, 'B': {"Креативность":1}, 'C': {"Креативность":2}},
        TestStates.Q5: {'A': {"Гибкость":2}, 'B': {"Гибкость":-1}, 'C': {"Гибкость":-2}},
        TestStates.Q6: {'A': {"Гибкость":3}, 'B': {"Гибкость":-2}, 'C': {"Гибкость":1}},
        TestStates.Q7: {'A': {"Ответственность":3}, 'B': {"Ответственность":-2}, 'C': {"Ответственность":-3}},
        TestStates.Q8: {'A': {"Ответственность":2}, 'B': {"Ответственность":-1}, 'C': {"Ответственность":-2}},
        TestStates.Q9: {'A': {"Стрессоустойчивость":2}, 'B': {"Стрессоустойчивость":-1}, 'C': {"Стрессоустойчивость":-2}},
        TestStates.Q10: {'A': {"Стрессоустойчивость":-2}, 'B': {"Стрессоустойчивость":2}, 'C': {"Стрессоустойчивость":-3}},
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
    

    # # Запись в test_results
    # test_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # results_sheet.append_row([
    #     user_id,
    #     test_date,
    #     best_match,
    #     str(scores)  # Сохраняем баллы в виде JSON-строки
    # ])


    await message.answer(
        f"Ваш тип: {best_match}!\n\n{DESCRIPTIONS[best_match]}\n\n"
        "Чтобы пройти тест заново, нажмите /start"
    )
    del user_data[user_id]

if __name__ == "__main__":
    dp.run_polling(bot)