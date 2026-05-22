def validate_player_move(user_input, current_letter, all_cities, used_cities):
    city = user_input.strip().lower()  # нормализация данных ввода

    if not city:  # пустой ввод
        return False, "введите название города"

    if len(city) < 2:  # проверка на короткое название
        return False, "название слишком короткое"

    if city[0] != current_letter:  # проверка первой буквы
        return False, f"нужна буква '{current_letter.upper()}'"

    if city not in all_cities:  # наличие в базе городов
        return False, "город не найден в базе"

    if city in used_cities:  # повторное использование названия
        return False, "город уже называли"

    return True, city # проверка пройдена