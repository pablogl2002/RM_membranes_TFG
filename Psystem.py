import membrane

class PSystem:

    def __init__(self, H=0, membranes:dict={}, plasmids=None, i0=None):
        self.membNum = H
        self.membranes = membranes
        self.plasmids = plasmids
        self.outRegion = i0