import collections

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
        print(self.p_rules)

    def add_child(self, child:int):
        '''
        Add child to the membrane.

        :param child: child's id
        :type child: int

        '''
        self.childs.add(child)
        self.rhs_alphabet.add(str(child))
    
    def add_plasmids(self, plasmids:list):
        '''
        Add plasmid to the membrane.

        :param plasmids: list of plasmids' id 
        :type plasmids: list

        '''
        for plasmid in plasmids:
            self.rules.add(plasmid)
    
    def add_objects(self, objects:str):
        '''
        Add objects to the membranes.

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
        applicable_rules = [r for r in self.rules if self.is_feasible(r)]
        promising = []
        #print(self.rules)
        for r in applicable_rules: 
            # comprueba las prioridades de las reglas
            cond = True
            for r1, r2 in self.p_rules:
                if r2 == r and self.is_feasible(r1):
                    cond = False
            if cond: promising.append(r)

        # comprobar que no haya conflicto entre reglas
            # es decir que si una regla es a -> x y otra es a -> b, que solo se aplique una
        
        feasible = self.solve_conflicts(promising)
        #feasible = promising
        # print(f"aplicables: {applicable_rules}")
        # print(f"promesas: {promising}")
        #print(f"{self.id} {feasible}")
        # cambiar a feasible cuando solve conflicts devuelva correctamente lo q toca
        return feasible


    def solve_conflicts(self, promising):
        # hacer backtracking aqui para sacar las posibles variaciones
        feasible = []
        conflictive = collections.defaultdict(set)

        for r1 in promising:
            cond = True
            for r2 in promising:
                # de esta forma no mete ninguna, tiene q meter una en una solucion y la otra en otra
                key = self.conflict(r1, r2)
                if r1 != r2 and key != None:
                    conflictive[key].add(r1)
                    conflictive[key].add(r2)
                    cond = False
                    break
            # if cond: feasible.append(r1)
            feasible.append(r1)
        print(f"conflictivas: {conflictive}")
        #print(feasible)
        return feasible

    def conflict(self, rule1, rule2):
        lhs1, _ = self.rules[rule1]
        lhs2, _ = self.rules[rule2]
        
        lhs_min_len, lhs_max_len = (lhs1, lhs2) if len(lhs1) <= len(lhs2) else (lhs2, lhs1)

        for a in lhs_min_len:
            if a in lhs_max_len:
                return a
        return None
    
    """ 
    def feasible_rules(self):
        '''
        Get the feasible rules from the membrane.

        :return feasible_r

        '''
        aux = {}

        non_feasible = set()
        for i1, i2 in self.p_rules:
            if self.is_feasible(i1):
                non_feasible.add(i2)

        print(non_feasible)
        
        # corregir puede estar una regla (r1, r3) y luego (r2, r1)
        def check_prio(n_feasible, rule):
            for i1, i2 in self.p_rules:
                if i1 == rule: return True
                elif i2 == rule: 
                    if i1 in n_feasible and i2 not in n_feasible: return True
                    else: return False
            return True

        def promising(feasible, n_feasible, rule):
            if (rule not in feasible) and (rule not in n_feasible) and self.is_feasible(rule) and check_prio(n_feasible, rule):
                for l in self.alphabet:
                    if aux.get(l,0) + self.rules[rule][0].count(l) <= self.objects[l]:
                        aux[l] = aux.get(l,0) + self.rules[rule][0].count(l)
                    else: return False
                return True
            else: return False

        def backtracking(feasible, n_feasible, index):
            if index > len(self.rules.keys()): # if completo
                # if factible ?
                yield feasible.copy()
            else:
                # if index not in feasible_r and index not in non_feasible and self.is_feasible(index):
                if promising(feasible, n_feasible, index):
                    feasible.add(index)
                    yield from backtracking(feasible, n_feasible, index + 1)
                    for l in self.alphabet:
                        aux[l] = aux.get(l,0) - self.rules[index][0].count(l)
                    feasible.pop()
                else:
                    n_feasible.add(index)
                yield from backtracking(feasible, n_feasible, index + 1)

        # for rule in self.rules.keys():
        #     if rule not in feasible_r and rule not in non_feasible and self.is_feasible(rule):
        #         feasible_r.add(rule)
        # return feasible_r
        yield from backtracking(set(), non_feasible, 1) """
    
    def is_feasible(self, rule):
        '''
        Get if a rule is feasible.

        :return boolean

        '''
        for obj in self.alphabet:
            if self.objects[obj] < self.rules[rule][0].count(obj):
                return False
        for obj in self.rules[rule][1]:
            if obj not in self.rhs_alphabet:
                return False
        return True