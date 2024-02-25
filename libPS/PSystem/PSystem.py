import random
import re
from .membrane import *

class PSystem:

    def __init__(self, H={}, V:list=[], base_struct="11", m_objects={1:''}, m_rules={1:{}}, m_plasmids={0:[]}, p_rules={1:[]}, i0=1):
        """PSystem class constructor.

        Args:
            H (dict, optional): Plasmids' alphabet and its rules. Defaults to {}.
            V (list, optional): System's alphabet. Defaults to [].
            base_struct (str, optional): Initial system's structure. Defaults to "11".
            m_objects (dict, optional): Membranes' objects | key:int = memb_id, value:str = memb_objects. Defaults to {1:''}.
            m_rules (dict, optional): Membranes' rules | key:int = memb_id, value:dict = memb_rules. Defaults to {1:{}}.
            m_plasmids (dict, optional): Membranes' plasmids. Defaults to {0:[]}.
            p_rules (dict, optional): Rules priority in each membrane | key:int = memb_id, value:list = memb_priority. Defaults to {1:[]}.
            i0 (int, optional): Output membrane. Defaults to 1.
        """

        self.plasmids = set(H)
        self.alphabet = set(V)
        self.membranes = {}
        self.outRegion = i0

        # genera la estructura dada
        self._gen_struct(base_struct, m_objects, m_rules, p_rules)


    def _gen_struct(self, struct, m_objects, m_rules, p_rules):
        """Creates system structure.

        Args:
            struct (str): Initial structure
            m_objects (dict): Membrane's objects | key:int = memb_id, value:str = memb_objects
            m_rules (dict): Membrane's rules | key:int = memb_id, value:dict = memb_rules
            p_rules (dict): Rules priority in each membrane | key:int = memb_id, value:list = memb_priority
        """

        open = struct[0]    # variable que indica en qué membrana estamos generando (permite comprobar a la vez que se va generando que la estructura inicial sea correcta)
        id = int(open)      # identificador de la membrana abierta
        # creamos entrada para la primera membrana con sus parametros correspondientes
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects=m_objects[id], rules=m_rules[id], p_rules=p_rules[id]))
        # recorremos todas las posiciones del array de estructura 
        for m in struct[1:]:
            # print(open)
            # si nos encontramos con un numero diferente al anterior significa que se trata de una membrana hija
            if m != open[-1] and m not in open[:-1]:
                # añadimos un hijo a la membrana padre
                self.membranes[int(open[-1])].add_child(int(m))
                id = int(m) # actualizamos el identificador
                # creamos la membrana hija con sus parametros correspondientes
                memb = Membrane(V=self.alphabet, id=id, parent=int(open[-1]), objects=m_objects[id], rules=m_rules[id], p_rules=p_rules[id])
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
            verbose (boolean): if verbose = True, prints system's structure in each step. Default to False.
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
            verbose (boolean): if verbose = True, prints system's structure in each step. Default to False.
        """
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
        print(self.membranes[self.outRegion].objects)


    def evolve(self, feasible_rules, verbose=False):
        """Makes an iteration on the system choosing a random membrane to apply its rules.

        Args:
            feasible_rules (tuple): System's feasible rules | (memb_id:int, rules_set:list)
        """

        # selección de una membrana aleatoria dentro de las posibles con reglas factibles
        memb_id, f_rules = random.choice(feasible_rules)

        dissolve = False

        if verbose: print(f'[membrane {memb_id}] rules applied : {f_rules}')
        for rule_id in f_rules:
            
            # si una regla anterior ha disuelto la membrana no aplica más reglas en esa membrana
            if dissolve == True: break
            
            # divide en parte izquierda y derecha la regla
            lhs, rhs = self.membranes[memb_id].rules[rule_id]






            # por si es una regla que interactúa con plasmidos, o se ha querido usar la estructura de los corchetes, en la parte derecha de la regla
            match = re.search(r'(.*)\[(.*)\]', lhs)
            if match:
                plasmids, lhs = match.group(1), match.group(2)
                print(f"plasmids: {plasmids} | lhs: {lhs}")
            else:
                plasmids = ""
            
            # por si se ha querido usar la estructura de los corchetes en la parte izquierda de la regla
            match = re.search(r'\[(.*?)\]', rhs)
            if match:
                rhs = match.group(1)






            # máximo numero de iteraciones posibles para la regla (minimo numero de objetos en la membrana a los que afecta la regla dividido el numero de ocurrencias en la parte izquierda de la regla)
            max_possible_i = min([int(obj/lhs.count(s)) for s,obj in self.membranes[memb_id].objects.items() if s in lhs])

            # printea membrana y regla
            if verbose: print(f'memb_id: {memb_id} | n_times: {max_possible_i} -> rule: {self.membranes[memb_id].rules[rule_id]}')

            # recorremos la parte izquierda y se quitan los objetos recorridos del diccionario de objectos de la membrana
            for obj in lhs:
                self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects[obj] - max_possible_i
            
            # de la membrana elegida sacamos el id de la membrana padre 
            parent_id = self.membranes[memb_id].parent

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
                        self.membranes[parent_id].childs.remove(memb_id)
                        # como se ha disuelto la membrana, las membranas hijas de la disuelta pasan a ser hijas de la membrana padre
                        self.membranes[parent_id].childs = self.membranes[parent_id].childs | self.membranes[memb_id].childs
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


    def get_feasible_rules(self):
        """Get feasible rules from all membranes in the system.

        Returns:
            list: List of membranes and their feasible rules
        """

        feasible_rules = []
        # recorre todas las membranas y va añadiendo en feasible_rules las reglas factibles
        for id, memb in self.membranes.items():
            # obtiene las reglas factibles de una membrana
            all_f_rules = list(memb.get_feasible_rules())
            rules = random.choice(all_f_rules)
            # en el caso de que se obtengan reglas las añade en feasible_rules como una tuplas como una tupla con el identificador de la membrana y las reglas 
            if len(rules) != 0: feasible_rules.append((id, rules))

        return feasible_rules


    def print_system(self):
        """Print system's structure
        """
        print(self._struct_system())


    def _struct_system(self, struct='', id=1):
        """Recursive function that returns system's structure.

        Args:
            struct (str, optional): Acumulative structure to do it in a recursive way. Defaults to ''.
            id (int, optional): Membrane's id . Defaults to 1.

        Returns:
            str: Generate a more visual form of the system
        """
        
        objects = ''
        for obj, n in self.membranes[id].objects.items():
            objects += obj*n
        struct = f"[{id} '{objects}' "
        if self.membranes[id].childs != {}:
            for id_child in self.membranes[id].childs:
                struct += self._struct_system(struct, id_child)
        struct += f']{id}'
        return struct