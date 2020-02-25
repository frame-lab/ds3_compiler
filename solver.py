model = 'modelo'
stateTree = ['w1']
spn = 'caminho'

def solve(state, valid, formulae):
    if(formulae.data == 'conjunction'):
        return conjunction(state,valid,formulae)
    elif(formulae.data == 'disjunction'):
        return disjunction(state,valid,formulae)
    elif(formulae.data == 'implication'):
        return implication(state,valid,formulae)
    elif(formulae.data == 'negate'):
        return negate(state,valid,formulae)
    elif(formulae.data == 'symbol'):
        return symbol(state,valid,formulae)
    elif(formulae.data == 'true'):
        return True
    elif(formulae.data == 'false'):
        return False

#<s,π>ϕ
# Inicialmente vou supor que a marcação é sempre a marcação inicial e
#  o programa é a própria rede.
# Logo, preciso guardar o caminho do arquivo que representa a rede apenas.
#def modal(state, valid, formulae):   
#Onde guardar o arquivo da rede? Ele precisa ser dado na propria formula?
#    caminho_arquivo_rede, formula

# def diamond: "<" path ">" _exp
    
# def box: "[" path "]" _exp

def implication(state, valid, formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,False,lhs) or solve(state,True,rhs)
    else:
        return solve(state,True,lhs) and solve(state,False,rhs)

def disjunction(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,True,lhs) or solve(state,True,rhs)
    else:
        return solve(state,False,lhs) and solve(state,False,rhs)


def conjunction(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,True,lhs) and solve(state,True,rhs)
    else:
        return solve(state,False,lhs) or solve(state,False,rhs)

def negate(state,valid,formulae):
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    
    return solve(state,not valid, formulae.children[0])

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

#print(solve('w1',True,'A->B'))