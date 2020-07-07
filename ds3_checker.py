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
#parse_tree = parser.parse("< {} > wait1 = 1".format(network))
parse_tree = parser.parse("! < {} > draw = 3".format(network))

print(parse_tree.pretty())

#Default Initial State
stateTree = StateTree(name='w1')

#Lembrar de ignorar o no raiz da arvore que possui _exp
print(solve(stateTree,True,parse_tree.children[0]))
