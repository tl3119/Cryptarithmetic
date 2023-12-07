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


def set_up_constraints(variables, unique_variables):
    # set constraints as List[Tuple[str, str]], ex: [(x1, x2), (x1,x3)]
    constraints = []

    # set up Alldiff constraint (C1)
    for i in unique_variables:
        for j in unique_variables:
            if j != i:
                if ((i, j) not in constraints) and ((j, i) not in constraints):
                    if i < j: # according to alphabetical order so that no repeated constraints
                        constraints += [(i, j)]
                    else:
                        constraints += [(j, i)]

    # print("constraints: ", constraints)
    # print(len(constraints))

    # print("unique variables: ", unique_variables)
    # set up rest of the constraints
    rest_constraints = []

    # C2 (x4+x8 = 10*alpha+x13)
    rest_constraints += [tuple(sorted((variables[4-1], variables[8-1])))]
    rest_constraints += [tuple(sorted((variables[4-1], variables[13-1])))]
    rest_constraints += [tuple(sorted((variables[8-1], variables[13-1])))]
    rest_constraints += [tuple(sorted(("alpha", variables[13-1])))]
    rest_constraints += [tuple(sorted(("alpha", variables[4-1])))]
    rest_constraints += [tuple(sorted(("alpha", variables[8-1])))]

    # C3 (alpha+x3+x7 = 10*beta+x12)
    rest_constraints += [tuple(sorted(("alpha", variables[3-1])))]
    rest_constraints += [tuple(sorted(("alpha", variables[7-1])))]
    rest_constraints += [tuple(sorted(("alpha", variables[12-1])))]
    rest_constraints += [tuple(sorted(("alpha", "beta")))]
    rest_constraints += [tuple(sorted((variables[3-1], variables[7-1])))]
    rest_constraints += [tuple(sorted((variables[3-1], variables[12-1])))]
    rest_constraints += [tuple(sorted((variables[3-1], "beta")))]
    rest_constraints += [tuple(sorted((variables[7-1], "beta")))]
    rest_constraints += [tuple(sorted((variables[7-1], variables[12-1])))]
    rest_constraints += [tuple(sorted((variables[12-1], "beta")))]

    # C4 (beta+x2+x6 = 10*gamma+x11)
    rest_constraints += [tuple(sorted(("beta", variables[2-1])))]
    rest_constraints += [tuple(sorted(("beta", variables[6-1])))]
    rest_constraints += [tuple(sorted(("beta", variables[11-1])))]
    rest_constraints += [tuple(sorted(("beta", "gamma")))]
    rest_constraints += [tuple(sorted((variables[2-1], variables[6-1])))]
    rest_constraints += [tuple(sorted((variables[2-1], "gamma")))]
    rest_constraints += [tuple(sorted((variables[2-1], variables[11-1])))]
    rest_constraints += [tuple(sorted((variables[6-1], "gamma")))]
    rest_constraints += [tuple(sorted((variables[6-1], variables[11-1])))]
    rest_constraints += [tuple(sorted((variables[11-1], "gamma")))]

    # C5 (gamma+x1+x5 = 10+x10)
    rest_constraints += [tuple(sorted((variables[1-1], "gamma")))]
    rest_constraints += [tuple(sorted((variables[5-1], "gamma")))]
    rest_constraints += [tuple(sorted((variables[10-1], "gamma")))]
    rest_constraints += [tuple(sorted((variables[1-1], variables[5-1])))]
    rest_constraints += [tuple(sorted((variables[1-1], variables[10-1])))]
    rest_constraints += [tuple(sorted((variables[5-1], variables[10-1])))]

    for i in rest_constraints:
        if i not in constraints:
            constraints += [i]

    return constraints

def select_unassigned_variable(unique_variables, assignment, domains, constraints):
    min_variables = minimum_remaining_values(unique_variables, assignment, domains)
    if min_variables is None:
        return None
    else:
        if len(min_variables) > 1:
            degree_var = degree_heuristics(unique_variables, constraints, assignment, min_variables)
            if degree_var is None:
                return None
            else:
                return degree_var
        else:
            return min_variables

def backtracking_search(variables, unique_variables, domains, constraint, assignment, clean_variables):
    if len(assignment) == len(unique_variables): # if assignment complete
        if check_completion(assignment, clean_variables):
            print("solution found!!!")
            print("assignment: ", assignment)
            return assignment
    current_variable = select_unassigned_variable(unique_variables, assignment, domains, constraint)
    if current_variable is not None:
        current_variable = current_variable[0] # current variable return a list of len = 1
        # print("current variable: ", current_variable)
        for value in domains[current_variable]:
            if value not in assignment.values():  # Check if the value is not already assigned
                new_assignment = assignment.copy()
                new_assignment[current_variable] = value
                # print("assignment: ", new_assignment)
                result = backtracking_search(variables, unique_variables, domains, constraint, new_assignment, clean_variables)
                if result is not None:
                    return result
                assignment[current_variable] = None
    return None

    # if len(assignment) == len(unique_variables): # if assignment complete
    #     if check_completion(assignment, clean_variables):
    #         print("solution found!!!")
    #         print("assignment: ", assignment)
    #         return assignment
    # for i in range(len(unique_variables)):
    #     current_variable = select_unassigned_variable(unique_variables, assignment, domains, constraint)
    #     if current_variable is not None:
    #         current_variable = current_variable[0] # current variable return a list of len = 1
    #         for value in domains[current_variable]:
    #             assignment[current_variable] = value
    #             print("assignment: ", assignment)
    #             backtracking_search(variables, unique_variables, domains, constraint, assignment, clean_variables)

# def consistent(current_variable, value, assignment):
#     assignment[current_variable] = value
#     for i in assignment: 

def check_completion(assignment, clean_variables): # function checked
    line1_value = (assignment[clean_variables[1-1]]*1000
                    +assignment[clean_variables[2-1]]*100
                    +assignment[clean_variables[3-1]]*10
                    +assignment[clean_variables[4-1]])
    line2_value = (assignment[clean_variables[5-1]]*1000
                    +assignment[clean_variables[6-1]]*100
                    +assignment[clean_variables[7-1]]*10
                    +assignment[clean_variables[8-1]])
    line3_value = (assignment[clean_variables[9-1]]*10000
                    +assignment[clean_variables[10-1]]*1000
                    +assignment[clean_variables[11-1]]*100
                    +assignment[clean_variables[12-1]]*10
                    +assignment[clean_variables[13-1]])
    if line1_value + line2_value == line3_value:
        return True
    else:
        return False

# Main function
def main() -> None:
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    cmdline = parser.parse_args()

    # Read input file and create initial and goal states
    with open(cmdline.filename, 'r') as file:
        lines = file.read().splitlines()

    # get all variables
    variables = []
    clean_variables = []
    for i in lines:
        for j in i:
            variables += [j]
            clean_variables += [j]

    # make a set of unique variables
    unique_variables = set(''.join(lines))
    
    # get the constraints set up
    constraints = set_up_constraints(variables, unique_variables)

    # put the three auxilary variables in 
    # unique_variables.add("alpha") # three auxillary variables representing carry over
    # unique_variables.add("beta")
    # unique_variables.add("gamma")

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
    domains["alpha"] = [0, 1]
    domains["beta"] = [0, 1]
    domains["gamma"] = [0, 1]

    # print out the parameters and check
    print("constraints: ", constraints)
    print("domains: ", domains)
    print("variables: ", variables)
    print("unique variables: ", unique_variables)

    assignment = {}
    backtracking_search(variables, unique_variables, domains, constraints, assignment, clean_variables)

    # assignment1 = {'M': 1, 'S': 9, 'E': 5, 'R': 8, 'Y': 2, 'D': 7, 'O': 0, 'N': 6} # this is a solution for SENDMOREMONEY
    # print(clean_variables)
    # print(check_completion(assignment1, clean_variables))

if __name__ == "__main__":
    main()