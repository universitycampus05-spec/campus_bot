import os
import json
from fastapi import FastAPI
from fastapi.responses import HTMLResponse

# ----------------------------
# Пути к файлам (в корне)
# ----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "buildings.json")
HTML_PATH = os.path.join(BASE_DIR, "chat_widget.html")

# ----------------------------
# Загружаем базу знаний
# ----------------------------
if not os.path.exists(DATA_PATH):
    raise FileNotFoundError(f"Файл базы данных не найден: {DATA_PATH}")

with open(DATA_PATH, "r", encoding="utf-8") as f:
    buildings = json.load(f)

# ----------------------------
# Функция поиска по базе
# ----------------------------
def find_building(question):
    question = question.lower()
    for info in buildings.values():
        keywords = [info["name"].lower()] + [s.lower() for s in info["services"]]
        for word in keywords:
            if word in question:
                return info
    return None

# ----------------------------
# Создаём FastAPI приложение
# ----------------------------
app = FastAPI()

# ----------------------------
# Эндпоинт для HTML виджета
# ----------------------------
@app.get("/", response_class=HTMLResponse)
async def chat_page():
    if not os.path.exists(HTML_PATH):
        return "<h1>Файл chat_widget.html не найден</h1>"
    with open(HTML_PATH, "r", encoding="utf-8") as f:
        return f.read()

# ----------------------------
# Эндпоинт для обработки вопросов
# ----------------------------
@app.get("/ask")
async def ask(question: str):
    building = find_building(question)
    if building:
        return (
            f"{building['name']}. {building['description']}. "
            f"Услуги: {', '.join(building['services'])}. "
            f"Расположение: {building['location']}"
        )
    else:
        return "К сожалению, в базе данных нет информации по вашему запросу."
