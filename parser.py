from lark import Lark

def parser():
    return Lark("""
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

        _value: true 
            | false 
            | loc_exp 
        
        negate: "!" _exp
        conjunction: _exp "&" _exp
        disjunction: _exp "|" _exp
        implication: _exp "=>" _exp
        diamond: "<" PATH ">" _exp
        box: "[" PATH "]" _exp
        
        true: "true"
        false: "false"
        loc_exp: /[a-zA-Z][a-zA-Z_0-9]*\s*(<=|>=|!=|<|>|=)\s*[\d]+/

        PATH: /(\/{0,1}(((\w)|(\.)|(\\\s))+\/)*((\w)|(\.)|(\\\s))+)|\//

        %import common.WS
        %ignore WS

        """, start='_exp')

def parse(formula):
    ast = parser().parse(formula)
    ast = ast.children[0]  #Ignores Tree Root (_exp)
    
    return ast