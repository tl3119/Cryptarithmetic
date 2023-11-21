import argparse
from typing import List, Tuple


def minimum_remaining_values(variables, assigned, domains):
    unassigned_variables = [var for var in variables if var not in assigned]
    if not unassigned_variables:
        return None

    min_length = len(domains[unassigned_variables[0]])
    min_variables = [unassigned_variables[0]]

    for var in unassigned_variables[1:]:
        if len(domains[var]) < min_length:
            min_length = len(domains[var])
            min_variables = [var]
        # if there are multiple variables have same values
        elif len(domains[var]) == min_length:
            min_variables.append(var)   

    return min_variables


# if multiple values are left after apply MRV, then apply degree_heuristic
def degree_heuristics(variables, constraints, assigned, min_variables):
    unassigned_variables = [var for var in variables if var not in assigned]
    if not unassigned_variables:
        return None

    # a dictionary to count number of constraints in the default constraints
    degrees = {var: 0 for var in unassigned_variables}

    for constraint in constraints:
        var1, var2 = constraint
        if var1 in min_variables and var2 in unassigned_variables:
            degrees[var1] += 1
        if var1 in unassigned_variables and var2 in min_variables:
            degrees[var2] += 1

    degree_variable = max(degrees, key=degrees.get)

    return degree_variable


# Main function
def main() -> None:
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    cmdline = parser.parse_args()

    # Read input file and create initial and goal states
    with open(cmdline.filename, 'r') as file:
        lines = file.read().splitlines()

    # include all variables
    variables = set(''.join(lines))
    assigned = {}

    # Initialize domains based on variable-specific constraints
    domains = {}

    index = 1
    for var in variables:
        if index == 1 or index == 5:
            domains[var] = list(range(1, 10))
        elif index == 9:
            domains[var] = [1]
        else:
            domains[var] = list(range(10))
        index += 1

    # set constraints as List[Tuple[str, str]], ex: [(x1, x2), (x1,x3)]
    constraints = []

if __name__ == "__main__":
    main()
