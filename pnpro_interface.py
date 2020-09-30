from lark import Lark
import xml.etree.ElementTree as ET
    
def update_spn(markup, subnet, orig, dest):
    tree = ET.parse(orig)
    root = tree.getroot()

    set_markup(markup, root)
    extract_subnet(subnet, root)    

    tree.write(dest)

def extract_subnet(subnet, root):
    #Use entire network
    if subnet.children[0] == "@":
        return

    subnet_transition_names = map(lambda transition : transition.children[0].value, subnet.children)
    
    transitions = root.findall(".//transition")
    for transition in transitions:
        if transition.get('name') not in subnet_transition_names:
            remove_transition(transition.get('name'), root)

def remove_transition(transition_name, root):
    #Remove Transition
    nodes = root.find(".//nodes")
    transition = nodes.find(f"./transition[@name='{transition_name}']")
    nodes.remove(transition)

    # Remove related Edges
    edges = root.find(".//edges")
    input_arcs = edges.findall(f"./arc[@head='{transition_name}']")
    remove_arcs = edges.findall(f"./arc[@tail='{transition_name}']")
    arcs = input_arcs + remove_arcs
    
    for arc in arcs:
        edges.remove(arc)

def set_markup(markup, root):
    markings = get_markings_from_markup(markup)    
    for node in markings:
        set_place_marking(node['place'], node['marking'], root)

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