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
#E ter a opcao de passar SPN como parametro fora da formula 
#   (parametro opcional msm so se o usuario quiser verificar algo no estado inicial 
#           (ou seja sem uso de modalidade))
#  Faz sentido o usuário não passar rede alguma? Nesse caso eu teria um modelo vazio, é possível, mas incomum.
network = 'example_models/philosophers.jani'

parser = ds3_parser()
#parse_tree = parser.parse(" eating1 = 1")
parse_tree = parser.parse(" < {} > thinking1 = 1".format(network))

#parse_tree = parser.parse("< {} > < {} > draw = 3 ".format(network, network))

#Default Initial State
stateTree = StateTree(network)

#Ignores Tree Root (_exp)
formulae = parse_tree.children[0]

result = solve(stateTree, formulae)
print("Formulae Result: {}".format(result))