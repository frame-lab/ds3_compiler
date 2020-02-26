import stormpy 

path = '/code/example_models/philosophers.jani'
formula = 'P=? [F eating1=1]'

jani_program, properties = stormpy.parse_jani_model(path)

properties = stormpy.parse_properties_for_jani_model(formula,jani_program)

model = stormpy.build_model(jani_program, properties)

print(model.model_type)

print("Labels: {}".format(model.labeling.get_labels()))