from lark import Lark, Visitor

ds3_parser = Lark("""
    _exp: _value _e* 
        | op1 _exp
        | "(" _exp ")" _e*

    _e: op2 _exp 
        
    _value: "true" 
        | "false"
        | symbol
    
    !op1: "~"
    !op2: "&" | "|" | "->"

    symbol: WORD

    %import common.WORD
    %import common.WS
    %ignore WS

    """, start='_exp')

#parse_tree = ds3_parser.parse(''' ~(A&B) & ~B & ~A ''')
#parse_tree = ds3_parser.parse(''' A & B ''')

#print(parse_tree)
#print(parse_tree.children[1])

class Print_Tokens(Visitor):
  def symbol(self, tree):
    assert tree.data == "symbol"
    t = tree.children[0]
    print(t)

#Print_Tokens().visit(parse_tree)
