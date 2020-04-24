import stormpy
from datetime import datetime

class StateTree:
    def __init__(self, model, name= None):
        if name:
            self.name = name
        else:
            self.name = str(datetime.now())
        self.model = model
        self.children = []
    
    def append_child(self, node):
        if isinstance(node, StateTree):
            self.children.append(node)


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

    print("State:",state.name,"Entails:",valid,"Formulae:",formulae)
    
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
        if not networkExecutes(model):
            return False 

        ## Quando que o meu estado muda no sentido de estado no sentido de ds3?
        ## E no sentido do storm?

        #Updates State Tree
        new_state = StateTree(model)
        state.children.append(new_state)

        if has_modality(exp):    
            return solve(new_state,True,exp)
        else:
            # No modality inside -> Goes directly to Storm
            
            #True/False (Quantity must be resolved to true or false ?)

            # TO DO - Get a node corresponding String Formulae (reconstruct the subtree to a string)
            return model_check_storm(jani_program,syntax_tree_to_string(exp))
    else:
        #~<spn> formula == [spn] ~formula
        return 
    
def has_modality(formulae):
    if formulae.data == "diamond" or formulae.data == "box":
       return True
    
    for index in range(len(formulae.children)):
        if has_modality(formulae.children[index]):
            return True 
    return False

def model_check_storm(program, storm_formula):
    #Marcação do estado & garantir que o estado é final (definir propriedade e passar pro storm)

    print("Storm Formula:" + storm_formula)

    #properties = stormpy.parse_properties_for_jani_model("eating1 = 1",program)
    properties = stormpy.parse_properties_for_jani_model(storm_formula,program)
    model = stormpy.build_model(program, properties)
    result = stormpy.check_model_sparse(model, properties[0])
    
    #Change to consider only final states instead of initial states
    initial_state = model.initial_states[0]
    print("\tProperty check \n\t\tResult (for initial states): {}".format(result.at(initial_state)))

    return result.at(initial_state)

def networkExecutes(model):
    #TO DO - Evolve the condition: How to verify if the network executes?
    return model.nr_states > 1

def syntax_tree_to_string(exp):
    ## How to transform the syntax tree back to a string in an easy way?
    # Use recursion to mount the string
    # Use a function that relates non token/terminals with their respective string counterpart
    #   Ex.: implication => "->"
    #       negation => "~"
    #       conjunction => "&"
    return ""

#def box(state, valid, formulae):    

# def net_markup_exp: 
#   Ex.: "eating1=1"

def implication(state, valid, formulae):
    print("State:",state.name,"Entails:",valid,"Formulae:",formulae)
    
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,False,lhs) or solve(state,True,rhs)
    else:
        return solve(state,True,lhs) and solve(state,False,rhs)

def disjunction(state,valid,formulae):
    print("State:",state.name,"Entails:",valid,"Formulae:",formulae)
    
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,True,lhs) or solve(state,True,rhs)
    else:
        return solve(state,False,lhs) and solve(state,False,rhs)


def conjunction(state,valid,formulae):
    print("State:",state.name,"Entails:",valid,"Formulae:",formulae)
    
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,True,lhs) and solve(state,True,rhs)
    else:
        return solve(state,False,lhs) or solve(state,False,rhs)

def negate(state,valid,formulae):
    print("State:",state.name,"Entails:",valid,"Formulae:",formulae)
    
    return solve(state,not valid, formulae.children[0])

def symbol(state,valid,formulae):
    print("State:",state.name,"Entails:",valid,"Formulae:",formulae)
    return valid_on_state(state,formulae) if valid else not valid_on_state(state,formulae)

def valid_on_state(state,symbol):
    #Futuramente tera o link com a funcao de valoracao
    #return symbol in valor_function(state)

    # Check if exp is valid based on Storm Output
    # Ex.: Is "eating1=1" valid on state?
    #   If there's no state(execution) "eating1=1" is false
    return False