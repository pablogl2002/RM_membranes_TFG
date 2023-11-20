from membrane import *

class PSystem:

    def __init__(self, V:list=[], base_struct="11", m_objects={}, m_rules={}, p_rules={}, i0=1):
        '''
        PSystem class constructor.

        # :param V: System's alphabet
        # :type V: list

        # :param base_struct: Initial system's structure 
        # :type base_struct: str

        # :param m_objects: Membrane's objects. Structure [{obj m1}'aab',{obj m2}'bba',...]
        # :type m_objects: str list

        # :param m_rules: Membrane's rules. Structure [[{rules m1}(lhs,rhs),(lhs,rhs)],[{rules m2}(lhs,rhs),(lhs,rhs)],...]
        # :type m_rules:  tuple list list

        # :param i0: output membrane
        # :type i0: int 
        # '''

        self.alphabet = set(V)
        self.membranes = {}
        self.plasmids = {}
        self.outRegion = i0

        self.gen_struct(base_struct, m_objects, m_rules, p_rules)

        print(self.struct_system())

        print("--------------------------------------------------------------------------------------------")

        feasible_rules = self.get_feasible_rules()
        while(feasible_rules != []):
            self.evolve(feasible_rules)
            print(self.struct_system())
            feasible_rules = self.get_feasible_rules()
            print("--------------------------------------------------------------------------------------------")


        print("============================================================================================")
        print(self.membranes[i0].objects)


    def gen_struct(self, struct, m_objects, m_rules, p_rules):
        open = struct[0]
        id = int(open)
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects=m_objects[id], rules=m_rules[id], p_rules=p_rules[id]))

        for m in struct[1:]:
            if m != open[-1]:
                self.membranes[int(open[-1])].add_child(id + 1)
                id = int(m)
                memb = Membrane(V=self.alphabet, id=id, parent=int(open[-1]), objects=m_objects[id], rules=m_rules[id], p_rules=p_rules[id])
                self.membranes[id] = self.membranes.get(id, memb)
                open = open + m
            else:
                open = open[:-1]

        if open != '':
            self.membranes = {}
            print('Incorrect membrane structure')

    def get_feasible_rules(self):
        feasible_rules = []
        for id, memb in self.membranes.items():
            aux = memb.feasible_rules()
            if len(aux) != 0: feasible_rules.append((id, aux))
        return feasible_rules

    def evolve(self, feasible_rules):
        memb_id, f_rules = random.choice(feasible_rules)
        rule_id = random.choice(list(f_rules))

        print(f'memb_id: {memb_id} | rule_id: {rule_id}')
        print(f'rule: {self.membranes[memb_id].rules[rule_id]}')

        lhs, rhs = self.membranes[memb_id].rules[rule_id]

        for obj in lhs:
            self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects[obj] - 1
        
        parent_id = self.membranes[memb_id].parent
   
        for i, _ in enumerate(rhs):
            if not(rhs[i].isdigit()):
                if rhs[i] == '.':   # disolver
                    if parent_id != None:
                        for obj in self.alphabet:
                            value = self.membranes[memb_id].objects[obj]
                            self.membranes[parent_id].objects[obj] = self.membranes[parent_id].objects.get(obj, 0) + value
                    self.membranes[parent_id].childs.remove(memb_id)
                    self.membranes.pop(memb_id)
                elif i+1 != len(rhs) and rhs[i+1].isdigit():  # in to child | out to parent    
                    id = int(rhs[i+1])
                    if id in self.membranes[memb_id].childs:
                        self.membranes[id].objects[rhs[i]] = self.membranes[id].objects[rhs[i]] + 1
                    elif id == 0:
                        if parent_id != None:
                            self.membranes[parent_id].objects[rhs[i]] = self.membranes[parent_id].objects[rhs[i]] + 1
                else:
                    self.membranes[memb_id].objects[rhs[i]] = self.membranes[memb_id].objects[rhs[i]] + 1

    def struct_system(self, struct='', id=1):
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
# n = 14
# k = 7

# alphabet = ['a','b','c','d','x','n','s']
# struct = '122331'
# m_objects = {1:'',
#              2:'a'*n+'c'*k+'d',
#              3:''}
# r_1 = {1:('dcx','n3'),
#        2:('d','s3')}
# r_2 = {1:('ac','x'),
#        2:('ax','c'),
#        3:('d','d.')}
# m_rules = {1:r_1,
#            2:r_2,
#            3:{}}
# p_rules = {1 : [(1,2)],
#            2 : [(1,3),(2,3)],
#            3 : []}
# i0 = 3

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