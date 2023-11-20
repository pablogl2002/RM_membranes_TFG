import random

class Membrane:

    def __init__(self, V, id:int, parent:int=None, objects:str='', rules={}, p_rules={}):
        self.alphabet = V
        self.id = id
        self.parent = parent
        self.childs = set()
        self.rules_id = 0
        self.rules = rules
        self.p_rules = p_rules
        self.plasmids = set()
        self.objects = {}
        self.rhs_alphabet = V.copy()

        self.rhs_alphabet.add('0')
        self.rhs_alphabet.add('.')

        self.add_objects(objects)

    def add_child(self, child:int):
        self.childs.add(child)
        self.rhs_alphabet.add(str(child))
    
    def add_plasmids(self, plasmids:list):
        for plasmid in plasmids:
            self.rules.add(plasmid)
    
    def add_objects(self, objects:str):
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
        non_feasible = set()
        for i1, i2 in self.p_rules:
            if self.is_feasible(i1):
                feasible_r.add(i1)
                non_feasible.add(i2)
            else:
                non_feasible.add(i1)

        for rule in self.rules.keys():
            if rule not in feasible_r and rule not in non_feasible and self.is_feasible(rule):
                feasible_r.add(rule)
        return feasible_r
    
    def is_feasible(self, rule):
        for obj in self.alphabet:
            if self.objects[obj] < self.rules[rule][0].count(obj):
                return False
        for obj in self.rules[rule][1]:
            if obj not in self.rhs_alphabet:
                return False
        return True