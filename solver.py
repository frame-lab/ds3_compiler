model = 'modelo'
stateTree = ['w1']
spn = 'caminho'

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

#<s,π>ϕ
# Inicialmente vou supor que a marcação é sempre a marcação inicial e
#  o programa é a própria rede.
# Logo, preciso guardar o caminho do arquivo que representa a rede apenas.
#def modal(state, valid, formulae):   

def implication(state, valid, formulae):
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
    
    return solve(state,not valid, formulae[1:])

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

print(solve('w1',True,'A->B'))
#print(solve('w1',True,'~A->B'))