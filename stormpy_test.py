import stormpy 

path = '/code/example_models/philosophers.jani'
formula = 'P=? [F eating1=1]'

jani_program, properties = stormpy.parse_jani_model(path)

properties = stormpy.parse_properties_for_jani_model(formula,jani_program)
#properties.append() = stormpy.parse_properties_for_jani_model(formula,jani_program)


model = stormpy.build_model(jani_program, properties)

print("Number of states: {}".format(model.nr_states))
print("Number of transitions: {}".format(model.nr_transitions))
print("Labels: {}".format(model.labeling.get_labels()))


sparse_result = stormpy.check_model_sparse(model, properties[0])
initial_state = model.initial_states[0]

print("Results:")
print(sparse_result.at(initial_state))

#result = stormpy.model_checking(model,properties[0])
#print(type(result))

# get_labels => Marcação da rede
# Posso perguntar se existe um estado em que todos os estados seguintes o retorno de get_labels é igual
# Exemplo da formula para perguntar:
#   AG labels = x U EF (AG labels = x)
# Lembrando que eu suponho que toda rede para

# for state in model.states:
#   for action in state.actions:
#     for transition in action.transitions:
#       print("From state {}, with probability {}, go to state {}".format(state, transition.value(), transition.column)) 