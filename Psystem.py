from membrane import *

class PSystem:

    def __init__(self, V:list=[], base_struct="11", membobjects=[], i0=None):
        self.alphabet = set(V)
        self.membranes = {}
        self.rules = {}
        self.plasmids = {}
        self.outRegion = i0

        self.gen_struct(base_struct)

    def gen_struct(self, struct):
        open = struct[0]
        id = int(open)
        self.membranes[id] = self.membranes.get(id, Membrane(V=self.alphabet, id=id, parent=None, objects='bbc'))

        for m in struct[1:]:
            if m != open[-1]:
                self.membranes[int(open[-1])].add_child(id + 1)
                id = id + 1
                memb = Membrane(V=self.alphabet, id=id, parent=open[-1], objects='aabc')
                self.membranes[id] = self.membranes.get(id, memb)
                open = open + m
            else:
                open = open[:-1]

        if open != '':
            self.membranes = {}
            print('Incorrect membrane structure')