from lark import Lark

import xml.etree.ElementTree as ET
    
#Sub-rede
def check_subnet_stopped_storm_formula(subnet, pnpro_file):
    # Entire network
    if subnet.children[0] == "@":
        return ' \"deadlock\" '

    transitions = get_transitions_from_subnet(subnet)

    trans = []
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

    #Collects Transition Preset
    preset = []
    for arc in root.findall(f".//arc[@kind='INPUT'][@head='{transition_name}']"):
        preset.append(arc.attrib['tail'])
    
    return preset

def get_transition_postset(transition_name, pnpro_file):
    tree = ET.parse(pnpro_file)
    root = tree.getroot()

    #Collects Transition Preset
    preset = []
    for arc in root.findall(f".//arc[@kind='OUTPUT'][@tail='{transition_name}']"):
        preset.append(arc.attrib['head'])
    
    return preset

def check_transition_enabled_storm_formula(transition_name, pnpro_file):    
    preset = get_transition_preset(transition_name, pnpro_file)

    return ' & '.join([p + '>0' for p in preset])


def check_transition_disabled_storm_formula(transition_name, pnpro_file):    
    preset = get_transition_preset(transition_name, pnpro_file)

    return ' | '.join([p + '<=0' for p in preset])


#Marcação

def set_markup(markup, orig, dest):
    markings = get_markings_from_markup(markup)

    tree = ET.parse(orig)
    root = tree.getroot()

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

    print(place.attrib['marking'])

def get_place_marking(place_name, marking, root):
    place = root.find(f".//place[@name='{place_name}']")
    
    if 'marking' in place.attrib.keys():
        return place.attrib['marking']
    return 0

