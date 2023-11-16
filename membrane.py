class Membrane:

    def __init__(self, V:list, id:int, parent:int=None, objects:str=''):
        self.alphabet = V
        self.id = id
        self.parent = parent
        self.childs = set()
        self.rules = set()
        self.plasmids = set()
        self.objects = {}
        self.add_objects(objects)

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
        #suma = sum([objects.count(v) for v in self.V])
        #if suma != len(objects):
        suma = 0
        prev_objs = self.objects
        for obj in self.alphabet:
            count = objects.count(obj)
            self.objects[obj] = self.objects.get(obj, 0) + count
            suma = suma + count
        if suma != len(objects):
            self.objects = prev_objs
            print(f'Objects given not in alphabet({self.alphabet})')
