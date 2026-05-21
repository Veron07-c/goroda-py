import requests
from pathlib import Path

# Путь к файлу с городами в той же папке, что и скрипт
CITIES_FILE = Path('cities.txt')

def load_cities(file_path=CITIES_FILE):
    # Создано пустое множество для хранения городов
    cities = set()
    # Если файла нет, возвращено пустое множество
    if not file_path.exists():
        return cities
    try:
        # Открыт файл для чтения с кодировкой UTF-8
        with open(file_path, 'r', encoding='utf-8') as f:
            # Прочитан файл построчно
            for line in f:
                # Убраны пробелы и переносы строк
                city = line.strip()
                # Если строка не пустая, добавлена во множество
                if city:
                    cities.add(city)
    # Если любая ошибка, просто пропущена
    except Exception:
        pass
    # Возвращено множество с городами
    return cities

def parse_and_save_cities(url=None, output_path=CITIES_FILE):
    # Если ссылка не передана, использована страница городов России
    if url is None:
        url = "https://ru.wikipedia.org/wiki/Список_городов_России"
    try:
        # Импортированы библиотеки внутри функции
        import bs4
        import re
        # Отправлен GET-запрос к странице
        response = requests.get(url, timeout=10)
        # Проверен статус ответа
        response.raise_for_status()
        # Создан объект для разбора HTML
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        # Создано пустое множество для городов
        cities = set()
        # Найдены все таблицы с классом wikitable
        for table in soup.select('table.wikitable'):
            # Перебраны строки таблицы
            for row in table.select('tr'):
                # Найдены ячейки в строке
                cells = row.select('td')
                if cells:
                    # Взята первая ячейка с названием города
                    city_cell = cells[0]
                    # Извлечён текст из ячейки
                    city_text = city_cell.get_text(separator=' ', strip=True)
                    # Удалено содержимое скобок
                    city_text = re.sub(r'\s*\(.*?\)', '', city_text)
                    # Взята первая часть до запятой
                    city_text = city_text.split(',')[0].strip()
                    # Проверено, что текст не пустой, длиннее 1 символа и не начинается с цифры
                    if city_text and len(city_text) > 1 and not city_text[0].isdigit():
                        cities.add(city_text)
        # Открыт файл для записи
        with open(output_path, 'w', encoding='utf-8') as f:
            # Записаны города в алфавитном порядке
            for city in sorted(cities):
                f.write(city + '\n')
        return True
    # Обработаны все возможные ошибки
    except Exception:
        return False

if __name__ == '__main__':
    all_cities = load_cities()

