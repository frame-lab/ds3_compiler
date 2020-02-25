from solver import solve
from ds3_parser import ds3_parser

# import sys

# if len(sys.argv) != 2:
#     print("Incorrect number of arguments")
# else:
#     print("Correct number of arguments")

# expression = sys.argv[1]

parser = ds3_parser()
parse_tree = parser.parse('A->B')
print(parse_tree.pretty())
print(solve('w1',True,parse_tree.children[0]))