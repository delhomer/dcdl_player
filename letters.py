import datetime
import numpy as np
import random
import threading
import time
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

def letter_picking(nb_voyels=0):
    """Return a list of ten letters, this list must be composed o  `nb_voyels` voyels

    Parameters
    ----------
    nb_voyels: integer
        Number of desired voyels (between 2 and 8)
    
    """
    random.seed(datetime.datetime.now())
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
    if not valid_word(draw, word):
        print("Votre mot est invalide: les lettres choisies ne sont pas toutes dans le tirage")
        word = ""
    print("Votre résultat est : {0}, vous marquez {1} points"
          .format(word, len(word)))
    return (word, len(word))

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
