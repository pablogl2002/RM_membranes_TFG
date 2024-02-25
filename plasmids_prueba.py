from libPS.PSystem import *

def problem_nsquared():
    """PSystem that generate a number and calulate the square of it
        Output in membrane 4:
        - m4.count(c) == m1.count(b)²

    Returns:
        PSystem: return de system generated 
    """

    alphabet = ['a','b','x','c','f']
    struct = '12334421'
    m_objects = {1:'',
                2:'',
                3:'af',
                4:''}

    r_2 = {1:('x','b'),
        2:('b','bc4'),
        3:('ff','f'),
        4:('f','a.')}

    r_3 = {1:('P1[a]','[ax]'),
        2:('a','x.'),
        3:('f','ff')}

    m_rules = {1:{},
            2:r_2,
            3:r_3,
            4:{}}

    p_rules = {1:[],
            2:[(3,4)],
            3:[],
            4:[]}
    i0 = 4
    return PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)

problem_nsquared().while_evolve(verbose=True)