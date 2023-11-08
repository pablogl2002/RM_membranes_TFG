
class Membrane:

    def __init__(self, id, parent, childs, plasmids, rules:dict={}, objects:dict={}):
        self.membrane = {
            "id": id,
            "parent": parent,
            "childs": childs,
            "plasmids": plasmids,
            "rules": rules,
            "objects": objects
        }

    def add_rule(self, rule, prio=0):
        self.membrane["rules"] = self.membrane["rules"].get(rule, 0) + prio
        if self.min_prio < prio: self.min_prio = prio
    
    def iteration(self):
        act_prio = 0
        minor_prior = set()
        for rule, prio in self.rules.items:
            if prio > act_prio:
                minor_prior.add((rule, prio))
            else:
                pass