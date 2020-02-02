from typing import List

def tableau(formulae: str, value: bool, true_vars: List[bool], false_vars: List[bool]):
    if(len(formulae) == 0):
        return (true_vars,false_vars)
    elif(formulae.startswith('~')):
        return negate(formulae.strip('~'), value, true_vars, false_vars)
    else:
        return literal(formulae,value,true_vars,false_vars)

def negate(formulae: str, value: bool, true_vars: List[bool], false_vars: List[bool]):    
    return tableau(formulae, not value, true_vars, false_vars)

def literal(literal: str, value: bool, true_vars: List[bool], false_vars: List[bool]):
    true_vars.append(literal) if value else false_vars.append(literal)
    
    return(true_vars,false_vars)

print(tableau("A",True, [],[]))
print(tableau("~B",True, [],[]))
