"""This module focuses on the addition technique: starting from a word of N
letters, one looks for words of (N+1) letters that use the letters of the
initial word, plus one additional letter.

It highlights the added letters as well as the longer words that result.

"""

import argparse
import numpy as np
import os
import pandas as pd


def addition(word, datapath="./data"):
    """Compute valid letter additions on the given `word`

    Parameters
    ----------
    word : str
        Word from which additions are computed
    datapath : str
        Lexicon path on the file system

    Returns
    -------
    pandas.DataFrame
        Set of letter addition with the associated words
    """
    nb_letters = len(word)
    filepath = str(nb_letters + 1) + "letters_by_draw.csv"
    lexicon = pd.read_csv(os.path.join(datapath, filepath))
    draw = ''.join(sorted(word))
    for letter in draw:
        lexicon = lexicon.loc[extract_candidates(letter, lexicon["draw"])]
        lexicon["draw"] = [word.replace(letter, "", 1)
                           for word in lexicon["draw"]]
    return lexicon.reset_index(drop=True)


def extract_candidates(letter, candidates):
    """
    Parameters
    ----------
    letter : str
    candidates : list
    """
    return np.array([letter in d for d in candidates])


def addition_as_dict(word, datapath="./data"):
    """Compute valid letter additions on the given `word`

    Parameters
    ----------
    word : str
        Word from which additions are computed
    datapath : str
        Lexicon path on the file system

    Returns
    -------
    pandas.DataFrame
        Set of letter addition with the associated words
    """
    additions = addition(word, datapath)
    additions = additions.groupby("draw")["display"].apply(lambda x: ' ; '.join(x))
    return [{"letter": i, "word": x} for i, x in additions.iteritems()]


if __name__=='__main__':

    program_description = ("Retrieve the list of valid words obtained "
                           "after a word addition.")
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-l', '--lexicon-path', default="data",
                        help="Path to lexicon")
    parser.add_argument('-w', '--word', required=True,
                        help="Word to extend")
    args = parser.parse_args()

    additions = addition_as_dict(args.word, args.lexicon_path)
    print(additions)
