from solver import solve
from ds3_parser import ds3_parser
from solver import StateTree
import sys

formula = None
spn = None

if len(sys.argv) == 2:
    formula = sys.argv[1]
    print(f"Checking Formula \"{formula}\"\n")
elif len(sys.argv) == 3:
    formula = sys.argv[1]
    spn = sys.argv[2]
    print(f"Checking Formula \"{formula}\" SPN: {spn}\n")
else:
    print("Incorrect number of arguments.\nCorrect Use: python ds3_checker.py <formula> [<spn>]")
    exit()

#Generates AST(formula)
parser = ds3_parser()
ast_formula = parser.parse(formula)
ast_formula = ast_formula.children[0]  #Ignores Tree Root (_exp)

#Generates Initial State
initial_state = StateTree(spn)

result = solve(initial_state, ast_formula)
print(f"Formula \"{formula}\" is {result}")