import json

# Загружаем базу знаний
with open("../data/buildings.json", "r", encoding="utf-8") as f:
    buildings = json.load(f)


def gather_keywords(info):
    """
    Собирает ключевые слова для поиска по зданию:
    имя, услуги, описание, локация.
    Без языков!
    """
    keywords = []

    # Имя (может быть строка или dict)
    name_field = info.get("name", "")
    if isinstance(name_field, dict):
        for v in name_field.values():
            keywords.append(str(v).lower())
    else:
        keywords.append(str(name_field).lower())

    # description
    desc = info.get("description", "")
    if isinstance(desc, dict):
        for v in desc.values():
            keywords.append(str(v).lower())
    else:
        keywords.append(str(desc).lower())

    # services
    services_field = info.get("services", [])
    if isinstance(services_field, dict):
        for sv in services_field.values():
            if isinstance(sv, list):
                keywords += [s.lower() for s in sv]
            else:
                keywords.append(str(sv).lower())
    elif isinstance(services_field, list):
        keywords += [s.lower() for s in services_field]
    else:
        keywords.append(str(services_field).lower())

    # location
    loc = info.get("location", "")
    if isinstance(loc, str):
        keywords.append(loc.lower())

    # убираем пустые и дубликаты
    return list({k for k in keywords if k})


def find_building(question):
    q = question.lower()
    for info in buildings.values():
        keywords = gather_keywords(info)
        if any(kw in q for kw in keywords):
            return info
    return None


print("Бот запущен. Введите запрос о здании кафедре, услуге или месте.")

while True:
    q = input("Студент: ").strip()
    if not q:
        continue
    if q.lower() in ["выход", "exit", "quit"]:
        print("Бот завершён.")
        break

    building = find_building(q)
    if building:
        # Имя
        name_field = building.get("name", "")
        if isinstance(name_field, dict):
            name = next(iter(name_field.values()))
        else:
            name = name_field

        # Описание
        desc_field = building.get("description", "")
        if isinstance(desc_field, dict):
            desc = next(iter(desc_field.values()))
        else:
            desc = desc_field

        # Услуги
        services_field = building.get("services", [])
        if isinstance(services_field, dict):
            sv = next(iter(services_field.values()))
            services = ", ".join(sv) if isinstance(sv, list) else str(sv)
        elif isinstance(services_field, list):
            services = ", ".join(services_field)
        else:
            services = str(services_field)

        location = building.get("location", "—")

        print(f"\nНазвание: {name}")
        print(f"Описание: {desc}")
        print(f"Услуги: {services}")
        print(f"Расположение: {location}\n")

    else:
        print("Информация не найдена. Уточните запрос.\n")


