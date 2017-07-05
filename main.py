import numpy as np
import random
import threading
import sys
import select

# The conson and voyel lists contain duplicate versions of each letters
# The frequency corresponds to the Scrabble letter repartition
# see e.g. https://fr.wikipedia.org/wiki/Lettres_du_Scrabble
# B*2, C*2, D*3, F*2, G*2, H*2, J*1, K*1, L*5, M*3, N*6, P*2, R*6, S*6, T*6
# V*2, W*1, X*1, Z*1
CONSONS = ['B', 'B', 'C', 'C', 'D', 'D', 'D', 'F', 'F', 'G', 'G', 'H',
           'H', 'J', 'K', 'L', 'L', 'L', 'L', 'L', 'M', 'M', 'M', 'N',
           'N', 'N', 'N', 'N', 'N', 'P', 'P', 'R', 'R', 'R', 'R', 'R', 'R',
           'S', 'S', 'S', 'S', 'S', 'S', 'T', 'T', 'T', 'T', 'T', 'T', 'V',
           'V', 'W', 'X', 'Z']
# A*9, E*15, I*8, O*6, U*6
VOYELS = ['A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'A', 'E', 'E', 'E', 'E', 'E',
           'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'E', 'I', 'I', 'I',
           'I', 'I', 'I', 'I', 'I', 'O', 'O', 'O', 'O', 'O', 'O', 'U', 'U',
           'U', 'U', 'U', 'U', 'Y']

NUMBERS = [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9, 10, 10, 25,
           50, 75, 100]

random.seed(123)

def letter_picking(nb_voyels=0):
    """Return a list of ten letters, this list must be composed o  `nb_voyels` voyels

    Parameters
    ----------
    nb_voyels: integer
        Number of desired voyels (between 2 and 8)
    
    """
    letter_list = np.repeat(0, 10)
    try:
        if nb_voyels < 2 or nb_voyels > 8:
            raise ValueError("Wrong nb_voyels value")
    except ValueError as verr:
        print("{0}: the number of voyels must be comprised between 2 and 8!".format(verr))
        raise
    letter_list  = list(np.random.choice(VOYELS, nb_voyels))
    letter_list = letter_list + list(np.random.choice(CONSONS, 10-nb_voyels))
    random.shuffle(letter_list)
    return ''.join(letter_list)

def figure_picking():
    """Return of list of six numbers, and a result that must be reached with
    these six numbers

    """
    number_list = random.sample(NUMBERS, 6)
    result = random.sample(range(1000), 1)
    return (number_list, *result)

def letter_game(nb_voyels, time):
    """ Run a letter game: choose randomly ten letter, among which there will
    be nb_voyels voyels; there is time seconds to find the longest word
    """
    draw = letter_picking(nb_voyels)
    print("***")
    print("Tirage composé de {0} voyelles: {1}".format(nb_voyels, draw))
    print("Le chrono est de {0} secondes...".format(time))
    i, o, e = select.select([sys.stdin], [], [], time)
    if i:
        word = sys.stdin.readline().strip().upper()
    else:
        word = ""
    print("Votre mot est: {0} ({1} lettres)".format(word, len(word)))
    if not valid_word(draw, word):
        print("Votre mot est invalide: les lettres choisies\
        ne sont pas toutes dans le tirage")
        word = ""
    return word

def valid_word(draw, word):
    """ Verify if a word is valid, according to the draw
    """
    draw_list = list(draw)
    for letter in word:
        if letter not in draw_list:
            return False
        else:
            draw_list.remove(letter)
    return True

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
        account = ""
    print("Votre résultat est : {0}, vous marquez {1} points"
          .format(account, compute_figure_score(draw[1], account)))
    return (account, compute_figure_score(draw[1], account))

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

    
def timeout():
    print("\nTemps écoulé!\n")

def run(nb_set, repartition):
    """Main program: play nb_set times a set of x figure draw(s) and y letter
    draw(s), repartition giving how y is being larger than x 
    
    """
    for i in range(1, 1+nb_set):
        for i in range(1, 1+repartition):
            nb_voyels = random.randint(2,8)
            print(''.join(letter_picking(nb_voyels)))
        print(figure_picking())
