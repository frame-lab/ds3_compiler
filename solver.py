#implementar a execucao de prova com estrategia

model = 'modelo'
stateTree = ['w1']

def solve(state, valid, formulae):
    if(formulae.__contains__('->')):
        return implication(state,valid,formulae)
    elif(formulae.__contains__('|')):
        return disjunction(state,valid,formulae)
    elif(formulae.__contains__('&')):
        return conjunction(state,valid,formulae)
    elif(formulae.startswith('~')):
        return negate(state,valid,formulae)
    else:
        return symbol(state,valid,formulae)

def implication(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    exp = formulae.split("->")
    lhs = exp[0]
    rhs = exp[1]

    if valid:
        return solve(state,False,lhs) or solve(state,True,rhs)
    else:
        return solve(state,True,lhs) and solve(state,False,rhs)

def disjunction(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    exp = formulae.split('|')
    lhs = exp[0]
    rhs = exp[1]

    if valid:
        return solve(state,True,lhs) or solve(state,True,rhs)
    else:
        return solve(state,False,lhs) and solve(state,False,rhs)


def conjunction(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    exp = formulae.split('&')
    lhs = exp[0]
    rhs = exp[1]

    if valid:
        return solve(state,True,lhs) and solve(state,True,rhs)
    else:
        return solve(state,False,lhs) or solve(state,False,rhs)

def negate(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    formulae = formulae[1:]
    
    return solve(state,not valid, formulae)

def symbol(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    return valid_on_state(state,formulae) if valid else not valid_on_state(state,formulae)

def valid_on_state(state,symbol):
    if symbol == 'TRUE':
        return True
    elif symbol == 'FALSE':
        return False
    else:
        #Futuramente tera o link com a funcao de valoracao
        #return symbol in valor_function(state)
        return False

#print(solve('w1',True,'FALSE'))
#print(solve('w1',True,'A'))
#print(solve('w1',True,'~A'))
#print(solve('w1',True,'~A&~B'))
#print(solve('w1',True,'A|B'))
#print(solve('w1',True,'~A|B'))
print(solve('w1',True,'A->B'))
print(solve('w1',True,'~A->B'))