import membrane

class PSystem:

    def prove_struct(self, struct):
        open = struct[0]
        if open == '1':
            for m in struct[1:]:
                if m != open[-1]:
                    open = open + m
                else:
                    
                    


        

    def __init__(self, V=[], base_struct="11", membobjects=[], i0=None):
        self.membNum
        self.membranes
        self.rules
        self.plasmids
        self.outRegion = i0    