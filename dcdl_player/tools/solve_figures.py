"""
"""

import argparse
import os



def add_parser(subparser):
    """
    """
    parser = subparser.add_parser(
        "solve_figures",
        help="Solve a letter draw by finding the longest words.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument('-d', '--draw', required=True,
                        help="Figure draw")
    parser.add_argument('-r', '--result', required=True,
                        help="Result to find")
    parser.set_defaults(func=main)


def main(args):
    """
    """
    print(args.draw)
    print(args.result)

if __name__=='__main__':

    program_description = ("Solve a figure draw by finding the good count.")
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-d', '--draw', required=True, nargs="+",
                        help="Figure draw")
    parser.add_argument('-r', '--result', required=True,
                        help="Result to find")
    args = parser.parse_args()

    main(args)
