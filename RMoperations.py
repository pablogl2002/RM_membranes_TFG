from libPS.PSystem import *

def suc(i):
    ''' Incrementa en una unidad el contenido del registro Ri 
            [i] <- [i] + 1
        sigue la ejecución
    '''    
    pass

def pre(i):
    ''' Si [i] > 0: 
            decrementa una unidad el contenido del registro Ri
                [i] <- [i] - 1
            sigue la ejecución            
        otro caso:
            sigue la ejecución
    '''
    pass

def cop():
    '''Copia registro membrana 2 a registro membrana 3
    '''
    alphabet=['a', 'c', 'x']
    plasmids = {
        "P1":{"P11":('a','x0')}
        }
    struct = '122331'
    m_objects = {
        1:'c',
        2:'a'*9
    }
    m_plasmids = {
        1: set(['P1'])
    }
    r_1 = {
        1:("P1c[a]2", "c[P1a]2"),
        2:("c[P1]2", "P1[]2"),
        3:("x","a2a3")
    }
    m_rules = {
        1:r_1
    }
    i0 = 3

    return PSystem(H=plasmids, V=alphabet, base_struct=struct, m_objects=m_objects, m_plasmids=m_plasmids, m_rules=m_rules, i0=i0)

cop().while_evolve(verbose=True)