from pprint import pprint
import random
import math

# счетчик временных меток
TIMESTAMPS_COUNT = 50000

# почему 0.0001 ;d
PROBABILITY_SCORE_CHANGED = 0.0001

# 
PROBABILITY_HOME_SCORE = 0.45

# максимальный шаг 
OFFSET_MAX_STEP = 3

INITIAL_STAMP = {
    "offset": 0,  # временная метка указывающая на начало игры
    "score": {
        "home": 0, # кол-во очков у команды домашней?
        "away": 0  #  кол-во очков у команды гостей?
    }
}


def generate_stamp(previous_value):
    #  переменная возвращает True или False?
    #  где говорится что если рандомное число (в пределах 0.0 - 1.0)
    #  больше чем 1 - 0.0001 то есть практически невозможно
    score_changed = random.random() > 1 - PROBABILITY_SCORE_CHANGED

    # Если score_changed=True and  (1-0.45)> random.random
    home_score_change = 1 if score_changed and random.random() > 1 - \
        PROBABILITY_HOME_SCORE else 0
    # то есть если счет изменился то гостям добавляют 1 очко
    # но если у домашних поменялся счет то изменение гостей равно 0
    away_score_change = 1 if score_changed and not home_score_change else 0
    # math floor округляет в меньшую сторону или до кратного
    # basicly between numbers 1 and 2
    offset_change = math.floor(random.random() * OFFSET_MAX_STEP) + 1

    # тогда возвращаться будет просто словарь, в котором всегда будет меняться только 2 значения,
    #  будет прибавляться 1 или 2 к offset
    #  и 1 очко гостям или 1 очком домашним
    return {
        "offset": previous_value["offset"] + offset_change,
       "score": {
            "home": previous_value["score"]["home"] + home_score_change,
            "away": previous_value["score"]["away"] + away_score_change
        }
    }

# тут создается массив с набором словарей изменений игры
# то есть пока range > TIMESTAMPS_COUNT будем генерить словари
# то есть 50000 словарей


def generate_game():
    stamps = [INITIAL_STAMP, ]
    current_stamp = INITIAL_STAMP
    for _ in range(TIMESTAMPS_COUNT):
        current_stamp = generate_stamp(current_stamp)
        stamps.append(current_stamp)

    return stamps

# Мы вызываем функцию генерации игры внутри которой вызываем генерацию штампов
game_stamps = generate_game()

# pprint(game_stamps)

# принимает все штампы и offset
# возвращает результат игры на опредленное время
# значит ли это что функция отрабатывает все значения?
# смысл в том, что offset может изменяться либо на 1 либо на 2 поэтому на какой-то offset может не быть словаря
def get_score(game_stamps, offset):
    '''
        Takes list of game's stamps and time offset for which returns the scores for the home and away teams.
        Please pay attention to that for some offsets the game_stamps list may not contain scores.
    '''
    # Все временные штампы добавляются по возрастанию
    # Поэтому можно воспользоваться бинарным поиском
    # Сразу отсекаем варианты проверяя что offset не меньше и не больше
    # Первого и последнего элемента
    if offset < game_stamps[0]["offset"]:
        return None, None

    if offset > game_stamps[-1]["offset"]:
        return None, None

    left = 0
    right = len(game_stamps) - 1

    while left <= right:
        index_mid = (left + right) // 2
        mid_offset = game_stamps[index_mid]["offset"]
        scores_homes = game_stamps[index_mid]["score"]["home"]
        scores_away = game_stamps[index_mid]["score"]["away"]
        # offset=target
        if mid_offset == offset:
            return scores_homes, scores_away
        # target > mid value going to right part of game_stamps
        elif mid_offset < offset:
            left = index_mid + 1
        # move to left
        else:
            right = index_mid - 1
    return None, None


# result = get_score(game_stamps, 'qeqe')
# print(result)

# result = get_score(game_stamps, 130550)
# print(result)

# result = get_score(game_stamps, -1)
# print(result)

