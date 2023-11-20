import random
from membrane import *

class PSystem:

    def __init__(self, V:list=[], base_struct="11", m_objects={}, m_rules={}, p_rules={}, i0=1):
        '''
        PSystem class constructor.

        :param V: System's alphabet
        :type V: list

        :param base_struct: Initial system's structure 
        :type base_struct: str

        :param m_objects: Membrane's objects
        :type m_objects: dict -> key:int = memb_id, value:str = memb_objects

        :param m_rules: Membrane's rules
        :type m_rules:  dict -> key:int = memb_id, value:dict = memb_rules

        :param p_rules: rules priority in each membrane
        :type p_rules:  dict -> key:int = memb_id, value:list = memb_priority

        :param i0: output membrane
        :type i0: int
        '''

        self.alphabet = set(V)
        self.membranes = {}
        self.plasmids = {}
        self.outRegion = i0

        # genera la estructura dada
        self.gen_struct(base_struct, m_objects, m_rules, p_rules)

        # muestra por pantalla cada estado después de aplicar una regla
        print(self.struct_system())
        print("--------------------------------------------------------------------------------------------")
        feasible_rules = self.get_feasible_rules()
        while(feasible_rules != []):
            self.evolve(feasible_rules)
            print(self.struct_system())
            feasible_rules = self.get_feasible_rules()
            print("--------------------------------------------------------------------------------------------")
        print("============================================================================================")
        # objectos tras aplicar todas las iteraciones posibles en la región de salida
        print(self.membranes[i0].objects)


    def gen_struct(self, struct, m_objects, m_rules, p_rules):
        '''
        Creates system structure.

        :param struct: initial structure
        :type struct: str

        :param m_objects: Membrane's objects.
        :type m_objects: dict -> key:int = memb_id, value:str = memb_objects         

        :param m_rules: Membrane's rules.
        :type m_rules:  dict -> key:int = memb_id, value:dict = memb_rules

        :param p_rules: rules priority in each membrane.
        :type p_rules:  dict -> key:int = memb_id, value:list = memb_priority

        '''
        open = struct[0]    # variable que indica en qué membrana estamos generando (permite comprobar a la vez que se va generando que la estructura inicial sea correcta)
        id = int(open)      # identificador de la membrana abierta
        # creamos entrada para la primera membrana con sus parametros correspondientes
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects=m_objects[id], rules=m_rules[id], p_rules=p_rules[id]))
        # recorremos todas las posiciones del array de estructura 
        for m in struct[1:]:
            # si nos encontramos con un numero diferente al anterior significa que se trata de una membrana hija
            if m != open[-1]:
                # añadimos un hijo a la membrana padre
                self.membranes[id].add_child(int(m))
                id = int(m) # actualizamos el identificador
                # creamos la membrana hija con sus parametros correspondientes
                memb = Membrane(V=self.alphabet, id=id, parent=int(open[-1]), objects=m_objects[id], rules=m_rules[id], p_rules=p_rules[id])
                # añadimos la membrana al diccionario de mebranas
                self.membranes[id] = self.membranes.get(id, memb)
                # añadimos a la variable auxiliar la membrana hija que se ha abierto
                open += m
            # si es el mismo numero 'cerramos' la membrana
            else:  
                open = open[:-1]

        # en el caso de que sea una estructura incorrecta (creo que podría haber error cuando '123231')
        if open != '':
            self.membranes = {}
            print('Incorrect membrane structure')


    def get_feasible_rules(self):
        '''
        Get feasible rules from all membranes in the system.

        :return feasible_rules 

        '''
        feasible_rules = []
        # recorre todas las membranas y va añadiendo en feasible_rules las reglas factibles
        for id, memb in self.membranes.items():
            # obtiene las reglas factibles de una membrana
            aux = memb.feasible_rules()
            # en el caso de que se obtengan reglas las añade en feasible_rules como una tuplas como una tupla con el identificador de la membrana y las reglas 
            if len(aux) != 0: feasible_rules.append((id, aux))
        return feasible_rules

    def evolve(self, feasible_rules):
        '''
        Makes an iteration on the system choosing a random rule from given rules (feasible_rules).

        :param feasible_rules: system's feasible rules
        :type feasible_rules: tuple (memb_id, rules_set) -> memb_id:int | rules_set:list

        '''
        # selección de una membrana aleatoria dentro de las posibles con reglas factibles
        memb_id, f_rules = random.choice(feasible_rules)
        # selección de una regla aleatoria del conjunto obtenido de la membrana aleatoria
        rule_id = random.choice(list(f_rules))

        # pritea membrana y regla
        print(f'memb_id: {memb_id} | rule: {self.membranes[memb_id].rules[rule_id]}')

        # divide en parte izquierda y derecha la regla
        lhs, rhs = self.membranes[memb_id].rules[rule_id]

        # recorremos la parte izquierda y se quitan los objetos recorridos del diccionario de objectos de la membrana
        for obj in lhs:
            self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects[obj] - 1
        
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
                    # eliminamos la entrada a la membrana disuelta
                    self.membranes.pop(memb_id)
                # en el caso de que no sea el último objeto de la regla y el siguiente sea un dígito
                elif i+1 != len(rhs) and rhs[i+1].isdigit():  # in to child | out to parent    
                    id = int(rhs[i+1])  # membrana hija a la que se introducirán los objetos o bien 0 si out
                    # si se encuentra el id entre los id de las membranas hijas
                    if id in self.membranes[memb_id].childs:
                        # añade objeto a la membrana hija
                        self.membranes[id].objects[rhs[i]] = self.membranes[id].objects[rhs[i]] + 1
                    # si es 0 -> out
                    elif id == 0:
                        # si tiene padre la membrana | si no tiene padre no se añade en ningún sitio
                        if parent_id != None:
                            # saca a la membrana padre el objeto
                            self.membranes[parent_id].objects[rhs[i]] = self.membranes[parent_id].objects[rhs[i]] + 1
                # caso de adicion a la propia membrana
                else:
                    # añade objeto a la membrana
                    self.membranes[memb_id].objects[rhs[i]] = self.membranes[memb_id].objects[rhs[i]] + 1

    def struct_system(self, struct='', id=1):
        '''
        Recursive function to print system's structure.

        :param struct: acumulative structure to do it in a recursive way 
        :type struct: str

        :param id: membrane's id 
        :type id: int

        '''
        objects = ''
        for obj, n in self.membranes[id].objects.items():
            objects += obj*n 
        struct = f"[{id} '{objects}' "
        if self.membranes[id].childs != {}:
            for id_child in self.membranes[id].childs:
                struct += self.struct_system(struct, id_child)
        struct += f']{id}'
        return struct

# ~ n es divisible entre k
n = 14
k = 7

alphabet = ['a','c','x','d']
struct = '122331'
m_objects = {1:'',
             2:'a'*n+'c'*k+'d',
             3:'a'}
r_1 = {1:('dcx','a3')}
r_2 = {1:('ac','x'),
       2:('ax','c'),
       3:('d','d.')}
m_rules = {1:r_1,
           2:r_2,
           3:{}}
p_rules = {1 : [],
           2 : [(1,3),(2,3)],
           3 : []}
i0 = 3

# # ~ n^2

# alphabet = ['a','b','x','c','f']
# struct = '12334421'
# m_objects = {1:'',
#              2:'',
#              3:'af',
#              4:''}

# r_2 = {1:('x','b'),
#        2:('b','bc4'),
#        3:('ff','af'),
#        4:('f','a.')}

# r_3 = {1:('a','ab'),
#        2:('a','x.'),
#        3:('f','ff')}

# m_rules = {1:{},
#            2:r_2,
#            3:r_3,
#            4:{}}

# p_rules = {1:[],
#            2:[(3,4)],
#            3:[],
#            4:[]}
# i0 = 4


ps = PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)