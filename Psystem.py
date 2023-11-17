from membrane import *

class PSystem:

    def __init__(self, V:list=[], base_struct="11", m_objects=[], m_rules=[], i0=1):
        self.alphabet = set(V)
        self.membranes = {}
        self.plasmids = {}
        self.outRegion = i0

        self.gen_struct(base_struct, m_objects, m_rules)
        # for memb in self.membranes.keys():
        #     print(self.membranes[memb].feasible_rules())
        
        print(self.membranes[2].feasible_rules())

        # while(self.membranes[i0].empty):
        #     self.evolve_iteration()
        #     print("--------------------------------------------------------------------------------------------")
        #     print(self.membranes)
        #     for id, memb in self.membranes.items():
        #        print(f'membrana : {id} con objetos: {memb.objects}')
            

    def gen_struct(self, struct, m_objects, m_rules):
        open = struct[0]
        id = int(open)
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects=m_objects[id-1], rules=m_rules[id-1]))

        for m in struct[1:]:
            if m != open[-1]:
                self.membranes[int(open[-1])].add_child(id + 1)
                id = id + 1
                memb = Membrane(V=self.alphabet, id=id, parent=open[-1], objects=m_objects[id-1], rules=m_rules[id-1])
                self.membranes[id] = self.membranes.get(id, memb)
                open = open + m
            else:
                open = open[:-1]

        if open != '':
            self.membranes = {}
            print('Incorrect membrane structure')

    def evolve_iteration(self):
        feasible_rules = []
        for id, memb in self.membranes.items():
            aux = memb.feasible_rules()
            if aux.len != 0: feasible_rules.append((id, aux)) 

        memb_id, f_rules = random.choice(feasible_rules)
        rule_id = random.choice(f_rules)
        
        lhs, rhs = self.membranes[memb_id].rules[rule_id]

        for obj in lhs:
            self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects[obj] - 1
        
        parent_id = self.membranes[memb_id].parent
        for i in enumerate(rhs):
            if not(i.isdigit()):
                if rhs[i] == '.':   # disolver membrana
                    if parent_id != None:
                        for obj in self.alphabet():
                            value = self.membranes[memb_id].objects[obj]
                            self.membranes[parent_id].objects[obj] = self.membranes[parent_id].objects.get(obj, 0) + value
                    self.membranes.pop(memb_id)
                elif rhs[i] != rhs[-1] and rhs[i + 1].isdigit():  # objecto in (id membrana) o out (0)
                    self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects[obj] - 1
                    if rhs[i+1] == '0': # object out membrane
                        self.membranes[parent_id].objects[obj] = self.membranes[parent_id].objects[obj] + 1
                    elif rhs[i+1] in self.membranes[memb_id].childs:
                        self.membranes[rhs[i+1]].objects[obj] = self.membranes[rhs[i+1]].objects[obj] + 1
                else:   # adicion de objetos
                    self.membranes[memb_id].objects[obj] = self.membranes[memb_id].objects.get(rhs[i], 0) + 1


    def print_system(self):
        for memb in self.membranes:
            pass

# from PSystem import *
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aaaaac','ab'], m_rules=[[('aa','b'),('c','a')],[('c','ca')]])

ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aa',''], m_rules=[[('a','ab2c2c2'),('aa','a0a0')],[('c','.')]], i0=2)
# for c in 'a2':
#     print(c.isdigit())