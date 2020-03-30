import stormpy

model = 'modelo'
stateTree = ['w1']
spn = 'caminho'

def solve(state, valid, formulae):
    if(formulae.data == 'diamond'):
        return diamond(state,valid,formulae)
    elif(formulae.data == 'conjunction'):
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

def diamond(state, valid, formulae):  
    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    
    path = formulae.children[0]
    exp = formulae.children[1]

    # #Path: Token 
    # #Exp: Tree
    # print("\nPath:" + path)
    # print("\nExp:" + exp.data)

    jani_program, properties = stormpy.parse_jani_model(path)
    properties = stormpy.parse_properties_for_jani_model(exp.data,jani_program)
    model = stormpy.build_model(jani_program, properties)
    result = stormpy.check_model_sparse(model, properties[0])
    initial_state = model.initial_states[0]

    print("Storm Output:")
    print("\tNumber of states: {}".format(model.nr_states))
    print("\tNumber of transitions: {}".format(model.nr_transitions))
    print("\tLabels: {}".format(model.labeling.get_labels()))
    print("\tProperty check result: {}".format(result.at(initial_state)))
    
    ## TO-DO:

    # State control structure
    # Check if the SPN has transitions with probability of firing > 0
    # If it has create a new state on the structure
    # Check if exp is valid based on Storm Output
    # Return accordingly to the Solver function

    return 

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
    #Futuramente tera o link com a funcao de valoracao
    #return symbol in valor_function(state)
    return False