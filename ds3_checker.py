from solver import solve
from ds3_parser import ds3_parser

# import sys

# if len(sys.argv) != 2:
#     print("Incorrect number of arguments")
# else:
#     print("Correct number of arguments")

# expression = sys.argv[1]

#preciso dar PNPRO como entrada
network = 'example_models/philosophers.jani'

parser = ds3_parser()
#parse_tree = ds3_parser.parse(''' ~(A&B) & ~B & ~A ''')
#parse_tree = parser.parse('A | B -> ~B')
parse_tree = parser.parse("< {} > eating1 = 1".format(network))

print(parse_tree.pretty())

#Lembrar de ignorar o no raiz da arvore que possui _exp
print(solve('w1',True,parse_tree.children[0]))

# for child in parse_tree.children:
#     print(child.data