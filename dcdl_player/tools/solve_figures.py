"""
"""

import argparse
import copy
import os


def encountered_step(step, steps):
    """
    """
    return any([(step[0] == s[0]
                 and all([i in s[1] for i in step[1]])
                 and step[2] == s[2])
                for s in steps])


def is_duplicated(reasoning, solutions):
    """
    """
    return any([all([encountered_step(rs, v["reasoning"][1])
                for rs in reasoning[1]])
                for k, v in solutions.items()])


def update_reasoning(reasoning, p1, p2, raw_op, res):
    """
    """
    assert raw_op in ["+", "-", "*", "/"]
    op = "+" if raw_op in "+-" else "*"
    if p1 in reasoning[0]:
        reasoning[0].remove(p1)
        if p2 in reasoning[0]: # p1 and p2 not yet used
            reasoning[0].remove(p2)
            reasoning[1].append([op, [p1, p2], res])
        else: # p1 not yet used, p2 intermediary result
            step_p2_mask = [p2 == step[2] for step in reasoning[1]]
            step_p2 = [step for step, pred in zip(reasoning[1], step_p2_mask)
                       if pred][0]
            step_p2_op, step_p2_plates, step_p2_res = step_p2
            if op == step_p2_op:
                step_p2_plates.append(p1)
                new_step = [op, step_p2_plates, res]
                reasoning[1].remove(step_p2)
                reasoning[1].append(new_step)
            else:
                new_step = [op, [p1, step_p2_res], res]
                reasoning[1].append(new_step)
    else:
        step_p1_mask = [p1 == step[2] for step in reasoning[1]]
        step_p1 = [step for step, pred in zip(reasoning[1], step_p1_mask)
                   if pred][0]
        step_p1_op, step_p1_plates, step_p1_res = step_p1
        if p2 in reasoning[0]: # p1 intermediary result, p2 not yet used
            reasoning[0].remove(p2)
            if op == step_p1_op:
                step_p1_plates.append(p2)
                new_step = [op, step_p1_plates, res]
                reasoning[1].remove(step_p1)
                reasoning[1].append(new_step)
            else:
                new_step = [op, [step_p1_res, p2], res]
                reasoning[1].append(new_step)
        else: # p1 and p2 intermediary results
            step_p2_mask = [p2 == step[2] for step in reasoning[1]]
            step_p2 = [step for step, pred in zip(reasoning[1], step_p2_mask)
                       if pred][p1==p2]
            step_p2_op, step_p2_plates, step_p2_res = step_p2
            if op == step_p1_op == step_p2_op:
                new_step = [op, [*step_p1_plates, *step_p2_plates], res]
                reasoning[1].append(new_step)
                reasoning[1].remove(step_p1)
                reasoning[1].remove(step_p2)
            elif op == step_p1_op and op != step_p2_op:
                step_p1_plates.append(p2)
                reasoning[1].append([op, step_p1_plates, res])
                reasoning[1].remove(step_p1)
            elif op == step_p2_op and op != step_p1_op:
                step_p2_plates.append(p1)
                reasoning[1].append([op, step_p2_plates, res])
                reasoning[1].remove(step_p2)
            else:
                reasoning[1].append([op, [p1, p2], res])



def solve(plates, target):
    """
    """
    plates.sort(reverse=True)
    solutions = {"1": {"program": "",
                       "reasoning": [plates, []],
                       "result": max(plates)}}
    queue = [(plates, "+", "", [plates, []]),
             (plates, "-", "", [plates, []]),
             (plates, "*", "", [plates, []]),
             (plates, "/", "", [plates, []])]
    while len(queue) > 0:
        plates, op, program, reasoning = queue.pop()
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
                next_reasoning = copy.deepcopy(reasoning)
                update_reasoning(next_reasoning, p1, p2, op, res)
                if abs(res - target) < abs(solutions["1"]["result"] - target):
                    solutions = {"1": {"program": next_program,
                                       "reasoning": next_reasoning,
                                       "result": res}}
                elif (abs(res - target) ==
                      abs(solutions["1"]["result"] - target)):
                    if not is_duplicated(next_reasoning, solutions):
                      solutions[str(len(solutions)+1)] = {"program":
                                                          next_program,
                                                          "reasoning":
                                                          next_reasoning,
                                                          "result": res}

                if len(next_plates) > 1:
                    next_plates.sort(reverse=True)
                    for next_op in "+-*/":
                        queue.append((next_plates, next_op,
                                      next_program, next_reasoning))
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
