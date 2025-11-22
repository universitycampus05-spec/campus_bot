import json

# Загружаем базу знаний
with open("../data/buildings.json", "r", encoding="utf-8") as f:
    buildings = json.load(f)

# Словари приветствий и команд
greetings = {
    "ru": ["привет", "здравствуй"],
    "kz": ["сәлем", "сәлеметсіз бе"],
    "en": ["hello", "hi"]
}

goodbyes = {
    "ru": ["выход", "пока", "quit", "exit"],
    "kz": ["шық", "қош бол", "exit", "quit"],
    "en": ["exit", "quit", "bye"]
}

responses = {
    "greeting": {
        "ru": "Привет! Я чат-бот навигации по кампусу Есенов Университета.",
        "kz": "Сәлем! Мен Есенов университетінің кампусы бойынша чат-ботпын.",
        "en": "Hello! I am the navigation chatbot for Yesenov University campus."
    },
    "no_info": {
        "ru": "К сожалению, я не нашёл информации по вашему запросу.",
        "kz": "Өкінішке орай, мен сіздің сұранысыңыз бойынша ақпарат таппадым.",
        "en": "Sorry, I could not find any information for your query."
    },
    "farewell": {
        "ru": "До встречи!",
        "kz": "Көріскенше!",
        "en": "See you!"
    }
}

def detect_language(text):
    text = text.lower()
    for lang, words in greetings.items():
        if any(word in text for word in words):
            return lang
    for lang, words in goodbyes.items():
        if any(word in text for word in words):
            return lang
    # По умолчанию русский
    return "ru"

def find_building(question):
    question = question.lower()
    for info in buildings.values():
        # объединяем ключевые слова на всех языках
        keywords = [info["name"].lower()]
        for lang_services in info["services"].values():
            keywords += [s.lower() for s in lang_services]
        if any(word in question for word in keywords):
            return info
    return None

# Приветствие при запуске
print("Бот: " + responses["greeting"]["ru"])
print("Напиши 'выход' чтобы закрыть бот.")

while True:
    q = input("Студент: ").strip().lower()
    
    lang = detect_language(q)  # Определяем язык запроса
    
    # Проверка на команды выхода
    if q in goodbyes.get(lang, []):
        print("Бот: " + responses["farewell"][lang])
        break

    # Проверка на приветствие
    if q in greetings.get(lang, []):
        print("Бот: " + responses["greeting"][lang])
        continue

    # Поиск здания
    building = find_building(q)
    if building:
        name = building["name"]
        description = building["description"].get(lang, building["description"]["ru"])
        services = ", ".join(building["services"].get(lang, building["services"]["ru"]))
        location = building["location"]
        print(f"Бот: {name}\nОписание: {description}\nУслуги: {services}\nРасположение: {location}")
    else:
        print("Бот: " + responses["no_info"][lang])

