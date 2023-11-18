from mal_membrane import *

class PSystem:

    def __init__(self, V:list=[], base_struct="11", m_objects=[], m_rules=[], p_rules=[], i0=1):
        '''
        PSystem class constructor.

        :param V: System's alphabet
        :type V: list

        :param base_struct: Initial system's structure 
        :type base_struct: str

        :param m_objects: Membrane's objects. Structure [{obj m1}'aab',{obj m2}'bba',...]
        :type m_objects: str list

        :param m_rules: Membrane's rules. Structure [[{rules m1}(lhs,rhs),(lhs,rhs)],[{rules m2}(lhs,rhs),(lhs,rhs)],...]
        :type m_rules:  tuple list list

        :param i0: output membrane
        :type i0: int 
        '''
        
        self.alphabet = set(V)
        self.membranes = {}
        self.plasmids = {}
        self.outRegion = i0

#        self.gen_struct(base_struct, m_objects, m_rules, p_rules)
        self.gen_struct(base_struct, m_objects, m_rules)

        feasible_rules = self.get_feasible_rules(p_rules)
        # while(feasible_rules != []):
        #     self.evolve(feasible_rules)
        #     print("--------------------------------------------------------------------------------------------")
        #     print(self.struct_system())
        #     feasible_rules = self.get_feasible_rules()
        print(feasible_rules)
        print("================================================================================================")
        print(self.membranes[i0].objects)


    # def gen_struct(self, struct, m_objects, m_rules, p_rules):
    def gen_struct(self, struct, m_objects, m_rules):
        open = struct[0]
        id = 1
        # self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects=m_objects[id-1], rules=m_rules[id-1], p_rules=p_rules[id-1]))
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects=m_objects[id-1], rules=m_rules[id-1]))
        for m in struct[1:]:
            if m != open[-1]:
                self.membranes[int(open[-1])].add_child(id + 1)
                id = id + 1
                print(id)
                print(p_rules[id-1])
                # memb = Membrane(V=self.alphabet, id=id, parent=int(open[-1]), objects=m_objects[id-1], rules=m_rules[id-1], p_rules=p_rules[id-1])
                memb = Membrane(V=self.alphabet, id=id, parent=int(open[-1]), objects=m_objects[id-1], rules=m_rules[id-1])
                self.membranes[id] = self.membranes.get(id, memb)
                open = open + m
            else:
                open = open[:-1]

        if open != '':
            self.membranes = {}
            raise NameError('Incorrect membrane structure')

    def get_feasible_rules(self):
        feasible_rules = []
        for cont, (id, memb) in enumerate(self.membranes.items()):
            aux = memb.feasible_rules()
            if len(aux) != 0: feasible_rules.append((id, aux))
        return feasible_rules

    def evolve(self, feasible_rules):
        memb_id, f_rules = random.choice(feasible_rules)
        rule_id = random.choice(list(f_rules))
        
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
                            print('id == 0')
                            print(self.membranes[parent_id])
                            self.membranes[parent_id].objects[rhs[i]] = self.membranes[parent_id].objects[rhs[i]] + 1
                else:
                    self.membranes[memb_id].objects[rhs[i]] = self.membranes[memb_id].objects[rhs[i]] + 1

    def struct_system(self, struct='', id=1):
        struct = f'[{id}{self.membranes[id].objects}'
        if self.membranes[id].childs != {}:
            for id_child in self.membranes[id].childs:
                struct += self.struct_system(struct, id_child)
        struct += f']{id}'
        return struct


# from PSystem import *
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aaaaac','ab'], m_rules=[[('aa','b'),('c','a')],[('c','ca')]])
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['a',''], m_rules=[[('a','b2')],[]])
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['','a'], m_rules=[[('a','b2')],[('a','c0')]])
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['','b'], m_rules=[[],[('b','a'), ('a','c.')]])
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aa',''], m_rules=[[('a','ab2c2c2'),('aa','a0a0')],[]], i0=2)

# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aa',''], m_rules=[[('a','ab2c2c2'),('aa','a0a0')],[]])


alphabet = ['a','b','c','d','x','n','s']
struct = '122331'
m_objects = ['aaccccd','']
m_rules = [[('dcx','n3'),('d','s3')], [('ac','x'),('ax','c'),('d','d')], []]
p_rules = [[(1,2)],[(1,3),(2,3)],[]]
i0 = 3

ps = PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)