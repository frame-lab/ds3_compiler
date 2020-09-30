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

    #Calls ast_to_string recursion to child
    rec_child = lambda x : ast_to_string(ast.children[x])

    if isinstance(ast, Token):
        return ast    

    # No children
    if ast.data == "true":
        return "true"
    if ast.data == "false":
        return "false"

    # Unary
    if ast.data == "negate":
        return "! ({})".format(rec_child(0))

    # Binary
    if ast.data == "conjunction":
        return "({}) & ({})".format(rec_child(0), rec_child(1))
    if ast.data == "disjunction":
        return "({}) | ({})".format(rec_child(0), rec_child(1))
    if ast.data == "implication":
        return "({}) => ({})".format(rec_child(0), rec_child(1))
    if ast.data == "marking":
        return "{}={}".format(rec_child(0), rec_child(1))
    
    # Trinary
    if(ast.data == 'diamond'):
        return "< {} ; {} > ({})".format(rec_child(0), rec_child(1), rec_child(2))
    if(ast.data == 'box'):
        return "[ {} ; {} ] ({})".format(rec_child(0), rec_child(1), rec_child(2))
    
    # N-ary
    if ast.data in ("markup", "subnet"):
        processed_children = [ rec_child(i) for i in range(len(ast.children)) ]
        return ', '.join(processed_children)

    return rec_child(0)

def has_modality(ast):
    if isinstance(ast, Token):  #Ignore Tokens
        return False

    if ast.data == "diamond" or ast.data == "box":
       return True
    
    for child in ast.children:
        if has_modality(child):
            return True  
    return False