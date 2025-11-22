import json

# Загружаем базу знаний
with open("../data/buildings.json", "r", encoding="utf-8") as f:
    buildings = json.load(f)

# Словари приветствий и команд (можно расширять)
greetings = {
    "ru": ["привет", "здравствуй", "добрый", "здарова"],
    "kz": ["сәлем", "сәлеметсіз бе", "сәле́м"],
    "en": ["hello", "hi", "hey"]
}

goodbyes = {
    "ru": ["выход", "пока", "прощай", "quit", "exit"],
    "kz": ["шық", "қош бол", "келесі кездесу", "exit", "quit"],
    "en": ["exit", "quit", "bye", "goodbye"]
}

responses = {
    "greeting": {
        "ru": "Привет! Я чат-бот навигации по кампусу Есенов Университета.",
        "kz": "Сәлем! Мен Есенов университетінің кампусы бойынша чат-ботпын.",
        "en": "Hello! I am the navigation chatbot for Yesenov University campus."
    },
    "no_info": {
        "ru": "К сожалению, я не нашёл информации по вашему запросу. Попробуйте указать название здания или услугу.",
        "kz": "Өкінішке орай, мен сіздің сұранысыңыз бойынша ақпарат таппадым. Ғимараттың атын немесе қызметін нақтылаңыз.",
        "en": "Sorry, I could not find any information for your query. Try specifying the building name or a service."
    },
    "farewell": {
        "ru": "До встречи!",
        "kz": "Көріскенше!",
        "en": "See you!"
    }
}

def detect_language(text):
    """Попытка определить язык по ключевым словам-приветствиям/прощаниям."""
    text = text.lower()
    # Сначала по приветствиям
    for lang, words in greetings.items():
        if any(word in text for word in words):
            return lang
    # По прощаниям
    for lang, words in goodbyes.items():
        if any(word in text for word in words):
            return lang
    # Если ничего не найдено — попробуем угадать по английским ключевым словам в базе:
    # (например, 'library', 'cafeteria' -> английский)
    eng_markers = ["library", "cafeteria", "building", "admin", "faculty"]
    if any(m in text for m in eng_markers):
        return "en"
    # По умолчанию — русский
    return "ru"

def normalize_name_field(name_field):
    """
    Возвращает словарь с языками из поля name.
    Если name_field — строка, вернём {'ru': name_field}
    Если dict — вернём его (ожидаем ключи ru/kz/en или похожие).
    """
    if isinstance(name_field, str):
        return {"ru": name_field}
    if isinstance(name_field, dict):
        return name_field
    # прочие варианты
    return {"ru": str(name_field)}

def gather_keywords(info):
    """
    Возвращает список ключевых слов для поиска у одного здания,
    учитывая имена и services во всех языках и локацию.
    """
    keywords = []
    # name может быть строкой или dict
    name_field = info.get("name", "")
    name_dict = normalize_name_field(name_field)
    for v in name_dict.values():
        keywords.append(str(v).lower())

    # services — может быть dict {ru:[...], kz:[...], en:[...]} или список
    services_field = info.get("services", {})
    if isinstance(services_field, dict):
        for lang_services in services_field.values():
            if isinstance(lang_services, list):
                keywords += [s.lower() for s in lang_services]
            elif isinstance(lang_services, str):
                keywords.append(lang_services.lower())
    elif isinstance(services_field, list):
        keywords += [s.lower() for s in services_field]
    elif isinstance(services_field, str):
        keywords.append(services_field.lower())

    # location (строка) добавим тоже
    loc = info.get("location", "")
    if isinstance(loc, str) and loc:
        keywords.append(loc.lower())

    # уберём пустые элементы и дубликаты
    return list({k for k in keywords if k})

def find_building(question):
    q = question.lower()
    for info in buildings.values():
        keywords = gather_keywords(info)
        # Ищем любое вхождение ключевого слова в вопрос (чтобы не требовать точного равенства)
        if any(kw in q for kw in keywords):
            return info
    return None

# Стартовое приветствие (показываем все три языка, чтобы пользователь понял)
print("Бот: " + responses["greeting"]["ru"])
print("Бот: " + responses["greeting"]["kz"])
print("Бот: " + responses["greeting"]["en"])
print("Напиши 'выход' чтобы закрыть бот.")

while True:
    q_original = input("Студент: ").strip()
    if not q_original:
        continue
    q = q_original.lower()

    lang = detect_language(q)

    # Проверка на команды выхода (не требуем точного равенства — допустимое вхождение)
    if any(word in q for word in goodbyes.get(lang, [])):
        print("Бот: " + responses["farewell"][lang])
        break

    # Проверка на приветствие (вхождение)
    if any(word in q for word in greetings.get(lang, [])):
        print("Бот: " + responses["greeting"][lang])
        continue

    # Поиск здания
    building = find_building(q)
    if building:
        # Имя: поддерживаем случай, когда name — dict с переводами
        name_field = building.get("name", "")
        name_dict = normalize_name_field(name_field)
        name = name_dict.get(lang, name_dict.get("ru", next(iter(name_dict.values()))))

        description_field = building.get("description", {})
        # description может быть dict или строка
        if isinstance(description_field, dict):
            description = description_field.get(lang, description_field.get("ru", ""))
        else:
            description = str(description_field)

        services_field = building.get("services", {})
        if isinstance(services_field, dict):
            services_list = services_field.get(lang, services_field.get("ru", []))
        elif isinstance(services_field, list):
            services_list = services_field
        else:
            services_list = [str(services_field)]

        services = ", ".join(services_list) if services_list else "—"

        location = building.get("location", "—")
        print(f"Бот: {name}\nОписание: {description}\nУслуги: {services}\nРасположение: {location}")
    else:
        print("Бот: " + responses["no_info"][lang])

