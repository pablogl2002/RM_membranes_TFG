from libPS.PSystem import *

def resta_aritmética(n,m):
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
    
    r_1 = {1:("P1[p]","p[P1]"),
           2:("P2[q]","q[P2]"),
           3:("a","a3")}
    r_2 = {1:("P1[]","[P1]")}
    r_3 = {1:("P2[]","[P2]")}
    m_rules = {1:r_1,
               2:r_2,
               3:r_3}
    p_rules= {1:[],
              2:[],
              3:[]}
    i0 = 2

    return PSystem(H=plasmids, V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)



resta_aritmética(4,8).while_evolve(verbose=True)