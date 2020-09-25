import ast_analyzer as ast
import pnpro_interface as pnpro
import storm_interface as storm

from state_tree import StateTree

def solve(state, formula):    
    formula_string = ast.ast_to_string(formula)
    print(f"Solving:\n  State: {state.name}\n  Formula: \"{formula_string}\"\n  Waiting for result...\n")

    if(formula.data == 'conjunction'):
        result = conjunction(state, formula)
    elif(formula.data == 'disjunction'):
        result = disjunction(state, formula)
    elif(formula.data == 'implication'):
        result = implication(state, formula)
    elif(formula.data == 'negate'):
        result = negate(state, formula)
    elif(formula.data == 'diamond'):
        result = diamond(state, formula)
    elif(formula.data == 'box'):
        result = box(state, formula)
    elif(formula.data == 'loc_exp'):
        result = loc_exp(state, formula)
    elif(formula.data == 'true'):
        result = True
    elif(formula.data == 'false'):
        result = False

    print(f"Formula \"{formula_string}\" is {result} \n")
    return result

def conjunction(state, formula):
    lhs = formula.children[0]
    rhs = formula.children[1]

    if are_contradictions(lhs,rhs):
        print("Third Excluded Law applied.\nFormula is a Contradiction")
        return False
    
    return solve(state, lhs) and solve(state, rhs)

def disjunction(state, formula):
    lhs = formula.children[0]
    rhs = formula.children[1]

    if are_contradictions(lhs,rhs):
        print("Third Excluded Law applied.\nFormula is a Contradiction\n")
        return True
    
    return solve(state, lhs) or solve(state, rhs)

def implication(state, formula):
    lhs = formula.children[0]
    rhs = formula.children[1]

    return (not solve(state, lhs)) or solve(state, rhs)
            
def negate(state, formula):
    return not solve(state, formula.children[0])

def diamond(state, formula):  
    markup = formula.children[0]
    subnet = formula.children[1]
    exp = formula.children[2]
    
    #Generates Marked SPN
    marked_spn = "temp/aux.PNPRO"     #TODO: generates unique dest path for SPNs
    pnpro.set_markup(markup, state.network, marked_spn)
    jani_program = storm.get_jani_program(marked_spn)

    #Generates Stop Condition
    stopped = pnpro.check_subnet_stopped_storm_formula(subnet, state.network)
        
    if not storm.network_executes_and_stops(jani_program, stopped):
        print("Network does not executes and stops. So modality is false\n")
        return False

    #Updates State Tree
    new_state = StateTree(state.network)
    state.append_child(new_state)

    if ast.has_modality(exp):    
        return solve(new_state, exp)
    else:
        csl_formula = f"P=? [true U ({ast.ast_to_string(exp)}) & ({stopped})]"

        model_check_result = storm.model_check_storm(jani_program, csl_formula)
        return bool(model_check_result)     ## Probability != 0 => True

def box(state, formula):    
    markup = formula.children[0]
    subnet = formula.children[1]
    exp = formula.children[2]
    
    #Generates Marked SPN
    marked_spn = "temp/aux.PNPRO"     #TODO: generates unique dest path for SPNs
    pnpro.set_markup(markup, state.network, marked_spn)
    jani_program = storm.get_jani_program(marked_spn)

    #Generates Stop Condition
    stopped = pnpro.check_subnet_stopped_storm_formula(subnet, state.network)
        
    if not storm.network_executes_and_stops(jani_program, stopped):
        print("Network does not executes and stops. So modality is false\n")
        return False

    if ast.has_modality(exp):    
        return solve(state, exp)
    else:
        csl_formula = f"P=? [true U ({ast.ast_to_string(exp)}) & ({stopped})]"

        model_check_result = storm.model_check_storm(jani_program, csl_formula)
        return model_check_result == 1

def loc_exp(state, formula):
    if not state.network:
        print("Markup Expressions can't be resolved without an associated Stochastic Petri Net")
        exit()
    else: 
        jani_program = storm.get_jani_program(state.network)
        result = storm.model_check_storm(jani_program, formula)
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