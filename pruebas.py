from libPS.PSystem import *

# ~ n es divisible entre k
def k_divides_n(n,k):
    """P System that checks if a number (n) is divisible by another one (k)

        Output in membrane 3:
        - k divides n: 'a'
        - k not divides n: 'aa'

    Args:
        k (int): divisor
        n (int): dividend

    Returns:
        PSystem: return de system generated 
    """

    alphabet = ['a','c','x','d']
    struct = '122331'
    m_objects = {
                2:'a'*n+'c'*k+'d',
                3:'a'}
    r_1 = {1:('dcx','a3')}
    r_2 = {1:('ac','x'),
        2:('ax','c'),
        3:('d','d.')}
    m_rules = {
            1:r_1,
            2:r_2}
    p_rules = {2 : [(1,3),(2,3)]}
    i0 = 3
    return PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)


def k_divides_n2(n,k):
    alphabet = ['a','c','x','d','n','s']
    struct = '122331'
    m_objects = {2:'a'*n+'c'*k+'d'}
    r_1 = {1:('dcx','n3'),
           2:('d', 's3')}
    r_2 = {1:('ac','x'),
        2:('ax','c'),
        3:('d','d.')}
    m_rules = {
            1:r_1,
            2:r_2}
    p_rules = {1 : [(1,2)],
            2 : [(1,3),(2,3)]}
    i0 = 3
    return PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)

# ~ n^2
def problem_nsquared():
    """PSystem that generate a number and calulate the square of it
        Output in membrane 4:
        - m4.count(c) == m1.count(b)²

    Returns:
        PSystem: return de system generated 
    """

    alphabet = ['a','b','x','c','f']
    struct = '12334421'
    m_objects = {3:'af'}

    r_2 = {1:('x','b'),
        2:('b','bc4'),
        3:('ff','f'),
        4:('f','a.')}

    r_3 = {1:('a','ax'),
        2:('a','x.'),
        3:('f','ff')}

    m_rules = {
            2:r_2,
            3:r_3}

    p_rules = {2:[(3,4)]}
    i0 = 4
    return PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)

problem_nsquared().while_evolve(verbose=True)

# k_divides_n(15,3).while_evolve(verbose=True)
# k_divides_n(15,4).while_evolve(verbose=True)

# k_divides_n2(15,3).while_evolve(verbose=True)
# k_divides_n2(15,4).while_evolve(verbose=True)