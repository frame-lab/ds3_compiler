from lark import Lark
ds3_parser = Lark("""
    e: value f_* 
        | op1 e
        | "(" e ")" f_*

    f_: op2 e 
        
    !value: "true" 
        | "false"
        | symbol
    
    !op1: "~"
    !op2: "&" | "|" | "->"

    symbol: WORD

    %import common.WORD
    %import common.WS
    %ignore WS

    """, start='e')

print(ds3_parser.parse('''
        ~(A&B) & ~B & ~A
    '''
))