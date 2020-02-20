import stormpy.examples
import stormpy.examples.files

path = stormpy.examples.files.prism_dtmc_die
prism_program = stormpy.parse_prism_program(path)

model = stormpy.build_model(prism_program)
print("Number of states: {}".format(model.nr_states))

print("Labels: {}".format(model.labeling.get_labels()))