import random

class Membrane:

    def __init__(self, V, id:int, parent:int=None, objects:str='', rules:list=[], p_rules:list=[]):
        self.alphabet = V
        self.id = id
        self.parent = parent
        self.childs = set()
        self.rules_id = 0
        self.rules = {}
        self.p_rules = p_rules
        self.plasmids = set()
        self.objects = {}
        self.rhs_alphabet = V.copy()

        self.rhs_alphabet.add('0')
        self.rhs_alphabet.add('.')

        self.add_objects(objects)
        self.add_rules(rules)

    # para eliminar entradas de plasmidos en rules añadir set ids_reglas plasmidos y con rules.pop(id) o rules.del(id) se elimina la entrada al dict

    def add_child(self, child:int):
        self.childs.add(child)
        self.rhs_alphabet.add(str(child))
    
    def add_rules(self, rules:list):
        for rule in rules:
            self.rules_id = self.rules_id + 1
            self.rules[self.rules_id] = self.rules.get(self.rules_id, rule)
        
    def add_plasmids(self, plasmids:list):
        for plasmid in plasmids:
            self.rules.add(plasmid)
    
    def add_objects(self, objects:str):
        if len(objects) != 0:
            self.empty = False
        suma = 0
        prev_objs = self.objects
        for obj in self.alphabet:
            count = objects.count(obj)
            self.objects[obj] = self.objects.get(obj, 0) + count
            suma = suma + count
        if suma != len(objects):
            self.objects = prev_objs
            print(f'Objects given not in alphabet({self.alphabet})')

    def feasible_rules(self):
        feasible_r = set()
        
        for rule in self.rules.keys():
            aux = True
            for obj in self.alphabet:
                if self.objects[obj] < self.rules[rule][0].count(obj):
                    aux = False
                    break
            if aux:
                for obj in self.rules[rule][1]:
                    if obj not in self.rhs_alphabet:
                        aux = False
                        break
            if aux: feasible_r.add(rule)
        return feasible_r
        