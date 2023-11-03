
class Membrane:

    def __init__(self, id, multisets:dict=None, rules:dict=None):
        self.id = id
        self.multisets = multisets if multisets != None else {}
        self.rules = rules if rules != None else {}
        self.min_prio = 0

    def add_rule(self, rule, prio=0):
        self.rules = self.rules.get(rule, 0) + prio
        if self.min_prio < prio: self.min_prio = prio
    
    def iteration(self):
        act_prio = 0
        minor_prior = set()
        for rule, prio in self.rules.items:
            if prio > act_prio:
                minor_prior.add((rule, prio))
            else:
                pass
        
