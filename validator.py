def validate_player_move(user_input, current_letter, all_cities, used_cities):
    city = user_input.strip().lower()  # нормализация данных ввода

    if not city:  # пустой ввод
        return False, "Ошибка: введите название города", None

    if len(city) < 2:  # проверка на короткое название
        return False, "Ошибка: название слишком короткое", None

    if city == "выход":  # проверка на выход из игры
        return False, "Игра завершена", None

    if city[0] != current_letter:  # проверка первой буквы
        return False, f"Ошибка: нужна буква '{current_letter.upper()}'", None

    if city not in all_cities:  # наличие в базе городов
        return False, "Ошибка: город не найден в базе", None

    if city in used_cities:  # повторное использование названия
        return False, "Ошибка: город уже называли", None

    return True, city, None  # проверка пройдена