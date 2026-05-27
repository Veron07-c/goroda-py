import requests
from pathlib import Path

CITIES_FILE = Path('cities.txt')

def load_cities(file_path=CITIES_FILE):
    cities = set()
    # Если файла нет, возвращено пустое множество
    if not file_path.exists():
        return cities
    try:
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
    return cities
    
def parse_and_save_cities(url=None, output_path=CITIES_FILE):
    if url is None:
        url = "https://ru.wikipedia.org/wiki/Список_городов_России"
    try:
        import bs4
        import re

        # Заголовок User-Agent, чтобы Википедия не заблокировала запрос
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }

        response = requests.get(url, timeout=10, headers=headers)
        response.raise_for_status()
        soup = bs4.BeautifulSoup(response.text, 'html.parser')
        cities = set()

        all_tables = soup.find_all('table')
        tables_with_cities = 0  # Счётчик таблиц с городами, чтобы не собирать мусор из навигации

        for table in all_tables:
            header_row = table.find('tr')
            if not header_row:
                continue

            th_cells = header_row.find_all('th')
            city_col_index = None

            # Ищет столбец, в котором заголовок содержит слово "Город"
            for idx, th in enumerate(th_cells):
                if 'Город' in th.get_text():
                    city_col_index = idx
                    break

            if city_col_index is None:
                continue

            tables_with_cities += 1
            # Берёт только первые две таблицы с городами — основную и ГФЗ
            if tables_with_cities > 2:
                break

            for row in table.find_all('tr'):
                cells = row.find_all('td')
                if len(cells) > city_col_index:
                    city_cell = cells[city_col_index]
                    city_text = city_cell.get_text(separator=' ', strip=True)
                    # Удаляет пояснения в скобках, например "Москва (столица)" -> "Москва"
                    city_text = re.sub(r'\s*\(.*?\)', '', city_text)
                    # Берёт часть до запятой, если есть уточнение
                    city_text = city_text.split(',')[0].strip()
                    if city_text and len(city_text) > 1 and not city_text[0].isdigit():
                        cities.add(city_text)

        if not cities:
            return False

        with open(output_path, 'w', encoding='utf-8') as f:
            for city in sorted(cities):
                f.write(city + '\n')

        return True

    except Exception:
        return False

if __name__ == '__main__':
    all_cities = load_cities()
