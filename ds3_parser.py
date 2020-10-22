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
        diamond: "<" markup ";" subnet ">" _exp
        box: "[" markup ";" subnet "]" _exp
        
        markup: INITIAL 
            | marking
            | marking _markup
        _markup: "," marking _markup
            | "," marking
        marking: ID "=" NAT

        subnet: ALL 
            | transition
            | transition _subnet
        _subnet: "," transition _subnet
            | "," transition
        transition: ID
        
        true: "true"
        false: "false"
        loc_exp: /[a-zA-Z][a-zA-Z_0-9]*\s*(<=|>=|!=|<|>|=)\s*[\d]+/

        INITIAL: "."
        ALL: "@"
        PATH: /(\/{0,1}(((\w)|(\.)|(\\\s))+\/)*((\w)|(\.)|(\\\s))+)|\//
        NAT: /[0-9]+/
        ID: /[a-zA-Z][a-zA-Z_0-9]*/

        %import common.WS
        %ignore WS

        """, start='_exp')

def parse(formula):
    ast = parser().parse(formula)
    ast = ast.children[0]  #Ignores Tree Root (_exp)
    
    return ast
