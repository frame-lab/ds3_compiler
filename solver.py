import stormpy
from state_tree import StateTree
from lark import Token

def solve(state, valid, formulae):
    print("State:", state.name, "Entails:", valid, "Formulae:", formulae)

    if(formulae.data == 'conjunction'):
        return conjunction(state,valid,formulae)
    elif(formulae.data == 'disjunction'):
        return disjunction(state,valid,formulae)
    elif(formulae.data == 'implication'):
        return implication(state,valid,formulae)
    elif(formulae.data == 'negate'):
        return negate(state,valid,formulae)
    elif(formulae.data == 'diamond'):
        return diamond(state,valid,formulae)
    elif(formulae.data == 'box'):
        return box(state,valid,formulae)
    elif(formulae.data == 'loc_exp'):
        return loc_exp(state,valid,formulae)
    elif(formulae.data == 'symbol'):
        return symbol(state,valid,formulae)
    elif(formulae.data == 'true'):
        return True
    elif(formulae.data == 'false'):
        return False

def diamond(state, valid, formulae):  
    path = formulae.children[0]
    exp = formulae.children[1]
    
    jani_program, properties = stormpy.parse_jani_model(path)
    model = stormpy.build_model(jani_program, properties)
    print_model_info(model)
    
    if valid:
        if not networkExecutes(model):
            return False 

        #Updates State Tree
        new_state = StateTree(jani_program)
        state.children.append(new_state)

        if has_modality(exp):    
            return solve(new_state,True,exp)
        else:
            model_check_result = model_check_storm(jani_program,exp)
            return bool(model_check_result)     ## Probability != 0 => True
    else:
        #~(<spn> expression) == [spn] ~expression
        return 

def box(state, valid, formulae):    
    path = formulae.children[0]
    exp = formulae.children[1]

    jani_program, properties = stormpy.parse_jani_model(path)
    model = stormpy.build_model(jani_program, properties)
    print_model_info(model)

    if valid:
        if not networkExecutes(model):
            return False 

        #Updates State Tree
        new_state = StateTree(jani_program)
        state.children.append(new_state)

        if has_modality(exp):    
            return solve(new_state,True,exp)
        else:
            model_check_result = model_check_storm(jani_program,exp)
            if model_check_result == 1 or model_check_result == True:
                return True
            else:
                return False
    else:
        ## ~[spn] expression <=> <spn> ~(expression)
        return

def print_model_info(model):
    print("Model - Storm Output:")
    print("\tNumber of states: {}".format(model.nr_states))
    print("\tNumber of transitions: {}".format(model.nr_transitions))
    print("\tLabels: {}".format(model.labeling.get_labels()))

def has_modality(formulae):
    if isinstance(formulae,Token):  #Ignore Tokens
        return False

    if formulae.data == "diamond" or formulae.data == "box":
       return True
    
    for index in range(len(formulae.children)):
        if has_modality(formulae.children[index]):
            return True 
    return False

def model_check_storm(program, formulae):
    """ 
        Transforms the Syntax Tree into a Storm formula to avaliate Final(deadlock) states 
        Returns boolean (quali) or float (quanti) result
    """
    
    storm_formula = "P=? [true U ({}) & \"deadlock\"]".format(ast_to_string(formulae))
    print("Storm - Check Property: " + storm_formula)

    properties = stormpy.parse_properties_for_jani_model(storm_formula,program)
    model = stormpy.build_model(program, properties)
    results_for_all_states = stormpy.check_model_sparse(model, properties[0])
    
    initial_state = model.initial_states[0]
    result = results_for_all_states.at(initial_state)
    print("\t\tResult: {}".format(result))

    return result

def networkExecutes(model):
    #TO DO - Evolve the condition: How to verify if the network executes?
    return model.nr_states > 1

def ast_to_string(ast):
    """ 
        Syntax Tree to String conversion
    """ 

    if isinstance(ast, Token):
        return ast    

    if len(ast.children) == 0:
        if ast.data == "true":
            return "true"
        if ast.data == "false":
            return "false"

    if len(ast.children) == 1:
        if ast.data == "negate":
            return "~ ({})".format(ast_to_string(ast.children[0]))

    if len(ast.children) == 2:
        fst = ast.children[0]
        snd = ast.children[1]

        if ast.data == "conjunction":
            return "({}) & ({})".format(ast_to_string(fst), ast_to_string(snd))
        if ast.data == "disjunction":
            return "({}) | ({})".format(ast_to_string(fst), ast_to_string(snd))
        if ast.data.data == "implication":
            return "({}) -> ({})".format(ast_to_string(fst), ast_to_string(snd))
        if(ast.data == 'diamond'):
            return "<{}> ({})".format(ast_to_string(fst), ast_to_string(snd))
        if(ast.data == 'box'):
            return "[{}] ({})".format(ast_to_string(fst), ast_to_string(snd))
        
    return ast_to_string(ast.children[0])    

def implication(state, valid, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,False,lhs) or solve(state,True,rhs)
    else:
        return solve(state,True,lhs) and solve(state,False,rhs)

def disjunction(state,valid,formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,True,lhs) or solve(state,True,rhs)
    else:
        return solve(state,False,lhs) and solve(state,False,rhs)

def conjunction(state,valid,formulae):   
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if valid:
        return solve(state,True,lhs) and solve(state,True,rhs)
    else:
        return solve(state,False,lhs) or solve(state,False,rhs)

def negate(state,valid,formulae):
    return solve(state,not valid, formulae.children[0])

def symbol(state,valid,formulae):
    return valid_on_state(state,formulae) if valid else not valid_on_state(state,formulae)

def loc_exp(state,valid,formulae):
    program = state.jani_program
    if not program:
        print("This formula can't be resolved without an associated Stochastic Petri Net")
        return
    else: 
        storm_formula = syntax_tree_to_string(formulae)
        result = model_check_storm(program,storm_formula)
        return result if valid else not result

def valid_on_state(state,symbol):
    ## TO DO
    # (Future) Change to Value Function passed as parameter
    #       return symbol in valor_function(state)
    return False