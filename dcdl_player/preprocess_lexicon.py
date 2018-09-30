"""Some functions centered around lexicon exploitation starting from raw
lexicon files provided by the "Des Chiffres et Des Lettres" belgian federation
(http://fbccl.be/) through its "Le Francophone" software.

"""

import argparse
import os
import pandas as pd

def import_lexicon(path, nb_letters, sorting="word"):
    """Import a raw version of the lexicon

    Parameters
    ----------
    path : str
        Path of the raw lexicon folder on the file system
    nb_letters : int
        Number of letters of words in the lexicon file

    Returns
    -------
    pandas.DataFrame
        Lexicon
    """
    lexicon_path = os.path.join(path, "D" + str(nb_letters) + "tft.txt")
    df = pd.read_csv(lexicon_path, encoding="LATIN1", header=None)
    df.columns = ["lexicon"]
    df["draw"] = df.lexicon.apply(lambda x: x.split(" ")[0])
    df["word"] = df.lexicon.apply(lambda x: x.split(" ")[1])
    df["display"] = df.lexicon.apply(lambda x: " ".join(x.split(" ")[2:]))
    return df.drop(["lexicon"], axis=1).sort_values(by=sorting)


def get_lexicon(path, sorting="word"):
    """Build the complete lexicon by importing words with 2 to 10 letters

    Parameters
    ----------
    path : str
        Path of the raw lexicon folder on the file system
    sorting : str
        Lexicon sorting way (e.g. 'word' or 'draw')

    Returns
    -------
    dict
        Complete lexicon, with words of 2 to 10 letters
    """
    lexicon = {}
    for nb_letters in range(2, 11):
        lexicon[nb_letters] = import_lexicon(path, nb_letters, sorting)
    return lexicon


def save_lexicon(lexicon, path, sorting="word"):
    """Save preprocessed lexicon on the file system

    Parameters
    ----------
    lexicon : dict
        Complete lexicon, with words of 2 to 10 letters
    path : str
        Path of the preprocessed lexicon folder on the file system
    sorting : str
        Lexicon sorting way (*e.g.* 'draw' or 'word')
    """
    for nb_letters in range(2, 11):
        filename = str(nb_letters) + "letters_by_{}.csv".format(sorting)
        filepath = os.path.join(path, filename)
        lexicon[nb_letters].to_csv(filepath, index=False)
        print("Save {}-lettered words to {}.".format(nb_letters, filepath))


def preprocessed_lexicon(path, sorting="word"):
    """Preprocess lexicon, by getting raw lexicon, merging them into a
    dictionary and storing them on cleaned file on the file system

    Parameters
    ----------
    path : str
        Path of the lexicon folder on the file system
    sorting : str
        Lexicon sorting way (*e.g.* 'word' or 'draw')
    """
    dcdl_lexicon = get_lexicon(path, sorting)
    save_lexicon(dcdl_lexicon, path, sorting)


if __name__=='__main__':

    parser = argparse.ArgumentParser(description=("DCDL lexicon preprocessing"))
    parser.add_argument('-p', '--path', default='./data',
                        help=("Path to raw lexicon files "
                              "('le francophone 2018'"))
    parser.add_argument('-s', '--sorting', default='word',
                        help=("Sorting column, either 'draw', "
                              "'word' or 'display'."))
    args = parser.parse_args()

    preprocessed_lexicon(args.path, args.sorting)
