import datetime
import numpy as np
import random
import threading
import sys
import select

NUMBERS = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 25,
           50, 75, 100]

def figure_picking():
    """Return of list of six numbers, and a result that must be reached with
    these six numbers

    """
    random.seed(datetime.datetime.now())
    number_list = random.sample(NUMBERS, 6)
    result = random.sample(range(1000), 1)
    return (number_list, *result)

def figure_game(time):
    """ Run a figure game: choose randomly six number and one target between
    100 and 999; there is time seconds to find the exact result
    """
    print("***")
    draw = figure_picking()
    print("Vous devez trouver {1}, avec: {0}".format(draw[0], draw[1]))
    i, o, e = select.select([sys.stdin], [], [], time)
    if i:
        account = int(sys.stdin.readline())
    else:
        account = 0
    score = compute_figure_score(draw[1], account)
    print("Votre résultat est : {0}, vous marquez {1} points"
          .format(account, score))
    return (account, score)

def compute_figure_score(target, result):
    """ Compute the score corresponding to the found result, knowing that
    target was supposed to be found
    """
    if target == result:
        return 10
    elif abs(target - result) == 1:
        return 8
    elif abs(target - result) == 2:
        return 7
    elif abs(target - result) == 3:
        return 6
    elif abs(target - result) == 4:
        return 5
    elif 5 <= abs(target - result) <= 6:
        return 4
    elif 7 <= abs(target - result) <= 8:
        return 3
    elif 9 <= abs(target - result) <= 10:
        return 2
    elif abs(target - result) <= 100:
        return 1
    else:
        return 0

