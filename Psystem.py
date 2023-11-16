from membrane import *

class PSystem:

    def __init__(self, V=[], base_struct="11", membobjects=[], i0=None):
        self.membNum = 1
        self.membranes = {}
        self.rules = {}
        self.plasmids = {}
        self.outRegion = i0

        self.gen_struct(base_struct)

    def gen_struct(self, struct):
        open = ''
        for m in struct:
            if open == '' or m != open[-1]:
                parent = None if open == '' else open[-1]
                self.membranes[self.membNum] = self.membranes.get(self.membNum, Membrane(id=self.membNum, parent=parent, objects={}))
                open = open + m
                self.membNum = self.membNum + 1
            else:
                open = open[:-1]

        if open != '':
            self.membNum = 1
            self.membranes = {}
            print('Incorrect membrane structure')