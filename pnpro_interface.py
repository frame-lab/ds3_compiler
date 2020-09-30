from lark import Lark
import xml.etree.ElementTree as ET
    
## Subnet
def check_subnet_stopped_storm_formula(subnet, pnpro_file):
    # Entire network
    if subnet.children[0] == "@":
        return ' \"deadlock\" '

    trans = []
    transitions = get_transitions_from_subnet(subnet)
    for transition in transitions:
        trans.append(check_transition_disabled_storm_formula(transition, pnpro_file))
    
    return ' & '.join([f'({t})' for t in trans])

def get_transitions_from_subnet(subnet):
    transitions = []
    for transition in subnet.children:
        transitions.append(transition.children[0].value)
    return transitions

def get_transition_preset(transition_name, pnpro_file):
    tree = ET.parse(pnpro_file)
    root = tree.getroot()

    preset = []
    for arc in root.findall(f".//arc[@kind='INPUT'][@head='{transition_name}']"):
        preset.append(arc.attrib['tail'])
    
    return preset

def check_transition_disabled_storm_formula(transition_name, pnpro_file):    
    preset = get_transition_preset(transition_name, pnpro_file)

    return ' | '.join([p + '<=0' for p in preset])


## Markup

def set_markup(markup, orig, dest):
    tree = ET.parse(orig)
    root = tree.getroot()

    markings = get_markings_from_markup(markup)    
    for node in markings:
        set_place_marking(node['place'], node['marking'], root)
    
    tree.write(dest)

def get_markings_from_markup(markup):
    markings = []
    for marking in markup.children:
        node = { 
            'place': marking.children[0].value,
            'marking': marking.children[1].value 
        }
        markings.append(node)
    return markings

def set_place_marking(place_name, marking, root):
    place = root.find(f".//place[@name='{place_name}']")
    place.attrib['marking'] = marking