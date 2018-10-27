"""
"""

import argparse
import numpy as np
import os
import pandas as pd

from dcdl_player import solve_letters


def verify_existence(datapath, word):
    """Verify if `word` is an entry of the lexicon stored in `datapath`

    Parameters
    ----------
    datapath : str
        Lexicon folder, on the file system
    word : str
        Word to verify ; must contains between 2 and 10 letters

    Returns
    -------
    bool
        True if ̀word` is valid, False otherwise
    """
    if len(word) < 2 or len(word) > 10:
        raise ValueError(("\"{word}\" number of letters is invalid, please "
                          "choose a word with between 2 and 10 letters."
                          "").format(word=word))
    lexicon = solve_letters.get_lexicon(datapath, len(word))
    return lexicon["display"].str.contains(word).any()


def human_readable(word, does_exist):
    """Produce a human-readable string to answer the word existence question

    Parameters
    ----------
    word : str
        Word to verify
    does_exist : bool
        If true, the word exists, otherwise it does not exist

    Returns
    -------
    str
        Human-readable answer regarding word existence
    """
    if does_exist:
        return "\"{}\" is valid!".format(word)
    else:
        return  "\"{}\" is not valid!".format(word)


if __name__=='__main__':

    program_description = ("Verify the existence of a word in the lexicon.")
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-l', '--lexicon-path', default="data",
                        help="Path to lexicon")
    parser.add_argument('-w', '--word', required=True,
                        help="Word to verify")
    args = parser.parse_args()

    word_existence = verify_existence(args.lexicon_path, args.word)
    print(human_readable(args.word, word_existence))
