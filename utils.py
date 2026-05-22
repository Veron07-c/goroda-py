def get_next_letter(city):
    # 1. На всякий случай переводим строку в нижний регистр и убираем пробелы
    city_clean = city.strip().lower()
    # 2. Берем самую последнюю букву с помощью отрицательного индекса [-1]
    last_letter = city_clean[-1]
    # 3. Создаем множество букв, на которые названия городов не существует
    bad_letters = {'ь', 'ы', 'ъ'}
    # 4. Проверка последней буквы
    if last_letter in bad_letters:
        # Если буква не подходит, берем предпоследнюю букву через индекс [-2]
        next_letter = city_clean[-2]
    else:
        # Если буква нормальная, она и становится целевой
        next_letter = last_letter
    return next_letter
