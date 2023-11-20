import random

class Membrane:

    def __init__(self, V, id:int, parent:int=None, objects:str='', rules={}, p_rules={}):
        '''
        Membrane class constructor.

        :param V: Membrane's alphabet (same as system's)
        :type V: list

        :param id: Membrane's id
        :type id: int

        :param parent: Parent Membrane's id
        :type parent: int

        :param objects: Membrane's objects
        :type objects: str

        :param rules: Membrane's rules
        :type rules: dict -> key: rule_id, value:list = tuple (lhs, rhs)

        :param p_rules: rules priority in membrane
        :type p_rules: list

        '''
        self.alphabet = V               # membrane's alphabet
        self.id = id                    # membrane's id
        self.parent = parent            # parent's id
        self.childs = set()             # childs' ids set list
        self.rules = rules              # rules' dict
        self.p_rules = p_rules          # rules' priority dict
        self.plasmids = set()           # plasmids' set list
        self.objects = {}               # membrane object's dict
        self.rhs_alphabet = V.copy()    # rhs rules' alphabet

        self.rhs_alphabet.add('0')  # se añade al alfabeto de la parte derecha un 0 para sacar objeto
        self.rhs_alphabet.add('.')  # se añade al alfabeto de la parte derecha un . para disolver membrana

        # se añaden los objetos iniciales a la membrana
        self.add_objects(objects)

    def add_child(self, child:int):
        '''
        Add child to the membrane

        :param child: child's id
        :type child: int

        '''
        self.childs.add(child)
        self.rhs_alphabet.add(str(child))
    
    def add_plasmids(self, plasmids:list):
        '''
        Add plasmid to the membrane

        :param plasmids: list of plasmids' id 
        :type plasmids: list

        '''
        for plasmid in plasmids:
            self.rules.add(plasmid)
    
    def add_objects(self, objects:str):
        '''
        Add objects to the membranes

        :param objects: objects to add in the membrane
        :type objects: str

        '''
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
        '''
        Get the feasible rules from the membrane

        :return feasible_r

        '''
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
        '''
        Get if a rule is feasible

        :return boolean

        '''
        for obj in self.alphabet:
            if self.objects[obj] < self.rules[rule][0].count(obj):
                return False
        for obj in self.rules[rule][1]:
            if obj not in self.rhs_alphabet:
                return False
        return True