import random

def get_computer_move(current_letter, all_cities, used_cities):
    filtred_cities = []
    for city in all_cities:
        if city not in used_cities and current_letter == city[0]:
            filtred_cities.append(city)
    if len(filtred_cities) == 0:
        return None
    else:
        return random.choice(filtred_cities)