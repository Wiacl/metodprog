import requests
import matplotlib.pyplot as plt

base_url = 'https://pokeapi.co/api/v2/'
limit = 10
url = f'{base_url}pokemon?limit={limit}'

response = requests.get(url)
pokemon_list = response.json()['results']

data = []  # список для хранения информации о покемонах

for pokemon in pokemon_list:
    pokemon_url = pokemon['url']
    pokemon_data = requests.get(pokemon_url).json()

    # словарь с характеристиками покемона
    pokemon_info = {
        'id': pokemon_data['id'],
        'name': pokemon_data['name'],
        'height': pokemon_data['height'],
        'weight': pokemon_data['weight'],
        'hp': pokemon_data['stats'][0]['base_stat'],
        'attack': pokemon_data['stats'][1]['base_stat'],
        'defense': pokemon_data['stats'][2]['base_stat']
    }

    data.append(pokemon_info)

names = [p['name'] for p in data]
heights = [p['height'] for p in data]
weights = [p['weight'] for p in data]
hp = [p['hp'] for p in data]
attack = [p['attack'] for p in data]
defense = [p['defense'] for p in data]

# 1. Линейный график (HP)
plt.figure()
plt.plot(names, hp, marker='o')
plt.title('HP покемонов')
plt.xlabel('Покемон')
plt.ylabel('HP')
plt.xticks(rotation=45)
plt.grid()
plt.show()

# 2. Точечная диаграмма (Рост vs Вес)
plt.figure()
plt.scatter(heights, weights)
for i in range(len(names)):
    plt.annotate(
        names[i],                 # текст (имя покемона)
        (heights[i], weights[i]), # координаты точки
        textcoords="offset points",
        xytext=(5, 5),             # смещение текста
        fontsize=9
    )
plt.title('Зависимость веса от роста')
plt.xlabel('Рост')
plt.ylabel('Вес')
plt.grid()
plt.show()

# 3. Столбчатая диаграмма (Атака)
plt.figure()
plt.bar(names, attack)
plt.title('Атака покемонов')
plt.xlabel('Покемон')
plt.ylabel('Атака')
plt.xticks(rotation=45)
plt.show()

# 4. Горизонтальная столбчатая диаграмма (Защита)
plt.figure()
plt.barh(names, defense)
plt.title('Защита покемонов')
plt.xlabel('Защита')
plt.ylabel('Покемон')
plt.show()

# 5. Гистограмма (Вес)
plt.figure()
plt.hist(weights, bins=10)
plt.title('Распределение веса покемонов')
plt.xlabel('Вес')
plt.ylabel('Количество')
plt.show()
