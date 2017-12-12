import numpy as np
import random
import threading
import sys
import select

import letters
import figures
    
def timeout():
    print("\nTemps écoulé!\n")

def run(nb_set, repartition, letter_chrono=30, figure_chrono=40):
    """Main program: play nb_set times a set of x figure draw(s) and y letter
    draw(s), repartition giving how y is being larger than x 
    
    """ 
    random.seed(123)
    results = []
    scores = []
    for i in range(1, 1+nb_set):
        for i in range(1, 1+repartition):
            nb_voyels = random.randint(2,8)
            cur_letter_game = letters.letter_game(nb_voyels, 15)
            results.append(cur_letter_game[0])
            scores.append(cur_letter_game[1])
        cur_figure_game = figures.figure_game(15)
        results.append(cur_figure_game[0])
        scores.append(cur_figure_game[1])
    print("Votre feuille de résultats: {0}".format(results))
    print("Vous avez marqué un total de {0} points durant cette partie!".format(sum(scores)))

if __name__ == '__main__':
    run(1, 2)
