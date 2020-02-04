def tableau(formulae, value, true_vars, false_vars):
    if(formulae.__contains__('&')):
        return conjunction(formulae,value,true_vars, false_vars)
    elif(formulae.startswith('~')):
        return negate(formulae, value, true_vars, false_vars)
    else:
        return literal(formulae,value,true_vars,false_vars)

def conjunction(formulae, value, true_vars, false_vars):
    exp = formulae.split('&')
    lhs = exp[0]
    rhs = exp[1]
    if value:
        lhs_result = tableau(lhs, True, true_vars, false_vars)
        if lhs_result is not None:
            return tableau(rhs, True, lhs_result[0], lhs_result[1])
    else:
        lhs_result = tableau(lhs, False, true_vars, false_vars)
        if lhs_result is not None:
            return lhs_result
        
        rhs_result = tableau(rhs,False,true_vars, false_vars)
        if rhs_result is not None:
            return rhs_result
        
    return None

def negate(formulae, value, true_vars, false_vars):    
    return tableau(formulae.strip('~'), not value, true_vars, false_vars)

def literal(literal, value, true_vars, false_vars):
    return assign_value_check_contradiction(literal, value, true_vars, false_vars)

def assign_value_check_contradiction(symbol, value, true_vars, false_vars):
    if check_contradiction(symbol, value, true_vars, false_vars):
        return None
    else:
        return assign_value(symbol, value, true_vars, false_vars) 

def check_contradiction(symbol,value, true_vars, false_vars):
    if value:
        return symbol in false_vars
    else:
        return symbol in true_vars

def assign_value(symbol,value, true_vars, false_vars):
    if value:
        if symbol in true_vars:
            return (true_vars,false_vars)
        return (true_vars + tuple(symbol), false_vars)
    else:
        if symbol in false_vars:
            return (true_vars,false_vars)
        return (true_vars, false_vars + tuple(symbol))

print(tableau("A",True, (), ()))
print(tableau("~B",True, (),()))
print(tableau("A&B",True, (),()))
print(tableau("A&~B",True, (),()))
