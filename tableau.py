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
        if lhs_result[0]:
            return tableau(rhs, True, lhs_result[1], lhs_result[2])
        else: 
            return (False,true_vars,false_vars)            
    return 'whatever'

def negate(formulae, value, true_vars, false_vars):    
    return tableau(formulae.strip('~'), not value, true_vars, false_vars)

def literal(literal, value, true_vars, false_vars):
    return assign_value_check_contradiction(literal, value, true_vars, false_vars)

def assign_value_check_contradiction(symbol, value, true_vars, false_vars):
    if value:
        if symbol in (false_vars):
            return (False,true_vars,false_vars)
        else:
            updated = true_vars + tuple(symbol)
            return(True,updated,false_vars)
    else:
        if symbol in (true_vars):
            return (False,true_vars,false_vars)
        else:
            updated = false_vars + tuple(symbol)
            return (True,true_vars,updated)

print(tableau("A",True, (), ()))
print(tableau("~B",True, (),()))
print(tableau("A&B",True, (),()))
print(tableau("A&~B",True, (),()))
