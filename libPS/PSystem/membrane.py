import collections

class Membrane:

    def __init__(self, V, id:int, parent:int=None, objects:str='', rules={}, p_rules={}):
        """Membrane class constructor.

        Args:
            V (list): Membrane's alphabet (same as system's)
            id (int): Membrane's id
            parent (int, optional): Parent Membrane's id. Defaults to None.
            objects (str, optional): Membrane's objects. Defaults to ''.
            rules (dict, optional): Membrane's rules | key: rule_id, value:list = tuple (lhs, rhs). Defaults to {}.
            p_rules (dict, optional): Rules priority in membrane. Defaults to {}.
        """

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
        """Add child to the membrane.

        Args:
            child (int): child's id
        """

        self.childs.add(child)
        self.rhs_alphabet.add(str(child))
    

    def add_objects(self, objects:str):
        """Add objects to the membranes.

        Args:
            objects (str): objects to add in the membrane
        """

        suma = 0
        prev_objs = self.objects
        for obj in self.alphabet:
            count = objects.count(obj)
            self.objects[obj] = self.objects.get(obj, 0) + count
            suma = suma + count
        if suma != len(objects):
            self.objects = prev_objs
            print(f'Objects given not in alphabet({self.alphabet})')


    # def get_feasible_rules(self):
    #     """Return a combination of rules that can be applied all at once in the membrane

    #     Returns:
    #         list: list of list (due to yields) with feasible rules combinations
    #     """

    #     applicable_rules = [r for r in self.rules if self._is_applicable(r)]   # recoge todas las reglas que se pueden aplicar
    #     promising = []
    #     for r in applicable_rules:
    #         # comprueba las prioridades de las reglas
    #         cond = True
    #         for r1, r2 in self.p_rules:
    #             if r2 == r and self._is_applicable(r1):
    #                 cond = False
    #         if cond: promising.append(r)

    #     # comprueba que no haya conflicto entre reglas
    #         # es decir que si una regla es a -> x y otra es a -> b, que solo se aplique una
    #     feasible = self._solve_conflicts(promising)

    #     return feasible


    # def _solve_conflicts(self, promising):
    #     """Solve the conflicts with the rules in a rules' list

    #     Args:
    #         promising (list): combination of a possible rules

    #     Yields:
    #         list: feasible combination of rules
    #     """

    #     feasible = promising
    #     conflictive = collections.defaultdict(set)

    #     for r1 in promising:
    #         for r2 in promising:
    #             key = self._conflict(r1, r2)
    #             if r1 != r2 and key != None:
    #                 conflictive[key].add(r1)
    #                 conflictive[key].add(r2)
    #                 if r1 in feasible: feasible.remove(r1)
    #                 if r2 in feasible: feasible.remove(r2)
    #                 break     

    #     def is_promising(sol, rule):
    #         for r in sol:
    #             if self._conflict(r, rule): return False
    #         return True

    #     def backtracking(sol):
    #         # if es completo
    #         if len(sol) == len(conflictive.keys()):
    #             yield feasible + sol
    #         else:
    #             # ramificar
    #             for _, rules in conflictive.items():
    #                 for rule in rules:
    #                     # if prometedor
    #                     if is_promising(sol, rule):
    #                         yield from backtracking(sol+[rule])

    #     yield from backtracking([])


    # def _conflict(self, rule1, rule2):
    #     """Checks if two rules have conflicts like 'a'-> 'b' and 'ab' -> 'b', both need an 'a' to be apply

    #     Args:
    #         rule1 (int): first rule to compare
    #         rule2 (int): second rule to compare

    #     Returns:
    #         char: first character where is the conflict
    #     """

    #     lhs1, _ = self.rules[rule1]
    #     lhs2, _ = self.rules[rule2]
        
    #     lhs_min_len, lhs_max_len = (lhs1, lhs2) if len(lhs1) <= len(lhs2) else (lhs2, lhs1)

    #     for a in lhs_min_len:
    #         if a in lhs_max_len:
    #             return a
    #     return None
    
    
    # def _is_applicable(self, rule):
    #     """Checks if a rule ca be applied

    #     Args:
    #         rule (int): rule to check

    #     Returns:
    #         boolean: if the can be applied to the system or not
    #     """

    #     for obj in self.alphabet:
    #         if self.objects[obj] < self.rules[rule][0].count(obj):
    #             return False
    #     for obj in self.rules[rule][1]:
    #         if obj not in self.rhs_alphabet:
    #             return False
    #     return True