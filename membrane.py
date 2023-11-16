class Membrane:

    def __init__(self, V:list, id:int, parent:int=None, objects:str=''):
        self.alphabet = V
        self.id = id
        self.parent = parent
        self.childs = set()
        self.rules = set()
        self.plasmids = set()
        self.objects = {}
        for obj in V:
            self.objects[obj] = self.objects.get(obj, 0)

    def add_child(self, child:int):
        self.childs.add(child)

    def add_childs(self, childs:list):
        for child in childs:
            self.childs.add(child)
    
    def add_rules(self, rules:list):
        for rule in rules:
            self.rules.add(rule)
    
    def add_plasmids(self, plasmids:list):
        for plasmid in plasmids:
            self.rules.add(plasmid)
    
    def add_objects(self, objects:str):
        suma = sum([objects.count(v) for v in self.V])
        if suma != len(objects):
            pass
