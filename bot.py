import json

# Загружаем базу знаний
with open("../data/buildings.json", "r", encoding="utf-8") as f:
    buildings = json.load(f)

def find_building(question):
    question = question.lower()
    for info in buildings.values():
        # объединяем все ключевые слова для поиска
        keywords = [info["name"].lower()] + [s.lower() for s in info["services"]]
        # если хоть одно слово встречается в вопросе
        if any(word in question for word in keywords):
            return info
    return None

print("Бот: Привет! Я чат-бот навигации по кампусу Есенов Университета.")
print("Напиши 'выход' чтобы закрыть бот.")

while True:
    q = input("Студент: ").strip().lower()
    
    if q in ["выход", "exit", "quit"]:
        print("Бот: До встречи!")
        break

    # Если пользователь пишет привет
    if q in ["привет", "здравствуй", "hello", "hi"]:
        print("Бот: Привет! Я чат-бот навигации по кампусу Есенов Университета.")
        continue

    building = find_building(q)
    if building:
        print(f"Бот: {building['name']}\nОписание: {building['description']}\nУслуги: {', '.join(building['services'])}\nРасположение: {building['location']}")
    else:
        print("Бот: К сожалению, в базе данных нет информации по вашему запросу.")


