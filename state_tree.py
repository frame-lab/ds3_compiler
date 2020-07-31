class StateTree:
    stateCount = 0

    @classmethod
    def incrementStateCount(cls):
        cls.stateCount += 1        

    def __init__(self, network= None, name= None):
        if name:
            self.name = name
        else:
            self.name = "w" + str(self.stateCount)
        
        self.incrementStateCount()
        self.network = network
        self.children = []
    
    def append_child(self, node):
        if isinstance(node, StateTree):
            self.children.append(node)