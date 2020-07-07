from datetime import datetime

class StateTree:
    def __init__(self, jani_program= None, name= None):
        if name:
            self.name = name
        else:
            self.name = str(datetime.now())
        self.jani_program = jani_program
        self.children = []
    
    def append_child(self, node):
        if isinstance(node, StateTree):
            self.children.append(node)