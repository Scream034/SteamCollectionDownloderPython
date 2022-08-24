from bs4 import BeautifulSoup
from requests import get

# Глобальные переменные
link: str = ''
language: int = 0
isAddictions: int
all_links: [] = []
all_id: [] = []
all_names: [] = []
all_addictions: [] = []

# запрашивает какой язык
language = int(input('Language?\n1 - Русский\n2 - English\n'))
if type(language) is not int:
    print('Error: Write numbers!')
    exit(0)
elif language != 1 and language != 2:
    print('Error: Write numbers that here!')
    exit(0)

# тут просто ссылку прошу
if language == 1:
    link = input('Ссылка?\n')
elif language == 2:
    link = input('link?\n')

# с зависимостями
if language == 1:
    isAddictions = int(input('С зависимостямии? (Долго)\n1 - да\n0 - нет\n'))
elif language == 2:
    isAddictions = int(input('With addictions? (of many time)\n1 - yes\n0 - no\n'))


# основа
site = get(link)
parse = BeautifulSoup(site.text, 'lxml')

# ищем
div = parse.find('div', class_='collectionChildren')
items = div.find_all('div', class_='collectionItem')

if items is not None:
    length = len(items)
else:
    if language == 2:
        print('Error: collection don\'t have items!')
    elif language == 1:
        print('Ошибка: коллекция не имеет предметов!')

# беру каждый элемент в коллекции
for index in range(length):
    item = items[index]
    all_links.append(item.find('a').attrs['href'])
    all_names.append(item.find('div', class_='workshopItemTitle').string)

# дальше, я беру id из ссылок
for index in range(length):
    link = all_links[index]
    all_id.append(link[link.find('id') + 3::])

# буду смотреть их зависимости
if isAddictions == 1:
    for index in range(length):
        item_site = get(all_links[index])
        item_parse = BeautifulSoup(item_site.text, 'lxml')

        item_div = item_parse.find('div', class_='responsive_local_menu')
        item_div_addiction = item_div.find('div', class_='requiredItemsContainer')

        if item_div_addiction != -1:
            for addiction in all_addictions:
                if addiction != item_div_addiction.text:
                    all_addictions.append(item_div_addiction.text)
                else:
                    continue
        else:
            continue

# записаваю всё в файл
with open('information.txt', 'w') as file:
    text = '//\n// author: paralax\n//\n'

    if language == 1:
        text += '// Незабудь login ! и путь !\n'
    elif language == 2:
        text += '// Do not forget login ! and path !\n'

    for index in range(length):
        id = all_id[index]
        name = all_names[index]
        text += f'workshop_download_item 294100 {id} // {name}\n'

    if len(all_addictions) != 0:
        if language == 1:
            text += '\n//\n// Зависимости:\n//\n\n'
            for index in range(length):
                addiction = all_addictions[index]
                text += f'// Зависимость: {addiction}\n'
        elif language == 2:
            text += '\n//\n// Addictions:\n//\n\n'
            for index in range(length):
                addiction = all_addictions[index]
                text += f'// Addiction: {addiction}\n'
    else:
        if isAddictions == 1:
            if language == 1:
                text += '// Зависмостей нет\n'
            elif language == 2:
                text += '// No addictions\n'
        else:
            if language == 1:
                text += '// Зависмости отключены\n'
            elif language == 2:
                text += '// Addictions off\n'

    file.write(text)
    file.close()

if language == 1:
    print('Отлично!')
elif language == 2:
    print('Good!')

