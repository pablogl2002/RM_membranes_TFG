class Membrane:

    def __init__(self, id:int, parent:int=None, objects:dict={}):
        self.id = id
        self.parent = parent
        self.childs = set()
        self.rules = set()
        self.plasmids = set()
        self.objects = objects

    def add_childs(self, childs:list):
        for child in childs:
            self.childs.add(child)
    
    def add_rules(self, rules:list):
        for rule in rules:
            self.rules.add(rule)
    
    def add_plasmids(self, plasmids:list):
        for plasmid in plasmids:
            self.rules.add(plasmid)
     
