import stormpy
import stormpy.gspn

import ast_analyzer as ast

""" Storm Interface Module """

def get_jani_program(path):
    """ Receives SPN codified in JANI or PNPRO and returns a JANI Model """

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

def model_check_storm(program, formula, final_states=False):
    """ 
        Uses Storm Checker to verify DS3 formula

        Program: Jani Program
        Formula: String or AST Formulae
        Final States: Boolean

        Returns boolean (quali) or float (quanti) result
    """

    if final_states:
        formula = f"P=? [true U ({formula}) & \"deadlock\"]"
        
    print("Storm - Check Property: " + formula)
    result = storm_check(program, formula)
    print(f"\t\tResult: {result}\n")

    return result

def network_executes_and_stops(program, stop_condition=' \"deadlock\" '):
    """ Verifies if network executes and stops """
    
    #Stops?
    result = storm_check(program, f"P=? [true U ({stop_condition})]")
    if result == 0:
        print("The given SPN does not stop. DS3 Checker was not designed to deal with this use case.\n")
        exit()
    
    #Executes?
    model = stormpy.build_model(program)
    if model.nr_states <= 1:
        print("Network doesn't have possible execution.\n")
        return False
    
    return True

def storm_check(program, formula):
    """ Model Checks formula(string) over model """

    properties = stormpy.parse_properties_for_jani_model(formula, program)
    model = stormpy.build_model(program, properties)
    results_for_all_states = stormpy.check_model_sparse(model, properties[0])
    initial_state = model.initial_states[0]
    result = results_for_all_states.at(initial_state)
    
    return result