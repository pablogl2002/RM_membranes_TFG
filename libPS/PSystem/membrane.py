import collections
import re

class Membrane:

    def __init__(self, H, V, id:int, parent:int=None, objects:str='', rules={}, plasmids=[], accessible_plasmids=[], p_rules={}):
        """Membrane class constructor.

        Args:
            H (dict): Plasmids' alphabet and its rules. Defaults to {}.         
            V (list): Membrane's alphabet (same as system's)
            id (int): Membrane's id
            parent (int, optional): Parent Membrane's id. Defaults to None.
            objects (str, optional): Membrane's objects. Defaults to ''.
            rules (dict, optional): Membrane's rules | key: rule_id, value:list = tuple (lhs, rhs). Defaults to {}.
            plasmids (list, optional): Plasmids in the membrane. Defaults to [].
            accessible_plasmids (list, optional): Plasmids that can access the membrane (in parents membrane, or environment if membrane 1). Defaults to [].
            p_rules (dict, optional): Rules priority in membrane. Defaults to {}.
        """

        self.plasmids = H                               # plasmids' alphabet and its rules
        self.alphabet = V                               # membrane's alphabet
        self.id = id                                    # membrane's id
        self.parent = parent                            # parent's id
        self.childs = set()                             # childs' ids set list
        self.rules = rules                              # rules' dict
        self.p_rules = p_rules                          # rules' priority dict
        self.plasmids_in = set(plasmids)                # plasmids' set list
        self.accessible_plasmids = accessible_plasmids  # plasmids that can access the membrane   
        self.objects = {}                               # membrane object's dict
        self.rhs_alphabet = V.copy()                    # rhs rules' alphabet

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
    

    def add_plasmids(self, plasmids:list):
        """Add plasmid to the membrane.

        Args:
            plasmids (list): list of plasmids' id 
        """

        # for plasmid in plasmids:
        #     self.rules.add(plasmid)
        pass
    

    def add_objects(self, objects:str):
        """Add objects to the membranes.

        Args:
            objects (str): objects to add in the membrane
        """

        suma = 0    # contador para saber si hemos sumado correctamente
        prev_objs = self.objects
        # para cada objecto del alfabeto contamos las veces que aparece en el string y lo sumamos al alfabeto
        for obj in self.alphabet:
            count = objects.count(obj)
            self.objects[obj] = self.objects.get(obj, 0) + count
            suma += count
        # si la suma no es igual a la longitud de los objetos significa que hay algún objeto que no se encuentra en el alfabeto que no hemos sumado 
        if suma != len(objects):
            self.objects = prev_objs
            raise NameError(f'Some objects given not in alphabet({self.alphabet})')


    def get_feasible_rules(self):
        """Return a combination of rules that can be applied all at once in the membrane

        Returns:
            list: list of list (due to yields) with feasible rules combinations
        """

        applicable_rules = [r for r in self.rules if self._is_applicable(r)]   # recoge todas las reglas que se pueden aplicar
        promising = []
        for r in applicable_rules:
            # comprueba las prioridades de las reglas
            cond = True
            # para cada relacion de prioridad en las reglas
            for r1, r2 in self.p_rules:
                # si la regla que estamos comprobando se encuentra en la parte derecha de la relación entonces comprueba si la regla de la parte izquierda es aplicable
                if r2 == r and self._is_applicable(r1):
                    # si r1 es aplicable entonces no se añade r2 al conjunto de reglas prometedoras
                    cond = False
            if cond: promising.append(r)    # añadimos la regla al conjunto de reglas prometedoras

        # comprueba que no haya conflicto entre reglas
            # es decir que si una regla es a -> x y otra es a -> b, que solo se aplique una
        feasible = self._solve_conflicts(promising)

        return feasible


    def _solve_conflicts(self, promising):
        """Solve the conflicts with the rules in a rules' list

        Args:
            promising (list): combination of a possible rules

        Yields:
            list: feasible combination of rules
        """

        feasible = promising
        conflictive = collections.defaultdict(set)

        # preprocesamiento para ver las reglas que son conflictivas entre sí
        for r1 in promising:
            for r2 in promising:
                if r1 != r2:
                    # comprobamos si es conflictiva
                    key = self._conflict(r1, r2)
                    if key != None: 
                        # si es conflictiva las añadimos la diccionario de conflictivas
                        conflictive[key].add(r1)
                        conflictive[key].add(r2)
                        # si se encontraban en las reglas factibles las borramos
                        if r1 in feasible: feasible.remove(r1)
                        if r2 in feasible: feasible.remove(r2)
                        break   # rompemos el segundo bucle

        def is_promising(sol, rule):
            # para cada regla que hay hasta ahora en la solución comprobamos si la regla entrante tiene conflicto con ellas
            for r in sol:
                if self._conflict(r, rule): return False
            return True

        def backtracking(sol):
            # if es completo
            if len(sol) == len(conflictive.keys()):
                yield feasible + sol
            else:
                # ramificar
                for _, rules in conflictive.items():
                    for rule in rules:
                        # if prometedor
                        if is_promising(sol, rule):
                            yield from backtracking(sol+[rule])

        yield from backtracking([])


    def _conflict(self, rule1, rule2):
        """Checks if two rules have conflicts like 'a'-> 'b' and 'ab' -> 'b', both need an 'a' to be apply

        Args:
            rule1 (int): first rule to compare
            rule2 (int): second rule to compare

        Returns:
            char: first character where is the conflict
        """

        lhs1, _ = self.rules[rule1]     # cogemos parte izquierda de la primera regla
        lhs2, _ = self.rules[rule2]     # cogemos parte izquierda de la segunda regla

        # comprueba si la primera regla tiene una estructura con plasmidos ej. "P1P2[abc]"
        match1 = re.search(r'(.*)\[(.*)\]', lhs1)
        if match1:
            plasmids1, lhs1 = match1.group(1), match1.group(2)  # si tiene plasmidos dividimos entre plasmidos y objetos
            plasmids1 = re.findall(r"P\d+", plasmids1)  # ponemos los plasmidos como una lista con los diferentes plásmidos
        else:
            plasmids1 = ""  # si no hay estructura de plasmidos lo inicializamos a cadena vacia para evitar errores

        # comprueba si la primera regla tiene una estructura con plasmidos ej. "P1P2[abc]"
        match2 = re.search(r'(.*)\[(.*)\]', lhs2)
        if match2:
            plasmids2, lhs2 = match2.group(1), match2.group(2)  # si tiene plasmidos dividimos entre plasmidos y objetos
            plasmids2 = re.findall(r"P\d+", plasmids2)  # ponemos los plasmidos como una lista con los diferentes plásmidos
        else:
            plasmids2 = ""  # si no hay estructura de plasmidos lo inicializamos a cadena vacia para evitar errores
        
        # comprueba si existe conflictos entre las reglas con los plásmidos
        plasmids_min_len, plasmids_max_len = (plasmids1, plasmids2) if len(plasmids1) <= len(plasmids2) else (plasmids2, plasmids1)
        for p in plasmids_min_len:
            if p in plasmids_max_len:
                return p

        # comprueba si existe conflictos entre las reglas con los objetos        
        lhs_min_len, lhs_max_len = (lhs1, lhs2) if len(lhs1) <= len(lhs2) else (lhs2, lhs1)
        for a in lhs_min_len:
            if a in lhs_max_len:
                return a
        return None # si no hay conflicto devuelve None


    def _is_applicable(self, rule_id):
        """Checks if a rule ca be applied

        Args:
            rule (int): rule to check

        Returns:
            boolean: if the can be applied to the system or not
        """
        
        lhs, rhs = self.rules[rule_id]  # divide la regla en parte izquierda y derecha

        # comprueba si la parte derecha de la regla tiene una estructura con plasmidos ej. "P1P2[abc]"
        match = re.search(r'(.*)\[(.*)\]', lhs)
        if match:
            plasmids_lhs, lhs = match.group(1), match.group(2)  # si tiene la estructura dividimos en plasmidos y objetos
        else:
            plasmids_lhs = ""
        
        # comprueba si la parte izquierda de la regla tiene una estructura con plasmidos ej. "[P1P2abc]" | "P1P2abc"
        match = re.findall(r"P\d+", rhs)
        if match:
            rhs = re.sub(r"P\d+", "", rhs)  # obtiene el string de objetos
            if rhs[0] == "["  and rhs[-1] == "]":
                rhs = rhs[1:-1]     # si estaba entre corchetes los quita
            plasmids_rhs = match

        # para cada plasmido en la regla comprueba si se encuentra en los plásmidos que pueden entrar a la membrana
        for p in plasmids_lhs:
            if p not in self.accessible_plasmids:
                return False
        for p in plasmids_rhs:
            if p not in self.accessible_plasmids:
                return False

        # para cada objeto de la parte izquierda comprueba que tiene suficientes como para sustituirlos
        for obj in self.alphabet:
            if self.objects[obj] < self.rules[rule_id][0].count(obj):
                return False
        # para los objetos de la parte derecha comprueba que sean del alfabeto
        for obj in self.rules[rule_id][1]:
            if obj not in self.rhs_alphabet:
                return False
        return True