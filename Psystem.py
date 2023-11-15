import membrane

class PSystem:

    def __init__(self, H=0, membranes:dict={}, rules:dict={}, plasmids=None, i0=None):
        self.membNum = H
        self.membranes = membranes
        self.rules = rules
        self.plasmids = plasmids
        self.outRegion = i0
    


    # def add_rule(self, rule, prio=0):
    #     self.membrane["rules"] = self.membrane["rules"].get(rule, 0) + prio
    #     if self.min_prio < prio: self.min_prio = prio    