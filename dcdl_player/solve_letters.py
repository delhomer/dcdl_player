"""
"""

import argparse
import numpy as np
import os
import pandas as pd

from dcdl_player import preprocess_lexicon
from dcdl_player import addition


def get_lexicon(path, nb_letters, sorting="draw"):
    """Get words with `nb_letters` letters, and sort them according to
    `sorting` column

    Parameters
    ----------
    path : str
        Lexicon folder, on the file system
    nb_letters : str
        Number of letters in the words
    sorting : str
        Lexicon sorting key, either `draw` or `word`

    Returns
    -------
    pandas.DataFrame
        Lexicon
    """
    filename = str(nb_letters) + "letters_by_{}.csv".format(sorting)
    filepath = os.path.join(path, filename)
    return pd.read_csv(filepath)


def find_best_word(draw, path):
    """
    """
    solution = pd.DataFrame({"nb_letters": [], "draw": [],
                             "word": [], "display": []})
    for nb_letters in range(10, 1, -1):
        best_word_n = find_best_word_n(draw, nb_letters, path)
        best_word_n["nb_letters"] = nb_letters
        solution = solution.append(best_word_n, ignore_index=True)
    return solution.reset_index(drop=True)


def find_best_word_n(draw, nb_letters, path):
    """
    """
    lexicon = get_lexicon(path, nb_letters)
    mask = [is_word_in_draw(draw, word) for word in lexicon["draw"]]
    lexicon = lexicon.loc[mask]
    return lexicon


def is_word_in_draw(draw, word):
    """Check if a given `word` is a valid solution of the provided `draw`, by
    checking if the number of each letter in the word is inferior than the
    amount of the same letter in the draw

    Parameters
    ----------
    draw : str
        Set of drawn letters
    word : str
        Candidate word

    Returns
    -------
    bool
        True if `word` is a solution of the `draw`, False otherwise
    """
    letter_checks = [draw.count(letter) >= word.count(letter)
                     for letter in list(set(word))]
    return np.all(letter_checks)


if __name__=='__main__':

    program_description = ("Solve a letter draw by finding the longest words.")
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-l', '--lexicon-path', default="data",
                        help="Path to lexicon")
    parser.add_argument('-d', '--draw', required=True,
                        help="Letter draw")
    args = parser.parse_args()

    solutions = find_best_word(args.draw, args.lexicon_path)
    print(solutions)