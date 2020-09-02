import stormpy
import stormpy.gspn
from state_tree import StateTree
from lark import Token
from lark import Tree as LarkTree
from ds3_parser import ds3_parser

def solve(state, formulae):    
    formulae_string = ast_to_string(formulae)
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
    elif(formulae.data == 'symbol'):
        result = symbol(state, formulae)
    elif(formulae.data == 'true'):
        result = True
    elif(formulae.data == 'false'):
        result = False

    print(f"Formula \"{formulae_string}\" is {result} \n")
    return result

def get_jani_program(path):
    if path.lower().endswith(".jani"):
        jani_program, properties = stormpy.parse_jani_model(path)
        return jani_program
    
    if path.lower().endswith(".pnpro"):
        gspn_parser = stormpy.gspn.GSPNParser()
        gspn = gspn_parser.parse(path)
        jani_builder = stormpy.gspn.GSPNToJaniBuilder(gspn)
        jani_program = jani_builder.build()
        return jani_program
    
    print("Unsupported file format: {}".format(path))
    exit()

def diamond(state, formulae):  
    path = formulae.children[0]
    exp = formulae.children[1]
    
    jani_program = get_jani_program(path)
    model = stormpy.build_model(jani_program)

    if not network_executes(model):
        print("Network has no possible execution\n")
        return False 

    #Updates State Tree
    new_state = StateTree(path)
    state.children.append(new_state)

    if has_modality(exp):    
        return solve(new_state, exp)
    else:
        model_check_result = model_check_storm(jani_program, exp, final_states=True)
        return bool(model_check_result)     ## Probability != 0 => True

def box(state, formulae):    
    path = formulae.children[0]
    exp = formulae.children[1]

    jani_program = get_jani_program(path)
    model = stormpy.build_model(jani_program)

    if not network_executes(model):
        print("Network has no possible execution\n")
        return False 

    if has_modality(exp):    
        return solve(state, exp)
    else:
        model_check_result = model_check_storm(jani_program, exp, final_states=True)
        return model_check_result == 1

def has_modality(formulae):
    if isinstance(formulae,Token):  #Ignore Tokens
        return False

    if formulae.data == "diamond" or formulae.data == "box":
       return True
    
    for child in formulae.children:
        if has_modality(child):
            return True  
    return False

def model_check_storm(program, formulae, final_states=False):
    """ 
        Transforms the Syntax Tree into a Storm formula to avaliate Final(deadlock) states 
        Returns boolean (quali) or float (quanti) result
    """
    
    storm_formula = ast_to_string(formulae)

    if final_states:
        storm_formula = "P=? [true U ({}) & \"deadlock\"]".format(storm_formula)
        
    print("Storm - Check Property: " + storm_formula)

    properties = stormpy.parse_properties_for_jani_model(storm_formula,program)
    model = stormpy.build_model(program, properties)
    results_for_all_states = stormpy.check_model_sparse(model, properties[0])
    
    initial_state = model.initial_states[0]
    result = results_for_all_states.at(initial_state)
    print("\t\tResult: {}\n".format(result))

    return result

def network_executes(model):
    """ 
    Além de verificar que a rede executa eu deveria também verificar que a rede para, 
        ou seja existe algum estado em que a propriedade "deadlock" é verdadeira.
    """

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
            return "! ({})".format(ast_to_string(ast.children[0]))

    if len(ast.children) == 2:
        fst = ast.children[0]
        snd = ast.children[1]

        if ast.data == "conjunction":
            return "({}) & ({})".format(ast_to_string(fst), ast_to_string(snd))
        if ast.data == "disjunction":
            return "({}) | ({})".format(ast_to_string(fst), ast_to_string(snd))
        if ast.data == "implication":
            return "({}) -> ({})".format(ast_to_string(fst), ast_to_string(snd))
        if(ast.data == 'diamond'):
            return "<{}> ({})".format(ast_to_string(fst), ast_to_string(snd))
        if(ast.data == 'box'):
            return "[{}] ({})".format(ast_to_string(fst), ast_to_string(snd))
        
    return ast_to_string(ast.children[0])    

def implication(state, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    return (not solve(state, lhs)) or solve(state, rhs)

def disjunction(state, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if are_contradictions(lhs,rhs):
        print("Third Excluded Law applied.\nFormulae is a Contradiction")
        return True
    
    return solve(state, lhs) or solve(state, rhs)

def conjunction(state, formulae):
    lhs = formulae.children[0]
    rhs = formulae.children[1]

    if are_contradictions(lhs,rhs):
        print("Third Excluded Law applied.\nFormulae is a Contradiction")
        return False
    
    return solve(state, lhs) and solve(state, rhs)

def is_node_equivalent(n1, n2):
    if type(n1) != type(n2):
        return False 
    elif isinstance(n1, Token):
        return n1.replace(" ","") == n2.replace(" ","")
    else:
        return n1.data == n2.data

def is_tree_equivalent(t1, t2):
    if not is_node_equivalent(t1, t2):
        return False
    
    if not isinstance(t1, Token):
        if len(t1.children) != len(t2.children):
            return False
    
        if t1.data in ("conjunction", "disjunction"):
            t1_list = [ item for item in t1.children ]
            t2_list = [ item for item in t2.children ]
            for e1 in t1_list:
                match = False
                for e2 in t2_list:
                    if is_tree_equivalent(e1, e2):
                        match = True
                        t2_list.remove(e2)
                        break
                
                if not match:
                    return False
        else:
            for i in range(0,len(t1.children)):
                if not is_tree_equivalent(t1.children[i], t2.children[i]):
                    return False 

    return True
        
def are_contradictions(t1, t2):
    """ Detects if t1 and t2 are contradictions.
            Ex.: ((A & B) & (C & D)) & !((B & A) & (D & C))
        IMPORTANT: The function is not exhaustive. 
                    If are_contradictions(n1, n2) -> n1 and n2 are contradictions
                    If not are_contradictions(n1, n2) -> nothing can be affirmed
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

def negate(state, formulae):
    return not solve(state, formulae.children[0])
    # exp = ast_to_string(formulae.children[0])
    # exp_result = solve(state, formulae.children[0])
    # result = not exp_result
    # print(f"Since {exp} : {exp_result}\nApplying negate: {result}")
    # return result



def symbol(state, formulae):
    return valid_on_state(state, formulae)

def loc_exp(state, formulae):
    if not state.network:
        print("Markup Expressions can't be resolved without an associated Stochastic Petri Net")
        exit()
    else: 
        jani_program = get_jani_program(state.network)
        result = model_check_storm(jani_program, formulae)
        return result

def valid_on_state(state,symbol):
    ##TODO
    # (Future) Change to Value Function passed as parameter
    #       return symbol in valor_function(state)
    return False