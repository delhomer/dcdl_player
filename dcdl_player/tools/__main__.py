"""Main method for dcdl_player and subsequent parser

Inspired from https://github.com/mapbox/robosat

"""

import argparse

from dcdl_player.tools import (
    addition,
    solve_figures,
    solve_letters,
    word_existence
)


def add_parsers():
    parser = argparse.ArgumentParser(prog="./dcdl")
    subparser = parser.add_subparsers(title="dcdl_player tools", metavar="")

    # Add your tool's entry point below.

    addition.add_parser(subparser)
    solve_figures.add_parser(subparser)
    solve_letters.add_parser(subparser)
    word_existence.add_parser(subparser)

    # We return the parsed arguments, but the sub-command parsers
    # are responsible for adding a function hook to their command.

    subparser.required = True

    return parser.parse_args()


if __name__ == "__main__":
    args = add_parsers()
    args.func(args)
