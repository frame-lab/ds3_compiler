import stormpy

class StateTree:
    def __init__(self, model):
        self.model = model
        self.children = []
    
    def append_child(self, node):
        if isinstance(node, StateTree):
            self.children.append(node)

model = 'modelo'
stateTree = StateTree('w1')
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
    if not valid:
        print("not yet implemented")
        return 

    print("State:",state,"Entails:",valid,"Formulae:",formulae)
    
    path = formulae.children[0]
    exp = formulae.children[1]

    # #Path: Token 
    # #Exp: Tree
    # print("\nPath:" + path)
    # print("\nExp:" + exp.data)

    jani_program, properties = stormpy.parse_jani_model(path)
    model = stormpy.build_model(jani_program, properties)

    print("Model - Storm Output:")
    print("\tNumber of states: {}".format(model.nr_states))
    print("\tNumber of transitions: {}".format(model.nr_transitions))
    print("\tLabels: {}".format(model.labeling.get_labels()))

    if valid:
        #Check if there's modality(diamond or box) inside of formulae
        if tem_modalidade_dentro():
            if networkExecutes(model):
                #Updates State Tree
                new_state = StateTree(model)
                stateTree.children.append(new_state)

                return solve(state,True,exp)
            else:
                return False
        else:
            # No modality inside
            # Goes directly to Storm
            if networkExecutes(model): 
                #Atualiza referencia da arvore de estados
                new_state = StateTree(model)
                stateTree.children.append(new_state)
                
                #True/False (Quantity must be resolved to true or false ?)
                return model_check_storm(jani_program,exp)
            else:
                return False
    else:
        #~<spn> formula == [spn] ~formula
        return 
    
    
def tem_modalidade_dentro():
    return False

def model_check_storm(program, storm_formula):
    print(storm_formula)

    properties = stormpy.parse_properties_for_jani_model("eating1 = 1",program)
    model = stormpy.build_model(program, properties)
    result = stormpy.check_model_sparse(model, properties[0])
    
    #Change to consider only final states instead of initial states
    initial_state = model.initial_states[0]
    print("\tProperty check \nResult (for initial states): {}".format(result.at(initial_state)))

    return result.at(initial_state)

def networkExecutes(model):
    #TO DO - Evolve the condigiton: How to verify if the network executes?
    return model.nr_states > 1

#def box(state, valid, formulae):    

# def net_markup_exp: 
#   Ex.: "eating1=1"

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

    # Check if exp is valid based on Storm Output
    # Ex.: Is "eating1=1" valid on state?
    #   If there's no state(execution) "eating1=1" is false
    return False