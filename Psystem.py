from membrane import *

class PSystem:

    def __init__(self, V:list=[], base_struct="11", m_objects=[], m_rules=[], i0=1):
        self.alphabet = set(V)
        self.membranes = {}
        self.plasmids = {}
        self.outRegion = i0

        self.gen_struct(base_struct, m_objects, m_rules)
        print(self.membranes[1].feasible_rules())

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

    
# from PSystem import *
# ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aaaaac','ab'], m_rules=[[('aa','b'),('c','a')],[('c','ca')]])

ps = PSystem(V=['a','b','c'], base_struct='1221', m_objects=['aa',''], m_rules=[[('a','ab2c2c2'),('aa','a0a0')],[('c','.')]], i0=2)
# for c in 'a2':
#     print(c.isdigit())