import random
from .membrane import *
import re

class PSystem:


    def __init__(self, H=None, V:list=[], base_struct="11", m_objects={0:''}, m_plasmids=None, m_rules={0:{}}, p_rules={0:[]}, i0=1):
        """PSystem class constructor.

        Args:
            H (dict, optional): Plasmids' alphabet and its rules. Defaults to {}.
            V (list, optional): System's alphabet. Defaults to [].
            base_struct (str, optional): Initial system's structure. Defaults to "11".
            m_objects (dict, optional): Membranes' objects | key:int = memb_id, value:str = memb_objects. Defaults to {1:''}.
            m_rules (dict, optional): Membranes' rules | key:int = memb_id, value:dict = memb_rules. Defaults to {1:{}}.
            p_rules (dict, optional): Rules priority in each membrane | key:int = memb_id, value:list = memb_priority. Defaults to {1:[]}.
            i0 (int, optional): Output membrane. Defaults to 1.
        """
        
        self.alphabet = set(V)
        self.membranes = {}
        self.outRegion = i0
        # self.enviroment = {"plasmids":set(), "objects":{}, "rules":{}}

        # preparar por si no se trabaja con plásmidos que no de ningún tipo de error
        if H == None:
            self.plasmids = {}
            m_plasmids = {i: set() for i in range(int(max(base_struct)) + 1)}
        else:
            self.plasmids = H

        # en el caso de que no le pasemos a alguna membrana los objetos, los inicializa a sin objetos
        if len(m_objects.keys()) != int(max(base_struct)) + 1:
            for i in range(int(max(base_struct)) + 1):
                m_objects[i] = m_objects.get(i, '')
        
        # en el caso de que no le pasemos a alguna membrana las reglas, las inicializa a sin reglas
        if len(m_rules.keys()) != int(max(base_struct)) + 1:
            for i in range(int(max(base_struct)) + 1):
                m_rules[i] = m_rules.get(i, {})

        # en el caso de que no le pasemos a alguna membrana las prioridades, los inicializa a sin prioridades
        if len(p_rules.keys()) != int(max(base_struct)) + 1:
            for i in range(int(max(base_struct)) + 1):
                p_rules[i] = p_rules.get(i, [])

        # genera la estructura dada
        self._gen_struct(base_struct, m_objects, m_plasmids, m_rules, p_rules)


    def _gen_struct(self, struct, m_objects, m_plasmids, m_rules, p_rules):
        """Creates system structure.

        Args:
            struct (str): Initial structure
            m_objects (dict): Membrane's objects | key:int = memb_id, value:str = memb_objects
            m_rules (dict): Membrane's rules | key:int = memb_id, value:dict = memb_rules
            p_rules (dict): Rules priority in each membrane | key:int = memb_id, value:list = memb_priority
        """

        # preparacion del entorno
        # self.enviroment['plasmids'] = m_plasmids[0] # añadir al entorno sus plásmidos
        # self.enviroment['rules'] = m_rules[0] # añadir al entorno sus reglas

        # añadir al entorno sus objetos 
        # objects = m_objects[0]
        # for obj in self.alphabet:
        #     count = objects.count(obj)
        #     self.enviroment['objects'][obj] = self.enviroment['objects'].get(obj, 0) + count

        self.membranes[0] = self.membranes.get(0, Membrane(V=self.alphabet, id=0, parent=None, objects=m_objects[0], plasmids=m_plasmids[0], rules=m_rules[0], p_rules=p_rules[0]))

        open = struct[0]    # variable que indica en qué membrana estamos generando (permite comprobar a la vez que se va generando que la estructura inicial sea correcta)
        id = int(open)      # identificador de la membrana abierta
        # creamos entrada para la primera membrana con sus parametros correspondientes
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=0, objects=m_objects[id], plasmids=m_plasmids[id], rules=m_rules[id], p_rules=p_rules[id]))
        # recorremos todas las posiciones del array de estructura 
        for m in struct[1:]:
            # print(open)
            # si nos encontramos con un numero diferente al anterior significa que se trata de una membrana hija
            if m != open[-1] and m not in open[:-1]:
                # añadimos un hijo a la membrana padre
                self.membranes[int(open[-1])].add_child(int(m))
                id = int(m) # actualizamos el identificador
                # creamos la membrana hija con sus parametros correspondientes
                memb = Membrane(V=self.alphabet, id=id, parent=int(open[-1]), objects=m_objects[id], plasmids=m_plasmids[id], rules=m_rules[id], p_rules=p_rules[id])
                # añadimos la membrana al diccionario de mebranas
                self.membranes[id] = self.membranes.get(id, memb)
                # añadimos a la variable auxiliar la membrana hija que se ha abierto
                open += m
            
            # si ya estaba abierta y no es la ultima abierta error por cerrar una membrana que no es la última abierta
            elif m in open[:-1]:
                raise NameError('Incorrect membrane structure 1')
            # si es el mismo numero 'cerramos' la membrana
            else:
                open = open[:-1]

        # en el caso de que sea una estructura incorrecta (creo que podría haber error cuando '123231')
        if open != '':
            raise NameError('Incorrect membrane structure 2')


    def steps(self, n=1, verbose=False):
        """Evolve the system n steps or until finish

        Args:
            n (int, optional): Number of steps to evolve. Defaults to 1.
            verbose (bool, optional): if verbose = True, prints system's structure in each step. Default to False.
        """

        cont = n
        while cont > 0:
            if verbose: 
                self.print_system()
                print("\n--------------------------------------------------------------------------------------------\n")
            feasible_rules = self.get_feasible_rules()
            self.evolve(feasible_rules, verbose)
            cont -= 1
        self.print_system()
        print("\n============================================================================================\n")
        # objectos tras aplicar n pasos en el sistema
        self.print_system()


    def while_evolve(self, verbose=False):
        """Evolve the system until finish

        Args:
            verbose (bool, optional): if verbose = True, prints system's structure in each step. Default to False.
        """
        # muestra por pantalla cada estado después de aplicar una regla
        #print("\n--------------------------------------------------------------------------------------------\n")
        print()
        feasible_rules = self.get_feasible_rules()
        while(feasible_rules != []):
            if verbose: 
                self.print_system()
                print("\n--------------------------------------------------------------------------------------------\n")
            self.evolve(feasible_rules, verbose)
            feasible_rules = self.get_feasible_rules()
        self.print_system()
        print("\n============================================================================================\n")
        # objectos tras aplicar todas las iteraciones posibles en la región de salida
        print(sorted(self.membranes[self.outRegion].objects.items()))


    def _struct_rule(self, memb_id, rule_id):
        lhs, rhs =  self.membranes[memb_id].rules[rule_id] if type(rule_id) == int else self.plasmids[rule_id[:-1]][rule_id]
        
        match = re.search(r'(?m)^((?:(?!\[).)*)(.*)', lhs)
        if match:
            lhs, childs_lhs = match.group(1), match.group(2)
            membs_lhs = [(lhs, memb_id)]
            if childs_lhs != "":
                match = re.sub(r'\[([^\[\]]*)\](\d*)', "", childs_lhs)
                match2 = re.findall(r'\[([^\[\]]*)\](\d*)', childs_lhs)
                if match:
                    match = re.findall(r'\[([^\[\]]*)\](\d*)', match)
                else:
                    match = []

                aux = match + match2
                for i in range(len(aux)):
                    aux[i] = (aux[i][0], int(aux[i][1]))

                membs_lhs += aux

        match = re.search(r'(?m)^((?:(?!\[).)*)(.*)', rhs)
        if match:
            rhs, childs_rhs = match.group(1), match.group(2)
            membs_rhs = [(rhs, memb_id)]
            
            if childs_rhs != "":
                match = re.sub(r'\[([^\[\]]*)\](\d*)', "", childs_rhs)
                match2 = re.findall(r'\[([^\[\]]*)\](\d*)', childs_rhs)
                if match:
                    match = re.findall(r'\[([^\[\]]*)\](\d*)', match)
                else:
                    match = []

                aux = match + match2
                for i in range(len(aux)):
                    aux[i] = (aux[i][0], int(aux[i][1]))

                membs_rhs += aux

        return sorted(membs_lhs, key=lambda x: x[1]), sorted(membs_rhs, key=lambda x: x[1])


    def evolve(self, feasible_rules, verbose=False):
        """Makes an iteration on the system choosing a random membrane to apply its rules.

        Args:
            feasible_rules (tuple): System's feasible rules | (memb_id:int, rules_set:list)
            verbose (bool, optional): if verbose = True, prints system's structure in each step. Default to False.
        """

        # selección de una membrana aleatoria dentro de las posibles con reglas factibles
        memb_id, f_rules = random.choice(feasible_rules)

        dissolve = False

        if verbose: print(f'[membrane {memb_id}] rules applied : {f_rules}')
        for rule_id in f_rules:
            # si una regla anterior ha disuelto la membrana no aplica más reglas en esa membrana
            if dissolve == True: break

            membs_lhs, membs_rhs = self._struct_rule(memb_id, rule_id)             
            dissolve = self._apply_rule(membs_lhs, membs_rhs, verbose)
            

    def _max_possible_iter(self, membs_lhs):
            
        max_iters = []
        for lhs, memb_id in membs_lhs:
            match = re.findall(r"P\d+", lhs)
            if match != []:
                rhs = re.sub(r"P\d+", "", lhs)  # obtiene el string de objetos

            aux = [int(obj/lhs.count(s)) for s, obj in self.membranes[memb_id].objects.items() if s in lhs]
            aux = min(aux) if aux != [] else 1
            max_iters.append(aux)

        return min(max_iters)


    def _apply_rule(self, membs_lhs, membs_rhs, verbose=False):
        """Apply rule with id = rule_id in membrane with id = memb_id

        Args:
            memb_id (int): membrane's id
            rule_id (int): rule's id to be applied
            verbose (bool, optional): if verbose = True, prints system's structure in each step. Default to False.

        Returns:
            bool: returns if the rule dissolves the membrane
        """
        # máximo numero de iteraciones posibles para la regla (minimo numero de objetos en la membrana a los que afecta la regla dividido el numero de ocurrencias en la parte izquierda de la regla)
        max_possible_i = self._max_possible_iter(membs_lhs)

        # printea membrana y regla
        # if verbose: print(f'memb_id: {memb_id} | n_times: {max_possible_i} -> rule: {self.membranes[memb_id].rules[rule_id]}')

        for lhs, memb_id in membs_lhs:        

            match = re.findall(r"P\d+", lhs)
            if match != []:
                lhs = re.sub(r"P\d+", "", lhs)  # obtiene el string de objetos

            # recorremos la parte izquierda y se quitan los objetos recorridos del diccionario de objectos de la membrana
            for obj in lhs:
                self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects[obj] - max_possible_i

        for rhs, memb_id in membs_rhs:
            # de la membrana elegida sacamos el id de la membrana padre 
            parent_id = self.membranes[memb_id].parent
            dissolve = False

            match = re.findall(r"P\d+", rhs)
            if match != []:
                rhs = re.sub(r"P\d+", "", rhs)  # obtiene el string de objetos
                plasmids_rhs = match
            else:
                plasmids_rhs = []

            if plasmids_rhs != []:

                if parent_id != None:
                    self.membranes[parent_id].plasmids.difference_update(plasmids_rhs)
                else:
                    self.enviroment['plasmids'].difference_update(plasmids_rhs)

                for child in self.membranes[memb_id].childs:
                    self.membranes[child].plasmids.difference_update(plasmids_rhs)

                # añadir a la membrana los plásmidos
                if memb_id != 0:
                    self.membranes[memb_id].plasmids.update(plasmids_rhs)
                else:
                    self.enviroment['plasmids'].update(plasmids_rhs)


            # recorremos la parte derecha de la regla           
            for i, _ in enumerate(rhs):
                # si no es un digito
                if not(rhs[i].isdigit()):
                    # en el caso de que sea un punto disolvemos membrana
                    if rhs[i] == '.':   # disolver
                        # si existe membrana padre  
                        if parent_id != None:
                            # añade los objetos de la membrana a disolver en la membrana padre
                            for obj in self.alphabet:
                                value = self.membranes[memb_id].objects[obj]
                                self.membranes[parent_id].objects[obj] = self.membranes[parent_id].objects.get(obj, 0) + value
                        
                        # eliminamos el hijo disuelto de la membrana padre
                        self.membranes[parent_id].remove_child(memb_id)
                        # como se ha disuelto la membrana, las membranas hijas de la disuelta pasan a ser hijas de la membrana padre
                        for child in self.membranes[memb_id].childs:
                            self.membranes[parent_id].add_child(child) 
                        # eliminamos la entrada a la membrana disuelta
                        self.membranes.pop(memb_id)

                        dissolve = True

                    # en el caso de que no sea el último objeto de la regla y el siguiente sea un dígito
                    elif i+1 != len(rhs) and rhs[i+1].isdigit():  # in to child | out to parent    
                        id = int(rhs[i+1])  # membrana hija a la que se introducirán los objetos o bien 0 si out
                        # si se encuentra el id entre los id de las membranas hijas
                        if id in self.membranes[memb_id].childs:
                            # añade objeto a la membrana hija
                            self.membranes[id].objects[rhs[i]] = self.membranes[id].objects[rhs[i]] + max_possible_i
                        # si es 0 -> out
                        elif id == 0:
                            # si tiene padre la membrana | si no tiene padre no se añade en ningún sitio
                            if parent_id != None:
                                # saca a la membrana padre el objeto
                                self.membranes[parent_id].objects[rhs[i]] = self.membranes[parent_id].objects[rhs[i]] + max_possible_i

                    # caso de adicion a la propia membrana
                    else:
                        # añade objeto a la membrana
                        self.membranes[memb_id].objects[rhs[i]] = self.membranes[memb_id].objects[rhs[i]] + max_possible_i

        return dissolve
        

    def get_feasible_rules(self):
        """Get feasible rules from all membranes in the system.

        Returns:
            list: List of membranes and their feasible rules
        """

        feasible_rules = []
        # recorre todas las membranas y va añadiendo en feasible_rules las reglas factibles
        for id, memb in self.membranes.items():
            # obtiene las reglas factibles de una membrana
            all_f_rules = list(self.get_memb_feasible_rules(id))
            rules = random.choice(all_f_rules)

            # en el caso de que se obtengan reglas las añade en feasible_rules como una tuplas como una tupla con el identificador de la membrana y las reglas 
            if len(rules) != 0: feasible_rules.append((id, rules))

        return feasible_rules
    
    
    def get_memb_feasible_rules(self, memb_id):

        if memb_id == 0:
            rules = self.membranes[memb_id].rules
        else:
            rules = self.membranes[memb_id].rules
            for pr in self.membranes[memb_id].plasmids:
                rules = rules | self.plasmids[pr]
        
        applicable_rules = [r for r in rules if self._is_applicable(memb_id, r)]   # recoge todas las reglas que se pueden aplicar
        promising = []
        for r in applicable_rules:
            # comprueba las prioridades de las reglas
            cond = True
            for r1, r2 in self.membranes[memb_id].p_rules:
                if r2 == r and self._is_applicable(memb_id, r1):
                    cond = False
            if cond: promising.append(r)

        # comprueba que no haya conflicto entre reglas
            # es decir que si una regla es a -> x y otra es a -> b, que solo se aplique una
        feasible = self._solve_conflicts(memb_id, promising)

        return feasible


    def _solve_conflicts(self, memb_id, promising):
        """Solve the conflicts with the rules in a rules' list

        Args:

            promising (list): combination of a possible rules

        Yields:
            list: feasible combination of rules
        """

        feasible = promising
        conflictive = collections.defaultdict(set)

        for r1 in promising:
            for r2 in promising:
                key, memb_id_2 = self._conflict(memb_id, r1, r2)
                if r1 != r2 and key != None:
                    conflictive[(key, memb_id_2)].add(r1)
                    conflictive[(key, memb_id_2)].add(r2)
                    if r1 in feasible: feasible.remove(r1)
                    if r2 in feasible: feasible.remove(r2)
                    break   

        def is_promising(sol, rule):
            for r in sol:
                if self._conflict(memb_id, r, rule): return False
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


    def _conflict(self, memb_id, rule1, rule2):
        """Checks if two rules have conflicts like 'a'-> 'b' and 'ab' -> 'b', both need an 'a' to be apply

        Args:
            rule1 (int): first rule to compare
            rule2 (int): second rule to compare

        Returns:
            char: first character where is the conflict
        """

        # lhs1, _ = self.membranes[memb_id].rules[rule1]
        membs_lhs1, _ = self._struct_rule(memb_id, rule1)
        # lhs2, _ = self.membranes[memb_id].rules[rule2]
        membs_lhs2, _ = self._struct_rule(memb_id, rule2)

        for lhs1, memb_id_1 in membs_lhs1:
            for lhs2, memb_id_2 in membs_lhs2:
                if memb_id_1 == memb_id_2:
                    lhs_min_len, lhs_max_len = (lhs1, lhs2) if len(lhs1) <= len(lhs2) else (lhs2, lhs1)

                    for a in lhs_min_len:
                        if a in lhs_max_len:
                            return a, memb_id_1
        
        return None, None


    def _is_applicable(self, memb_id, rule_id):
        """Checks if a rule ca be applied

        Args:
            rule (int): rule to check

        Returns:
            boolean: if the can be applied to the system or not
        """

        membs_lhs, membs_rhs = self._struct_rule(memb_id, rule_id)
        
        for lhs, memb_id in membs_lhs:
            match = re.findall(r"P\d+", lhs)
            if match != []:
                lhs = re.sub(r"P\d+", "", lhs)  # obtiene el string de objetos
                plasmids_lhs = match
            else:
                plasmids_lhs = []

            # para cada plasmido en la regla comprueba si se encuentra en los plásmidos que pueden entrar a la membrana
            for p in plasmids_lhs:
                
                if p not in self.membranes[memb_id].plasmids:
                    return False
            
            # para cada objeto de la parte izquierda comprueba que tiene suficientes como para sustituirlos
            for obj in self.alphabet:
                if self.membranes[memb_id].objects[obj] < lhs.count(obj):
                    return False
                
        for rhs, memb_id in membs_rhs:

            match = re.search(r'(.*)\[(.*)\]', rhs)
            if match:
                plasmids_out_rhs, rhs = match.group(1), match.group(2)
                if plasmids_out_rhs == "" : plasmids_out_rhs = []
            else: 
                plasmids_out_rhs = []

            # comprueba si la parte derecha de la regla tiene una estructura con plasmidos ej. "[P1P2a2b0c]" | "P1P2a2b0c"
            match = re.findall(r"P\d+", rhs)
            if match != []:
                rhs = re.sub(r"P\d+", "", rhs)  # obtiene el string de objetos
                if rhs != '' and rhs[0] == "["  and rhs[-1] == "]":
                    rhs = rhs[1:-1]     # si estaba entre corchetes los quita
                plasmids_in_rhs = match
            else: 
                plasmids_in_rhs = []

            for p in plasmids_in_rhs:
                if p not in self.accessible_plasmids(memb_id) and p not in self.membranes[memb_id].plasmids:
                    return False
            for p in plasmids_out_rhs:
                if p not in self.accessible_plasmids(memb_id) and p not in self.membranes[memb_id].plasmids:
                    return False

            # para los objetos de la parte derecha comprueba que sean del alfabeto
            for obj in rhs:
                if obj not in self.membranes[memb_id].rhs_alphabet:
                    return False

        return True

    def accessible_plasmids(self, memb_id):
        if memb_id != 0:
            parent_id = self.membranes[memb_id].parent
            if parent_id != None:
                accessible_plasmids = self.membranes[parent_id].plasmids
                
            for child in self.membranes[memb_id].childs:
                accessible_plasmids.update(self.membranes[child].plasmids)

            return accessible_plasmids
        else:
            for child in self.membranes[1].childs:
                accessible_plasmids.update(self.membranes[1].plasmids)

    def print_system(self):
        """Print system's structure
        """
        print(self._struct_system())


    def _struct_system(self, struct='', id=0):
        """Recursive function that returns system's structure.

        Args:
            struct (str, optional): Acumulative structure to do it in a recursive way. Defaults to ''.
            id (int, optional): Membrane's id . Defaults to 1.

        Returns:
            str: Generate a more visual form of the system
        """

        if self.plasmids != {}:
            if id == 0:
                env_objects = ''
                env_plasmids = ''
                for obj, n in sorted(self.membranes[id].objects.items()):
                    env_objects += obj*n
                for p in sorted(self.membranes[id].plasmids):
                    env_plasmids += p

                struct = f" '{env_plasmids}' '{env_objects}' "

                struct += self._struct_system(struct, id=1)
            else:
                objects = ''
                plasmids = ''
                for obj, n in sorted(self.membranes[id].objects.items()):
                    objects += obj*n
                for p in sorted(self.membranes[id].plasmids):
                    plasmids += p
                struct = f" [{id} '{plasmids}' '{objects}' "
                if self.membranes[id].childs != {}:
                    for id_child in self.membranes[id].childs:
                        struct += self._struct_system(struct, id_child)
                struct += f']{id}'
        else:
            if id != 0:
                objects = ''
                for obj, n in self.membranes[id].objects.items():
                    objects += obj*n
                struct = f"[{id} '{objects}' "
                if self.membranes[id].childs != {}:
                    for id_child in self.membranes[id].childs:
                        struct += self._struct_system(struct, id_child)
                struct += f']{id}'
            else:
                struct = self._struct_system(struct, 1)
        return struct