import stormpy 

path = '/code/example_models/philosophers.jani'

properties = { 
    
}

jani_program, properties = stormpy.parse_jani_model(path)

print(properties)

#model = stormpy.build_model(jani_program, properties)

#print(model.model_type)

#print("Labels: {}".format(model.labeling.get_labels()))