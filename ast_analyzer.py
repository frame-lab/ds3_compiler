from lark import Token

""" DS3 AST Analyzer Module"""

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

def ast_to_string(ast):
    """ 
        Abstract Syntax Tree to String conversion
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
            return "({}) => ({})".format(ast_to_string(fst), ast_to_string(snd))
        if(ast.data == 'diamond'):
            return "<{}> ({})".format(ast_to_string(fst), ast_to_string(snd))
        if(ast.data == 'box'):
            return "[{}] ({})".format(ast_to_string(fst), ast_to_string(snd))
        
    return ast_to_string(ast.children[0])

def has_modality(ast):
    if isinstance(ast, Token):  #Ignore Tokens
        return False

    if ast.data == "diamond" or ast.data == "box":
       return True
    
    for child in ast.children:
        if has_modality(child):
            return True  
    return False