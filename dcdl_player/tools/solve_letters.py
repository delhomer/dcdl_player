"""
"""

import argparse
import numpy as np
import os
import pandas as pd


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
    for nb_letters in range(len(draw), 1, -1):
        best_word_n = find_best_word_n(draw, nb_letters, path)
        best_word_n["nb_letters"] = nb_letters
        solution = solution.append(best_word_n, ignore_index=True)
    solution["nb_letters"] = solution["nb_letters"].astype(int)
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


def human_readable(solutions):
    """Print letter solution in a human-readable way

    Parameters
    ----------
    solutions : pandas.DataFrame
        Letter draw best solutions, ordered by number of letters

    Returns
    -------
    str
        Human-readable version of `solutions`
    """
    result = ""
    for i, group in solutions.groupby("nb_letters"):
        result = result + str(i) + " letters:" + "\n"
        result = result + " ".join(group["display"]) + "\n\n"
    return result


def main(args):
    """
    """
    assert len(args.draw) <= 10, "Maximum 10 letters in the draw!"
    solutions = find_best_word(args.draw.lower(), args.lexicon_path)
    print(human_readable(solutions))


if __name__=='__main__':

    main(args)
