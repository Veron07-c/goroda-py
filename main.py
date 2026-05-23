#ИМПОРТ: подключаем модули и встроенную библиотеку random
import random
import data_manager
import computer_ai
import validator
import utils

#ПОДГОТОВКА к игре
def main():
    all_cities = {city.lower() for city in data_manager.load_cities()} #загрузка базы данных
    used_cities = set() #создание списка для использованных городов

    #приветствие игрока и объяснение правил
    print("ДОБРО ПОЖАЛОВАТЬ В ИГРУ 'ГОРОДА'!")
    print("Правила: Чтобы завершить игру в любой момент, введите 'выход'.")

    #первый ход компьютера
    first_comp_city = random.choice(list(all_cities))
    used_cities.add(first_comp_city)
    print(f"Компьютер делает первый ход: {first_comp_city.capitalize()}")

    #вычисление буквы для игрока
    current_letter = utils.get_next_letter(first_comp_city)
    #флаг, который управляет бесконечным циклом
    game_over = False

    #СТАРТ игры
    while not game_over:
        #проверка на тупик: проверяем, есть ли вообще города для игрока
        test_move = computer_ai.get_computer_move(current_letter, all_cities, used_cities)

        if test_move is None:
            print(f"\nНа букву '{current_letter.upper()}' больше нет свободных городов в базе!")
            print("ПОЗДРАВЛЯЕМ! Вы победили, так как городов на эту букву не осталось.")
            game_over = True
            continue

        #ход игрока
        print(f"\nВаш ход! Введите город на букву: '{current_letter.upper()}'")
        user_input = input("Вы: ")

        #проверка на "выход"
        if user_input.strip().lower() == "выход":
            print("\nВы сдались. Игра завершена!")
            break

        # проверка по правилам
        is_valid, error_message = validator.validate_player_move(
            user_input, current_letter, all_cities, used_cities
        )

        if not is_valid:
            #если нарушено хоть одно условие, выводим ошибку и пропускаем ход компьютера
            print(f"Ошибка: {error_message}")
            continue  #возвращает цикл в начало (игрок пробует снова)

        #если всё верно, фиксируем ход игрока
        player_city = user_input.strip().lower()
        used_cities.add(player_city)

        #вычисление буквы для компьютера
        current_letter = utils.get_next_letter(player_city)

        #ход компьютера
        print("\nКомпьютер думает...")

        #поиск города для ответа: передаем букву, общую базу и список уже названных городов
        comp_city = computer_ai.get_computer_move(current_letter, all_cities, used_cities)

        #проверка на капитуляцию компьютера
        if comp_city is None:  # Если функция ИИ вернула None, значит городов нет
            print("У компьютера закончились слова! Вы победили!")
            game_over = True
            continue

        #если компьютер нашел город, выводим его
        print(f"Компьютер называет: {comp_city.capitalize()}")
        used_cities.add(comp_city)

        #расчет буквы для следующего хода игрока
        current_letter = utils.get_next_letter(comp_city)

    #ФИНАЛ игры
    print("Спасибо за игру! До новых встреч!")

if __name__ == "__main__":
    main()