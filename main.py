import numpy as np

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
    return (number_list, result)
