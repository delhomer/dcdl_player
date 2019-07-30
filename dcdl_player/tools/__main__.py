"""Main method for dcdl_player and subsequent parser

Inspired from https://github.com/mapbox/robosat

"""

import argparse

from dcdl_player.tools import (
    addition,
    solve_letters,
    word_existence
)


def addition_parser(subparser, reference_func):
    """Parser for addition command

    Parameters
    ----------
    subparser : argparser.parser.SubParsersAction
    reference_func : function
    """
    parser = subparser.add_parser(
        "addition",
        help=("Retrieve the list of valid words obtained "
              "after a word addition."),
    )
    parser.add_argument('-l', '--lexicon-path', default="data",
                        help="Path to lexicon")
    parser.add_argument('-w', '--word', required=True,
                        help="Word to extend")
    parser.set_defaults(func=reference_func)


def solve_letters_parser(subparser, reference_func):
    """Parser for findword command

    Parameters
    ----------
    subparser : argparser.parser.SubParsersAction
    reference_func : function
    """
    parser = subparser.add_parser(
        "findword",
        help="Solve a letter draw by finding the longest words.",
    )
    parser.add_argument('-l', '--lexicon-path', default="data",
                        help="Path to lexicon")
    parser.add_argument('-d', '--draw', required=True,
                        help="Letter draw")
    parser.set_defaults(func=reference_func)


def word_existence_parser(subparser, reference_func):
    """Parser for exist command

    Parameters
    ----------
    subparser : argparser.parser.SubParsersAction
    reference_func : function
    """
    parser = subparser.add_parser(
        "exist",
        help="Verify the existence of a word in the lexicon.",
    )
    parser.add_argument('-l', '--lexicon-path', default="data",
                        help="Path to lexicon")
    parser.add_argument('-w', '--word', required=True,
                        help="Word to verify")
    parser.set_defaults(func=reference_func)


def main():
    parser = argparse.ArgumentParser(
        prog="dcdl",
        description="Small Countdown utils to play with words"
    )
    sub_parsers = parser.add_subparsers(dest="command")

    addition_parser(sub_parsers, reference_func=addition.main)
    solve_letters_parser(sub_parsers, reference_func=solve_letters.main)
    word_existence_parser(sub_parsers, reference_func=word_existence.main)
    args = parser.parse_args()

    if args.func:
        args.func(args)
    else:
        parser.print_help()


if __name__ == "__main__":

    main()
