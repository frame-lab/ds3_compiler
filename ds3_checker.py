from solver import solve
from ds3_parser import ds3_parser
from solver import StateTree
import sys

formula = None
spn = None

if len(sys.argv) == 2:
    formula = sys.argv[1]
    print("Checking:\n\tFormula: {}".format(formula))
elif len(sys.argv) == 3:
    formula = sys.argv[1]
    spn = sys.argv[2]
    print("Checking:\n\tFormula:{} SPN: {}".format(formula,spn))
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
print("Formulae Validation: {}".format(result))