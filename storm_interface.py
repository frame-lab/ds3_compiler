import stormpy
import stormpy.gspn
import sys

import ast_analyzer as ast

""" Storm Interface Module """

def model_check_storm(network, formula):
    """ 
        Uses Storm Checker to verify DS3 formula

        Network: SPN codified in PNPRO or JANI
        Formula: String or AST Formula
        
        Returns boolean (quali) or float (quanti) result
    """
    
    program = get_jani_program(network)    

    print("Storm - Check Property: " + formula)
    try:
        result = storm_check(program, formula)
        print(f"\t\tResult: {result}\n")
        return result
    except:
        error_message = sys.exc_info()[1].args[0]
        if "Parsing error" in error_message:
            print("Please, verify if all place names are correct.")
            exit()
        else:
            raise

def network_executes_and_stops(network, stop_condition=' \"deadlock\" '):
    """ Verifies if network executes and stops """
    
    program = get_jani_program(network)    

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