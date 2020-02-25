from lark import Lark, Visitor

ds3_parser = Lark("""
    _exp: "(" _exp ")"
        | _op2    
        | _op1
        | _value 
        
    _op1: diamond
        | box
        | negate
    
    _op2: conjunction
        | disjunction
        | implication

    _value: true | false | symbol
    
    true: "true"
    false: "false"
    symbol: WORD  

    negate: "~" _exp
    conjunction: _exp "&" _exp
    disjunction: _exp "|" _exp
    implication: _exp "->" _exp
    diamond: "<" path ">" _exp
    box: "[" path "]" _exp

    path: WORD

    %import common.WORD
    %import common.WS
    %ignore WS

    """, start='_exp')

parse_tree = ds3_parser.parse(''' ~(A&B) & ~B & ~A ''')
print(parse_tree)
