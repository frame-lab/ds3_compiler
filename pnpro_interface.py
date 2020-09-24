from lark import Lark

import xml.etree.ElementTree as ET

#Sub-rede
def check_subnet_stopped_storm_formula(transitions, pnpro_file):
    trans = []
    for transition in transitions:
        trans.append(check_transition_disabled_storm_formula(transition, pnpro_file))
    
    return ' & '.join([f'({t})' for t in trans])

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
    tree = ET.parse(orig)
    root = tree.getroot()

    for node in markup:
        set_place_marking(node['place'], node['marking'], root)
    
    tree.write(dest)

def set_place_marking(place_name, marking, root):
    place = root.find(f".//place[@name='{place_name}']")
    place.attrib['marking'] = marking

    print(place.attrib['marking'])

def get_place_marking(place_name, marking, root):
    place = root.find(f".//place[@name='{place_name}']")
    
    if 'marking' in place.attrib.keys():
        return place.attrib['marking']
    return 0

