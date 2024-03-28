from libPS.PSystem import *

def resta_aritmetica(n,m):
    alphabet = ['a','b','c','p','q']
    plasmids = {
        "P1":{"P11":('a','a0')} ,
        "P2":{"P21":('ab','c0')}
    }
    struct = '122331'
    m_objects = {
        1:'pq',
        2:'a'*n,
        3:'b'*m
    }
    
    m_plasmids = {
        0: set(['P1','P2'])
    }

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

    i0 = 3

    return PSystem(H=plasmids, V=alphabet, base_struct=struct, m_objects=m_objects, m_plasmids=m_plasmids, m_rules=m_rules, i0=i0)


def producto_aritmetico(n, m):
    alphabet = ['a','b','p','x','q','r','t','s']
    plasmids = {
        "P1":{"P11":('ba','b')},
        "P2":{"P21":('a',"ab0")},
    }
    struct = '122331'
    m_objects = {
        1:'p',
        2:'b' + 'a'*n,
        3:'b' + 'a'*m,
    }
   
    m_plasmids = {
        0: set(['P1','P2']),
    }

    r_0 = {
        1:("P1[p]1","[P1x]1"),
        2:("P2[x]1","[P2q]1"),
    }
    
    r_1 = {
        1:("P1q[a]2","r[P1a]2"),
        2:("r[P1]2","P1s[]2"),
        3:("P2s[]3","t[P2]3"),
        4:("t[P2]3","P2q[]3"),
    }
    
    m_rules = {
        0:r_0,
        1:r_1,
    }

    i0 = 1

    return PSystem(H=plasmids, V=alphabet, base_struct=struct, m_objects=m_objects, m_plasmids=m_plasmids, m_rules=m_rules, i0=i0)


# resta_aritmetica(4,10).while_evolve(verbose=True)
# producto_aritmetico(4, 5).while_evolve(verbose=True)

# print("\nresta_aritmetica(10,16) ====>")
# for i in range(100):
#     resta_aritmetica(10,16).while_evolve()
# print("\nproducto_aritmetico(9,3) ====>")
    # producto_aritmetico(9,3).while_evolve()
