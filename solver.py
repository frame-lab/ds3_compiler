import storm_interface as storm
import ast_analyzer as ast
import pnpro_interface as pnpro

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
    markup = formulae.children[0]
    subnet = formulae.children[1]
    exp = formulae.children[2]
    
    #Generates Marked SPN
    marked_spn = "temp/aux.PNPRO"     #TODO: generates unique dest path for SPNs
    pnpro.set_markup(markup, state.network, marked_spn)
    jani_program = storm.get_jani_program(marked_spn)

    #Generates Stop Condition
    stopped = pnpro.check_subnet_stopped_storm_formula(subnet, state.network)
        
    #TODO: Should this function be here or inside of model_check_storm?
    # Treat subnets that don't stop as an exception?
    if not storm.network_executes_and_stops(jani_program, stopped):
        print("Network does not executes and stops. So modality is false\n")
        return False

    #Updates State Tree
    new_state = StateTree(state.network)
    state.append_child(new_state)

    if ast.has_modality(exp):    
        return solve(new_state, exp)
    else:
        # GENERATES CSL Formula
        csl_formula = f"P=? [true U ({ast.ast_to_string(exp)}) & ({stopped})]"

        model_check_result = storm.model_check_storm(jani_program, csl_formula)
        return bool(model_check_result)     ## Probability != 0 => True

def box(state, formulae):    
    markup = formulae.children[0]
    subnet = formulae.children[1]
    exp = formulae.children[2]
    
    #Generates Marked SPN
    marked_spn = "temp/aux.PNPRO"     #TODO: generates unique dest path for SPNs
    pnpro.set_markup(markup, state.network, marked_spn)
    jani_program = storm.get_jani_program(marked_spn)

    #Generates Stop Condition
    stopped = pnpro.check_subnet_stopped_storm_formula(subnet, state.network)
        
    #TODO: Should this function be here or inside of model_check_storm?
    # Treat subnets that don't stop as an exception?
    if not storm.network_executes_and_stops(jani_program, stopped):
        print("Network does not executes and stops. So modality is false\n")
        return False

    if ast.has_modality(exp):    
        return solve(state, exp)
    else:
        # GENERATES CSL Formula
        csl_formula = f"P=? [true U ({ast.ast_to_string(exp)}) & ({stopped})]"

        model_check_result = storm.model_check_storm(jani_program, csl_formula)
        return model_check_result == 1

def loc_exp(state, formulae):
    if not state.network:
        print("Markup Expressions can't be resolved without an associated Stochastic Petri Net")
        exit()
    else: 
        jani_program = storm.get_jani_program(state.network)
        result = storm.model_check_storm(jani_program, formulae)
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
    
    if ast.is_tree_equivalent(t1, t2):
        return True
    else:
        return False