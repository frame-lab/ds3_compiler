from solver import solve
from ds3_parser import ds3_parser
from solver import StateTree

# import sys

# if len(sys.argv) != 2:
#     print("Incorrect number of arguments")
# else:
#     print("Correct number of arguments")

# expression = sys.argv[1]

#preciso dar PNPRO como entrada
network = 'example_models/rock_paper_scissors.jani'

parser = ds3_parser()
#parse_tree = parser.parse("< {} > draw = 3".format(network))
parse_tree = parser.parse("< {} > < {} > draw = 3 ".format(network, network))

#Default Initial State
stateTree = StateTree()

#Ignores Tree Root (_exp)
formulae = parse_tree.children[0]

result = solve(stateTree, True, formulae)
print("Formulae Result: {}".format(result))
