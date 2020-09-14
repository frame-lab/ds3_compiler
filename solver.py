import storm_interface as storm
import ast_analyzer as ast

from state_tree import StateTree

def solve(state, formulae):    
    formulae_string = ast.ast_to_string(formulae)
    print(f"Solving:\n  State: {state.name}\n  Formula: \"{formulae_string}\"\n  Waiting for result...\n")

    result = None

    if(formulae.data == 'conjunction'):
        result = conjunction(state, formulae)
    elif(formulae.data == 'disjunction'):
        result = disjunction(state, formulae)
    elif(formulae.data == 'implication'):
        result = implication(state, formulae)
    elif(formulae.data == 'negate'):
        result = negate(state, formulae)
    elif(formulae.data == 'diamond'):
        result = diamond(state, formulae)
    elif(formulae.data == 'box'):
        result = box(state, formulae)
    elif(formulae.data == 'loc_exp'):
        result = loc_exp(state, formulae)
    elif(formulae.data == 'true'):
        result = True
    elif(formulae.data == 'false'):
        result = False

    print(f"Formula \"{formulae_string}\" is {result} \n")
    return result

def conjunction(state, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if are_contradictions(lhs,rhs):
        print("Third Excluded Law applied.\nFormulae is a Contradiction")
        return False
    
    return solve(state, lhs) and solve(state, rhs)

def disjunction(state, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if are_contradictions(lhs,rhs):
        print("Third Excluded Law applied.\nFormulae is a Contradiction\n")
        return True
    
    return solve(state, lhs) or solve(state, rhs)

def implication(state, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    return (not solve(state, lhs)) or solve(state, rhs)
            
def negate(state, formulae):
    return not solve(state, formulae.children[0])
    # exp = storm.ast_to_string(formulae.children[0])
    # exp_result = solve(state, formulae.children[0])
    # result = not exp_result
    # print(f"Since {exp} : {exp_result}\nApplying negate: {result}")
    # return result

def diamond(state, formulae):  
    path = formulae.children[0]
    exp = formulae.children[1]
    
    jani_program = storm.get_jani_program(path)

    if not storm.network_executes_and_stops(jani_program):
        print("Network does not executes and stops. So modality is false\n")
        return False

    #Updates State Tree
    new_state = StateTree(path)
    state.append_child(new_state)

    if ast.has_modality(exp):    
        return solve(new_state, exp)
    else:
        model_check_result = storm.model_check_storm(jani_program, exp, final_states=True)
        return bool(model_check_result)     ## Probability != 0 => True

def box(state, formulae):    
    path = formulae.children[0]
    exp = formulae.children[1]

    jani_program = get_jani_program(path)

    if not network_executes_and_stops(jani_program):
        print("Network does not executes and stops. So modality is false")
        return False 

    if has_modality(exp):    
        return solve(state, exp)
    else:
        model_check_result = model_check_storm(jani_program, exp, final_states=True)
        return model_check_result == 1

def loc_exp(state, formulae):
    if not state.network:
        print("Markup Expressions can't be resolved without an associated Stochastic Petri Net")
        exit()
    else: 
        jani_program = get_jani_program(state.network)
        result = model_check_storm(jani_program, formulae)
        return result

def are_contradictions(t1, t2):
    """ Detects if t1 and t2 are contradictions.
            Ex.: ((A & B) & (C & D)) & !((B & A) & (D & C))
        IMPORTANT: The function is not exhaustive. 
                    If are_contradictions(n1, n2) => n1 and n2 are contradictions
                    If not are_contradictions(n1, n2) => nothing can be affirmed
    """
    if t1.data == "negate":
        t1 = t1.children[0]
    elif t2.data == "negate":
        t2 = t2.children[0]
    else:
        return False
    
    if is_tree_equivalent(t1, t2):
        return True
    else:
        return False