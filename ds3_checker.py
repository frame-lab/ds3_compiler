from ds3_parser import parse
from solver import solve
from state_tree import StateTree
import sys

formula = None
spn = None

if len(sys.argv) == 3:
    formula = sys.argv[1]
    spn = sys.argv[2]
    print(f"Checking Formula \"{formula}\" SPN: {spn}\n")
else:
    print("Incorrect number of arguments.\nCorrect Use: python ds3_checker.py <formula> <spn>")
    exit()

#Generates AST(formula)
ast_formula = parse(formula)

#Generates Initial State
initial_state = StateTree(spn)

result = solve(initial_state, ast_formula)
print(f"Final result: \"{formula}\" is {result}")