from lark import Lark
json_parser = Lark("""
    exp: symbol 
        | value 
        | op1 exp 
        | exp op2 exp 
    
    value: "true" 
        | "false"
    
    symbol: ESCAPED_STRING
    op1: "!"
    op2: "&" | "|"

    %import common.ESCAPED_STRING
    %import common.WS
    %ignore WS

    """, start='exp')