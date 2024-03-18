from libPS.PSystem import *

def resta_aritmetica(n,m):
    alphabet = ['a','b','c','p','q']
    plasmids = {
              "P1":{"P11":('a','a0')} ,
              "P2":{"P21":('ab','c0')}
               }
    struct = '122331'
    m_objects = {0:'',
                 1:'pq',
                 2:'a'*n,
                 3:'b'*m}
    
    m_plasmids = {0: set(['P1','P2']),
                  1: set(),
                  2: set(),
                  3: set()}

    r_0 = {
        1:("P1[p]1","p[P1]1"),
        2:("P2[q]1","q[P2]1"),
    }
    
    r_1 = {
        1:("P1[]2","[P1]2"),
        2:("P2[]3","[P2]3"),
        3:("a","a3"),
    }

    m_rules = {
        0:r_0,
        1:r_1,
    }
    p_rules= {1:[],
              2:[],
              3:[]}
    i0 = 3

    return PSystem(H=plasmids, V=alphabet, base_struct=struct, m_objects=m_objects, m_plasmids=m_plasmids, m_rules=m_rules, p_rules=p_rules, i0=i0)

# resta_aritmetica(12,16).while_evolve(verbose=True)

def producto_aritmetico(n, m):
    alphabet = ['a','b','p','x','q','r','t','s']
    plasmids = {
              "P1":{"P11":('ba','b')},
              "P2":{"P21":('a',"ab0")}
               }
    
    