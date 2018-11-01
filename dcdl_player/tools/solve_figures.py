"""
"""

import argparse
import os


def solve(plates, target):
    """
    """
    plates.sort(reverse=True)
    solutions = {"1": {"program": "",
                       "result": max(plates)}}
    queue = [(plates, "+", ""),
             (plates, "-", ""),
             (plates, "*", ""),
             (plates, "/", "")]

    while len(queue) > 0:
        plates, op, program = queue.pop()
        current_plates = plates.copy()
        for i, p1 in enumerate(current_plates):
            p2_candidates = set(current_plates[(i+1):])
            for p2 in p2_candidates:
                if op == "-" and p1 - p2 in [0, p2]:
                    continue
                if op == "*" and (p1 == 1 or p2 == 1):
                    continue
                if op == "/" and (p1 == 1 or p2 == 1
                                  or p1 / p2 == p2 or p1 % p2 > 0):
                    continue
                if op == "/" and p1 % p2 > 0:
                    continue

                if op == "+":
                    res = p1 + p2
                elif op == "-":
                    res = p1 - p2
                elif op == "*":
                    res = p1 * p2
                elif op == "/":
                    res = int(p1 / p2)

                next_plates = current_plates.copy()
                next_plates.remove(p1)
                next_plates.remove(p2)
                next_plates.append(res)
                next_program = (program + str(p1) + op + str(p2)
                                + "=" + str(res) + "\n")
                if abs(res - target) < abs(solutions["1"]["result"] - target):
                    solutions = {"1": {"program": next_program,
                                       "result": res}}
                elif (abs(res - target) ==
                      abs(solutions["1"]["result"] - target)):
                    solutions[str(len(solutions)+1)] = {"program":
                                                        next_program,
                                                        "result": res}

                if len(next_plates) > 1:
                    next_plates.sort(reverse=True)
                    for next_op in "+-*/":
                        queue.append((next_plates, next_op,
                                      next_program))
    return solutions


def human_readable(solutions):
    """
    """
    result = ""
    for k, v in solutions.items():
        result = result + "Solution n°" + k + ":\n" + v["program"]
    return result

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
    solutions = solve(args.draw, args.result)
    print(human_readable(solutions))

if __name__=='__main__':

    program_description = ("Solve a figure draw by finding the good count.")
    parser = argparse.ArgumentParser(description=program_description)
    parser.add_argument('-d', '--draw', required=True, nargs="+", type=int,
                        help="Figure draw")
    parser.add_argument('-r', '--result', required=True, type=int,
                        help="Result to find")
    args = parser.parse_args()

    main(args)
