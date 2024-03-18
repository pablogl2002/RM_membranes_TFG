import re

lhs1 = "P1P2ac[P3b[d]2[e]3]1"
lhs2 = "P1P2ac[P3b]1[d]2[e]3"
lhs3 = "P1P2ac"
rhs1 = "P2P3b[P1ac[e]2[d]3]1"
rhs2 = "P2P3b[P1ac]1[e]2[d]3"
rhs3 = "P1P2a1c0"

def expresion(lhs, rhs):
    match = re.search(r'(?m)^((?:(?!\[).)*)(.*)', lhs)
    if match:
        lhs, childs_lhs = match.group(1), match.group(2)
        membs_lhs = [(lhs, 0)]
        # lhs = P1P2ac
        if childs_lhs != "":
            match = re.sub(r'\[([^\[\]]*)\](\d*)', "", childs_lhs)
            match2 = re.findall(r'\[([^\[\]]*)\](\d*)', childs_lhs)
            if match:
                match = re.findall(r'\[([^\[\]]*)\](\d*)', match)
            else:
                match = []

            membs_lhs += match + match2
            # membs_lhs = [('P3b', '1'), ('d', '2'), ('e', '3')]
        print("membs_lhs", membs_lhs)

    match = re.search(r'(?m)^((?:(?!\[).)*)(.*)', rhs)
    if match:
        rhs, childs_rhs = match.group(1), match.group(2)
        membs_rhs = [(rhs, 0)]
        
        if childs_rhs != "":
            match = re.sub(r'\[([^\[\]]*)\](\d*)', "", childs_rhs)
            match2 = re.findall(r'\[([^\[\]]*)\](\d*)', childs_rhs)
            if match:
                match = re.findall(r'\[([^\[\]]*)\](\d*)', match)
            else:
                match = []

            membs_rhs += match + match2
        print("membs_rhs", membs_rhs)

        return membs_lhs, membs_rhs

def plasmids(rhs):
    # comprueba si la parte derecha de la regla tiene una estructura con plasmidos ej. "[P1P2a2b0c]" | "P1P2a2b0c"
    match = re.findall(r"P\d+", rhs)
    if match != []:
        rhs = re.sub(r"P\d+", "", rhs)  # obtiene el string de objetos
        plasmids_rhs = match
    else: 
        plasmids_rhs = []

    print(plasmids_rhs)
    print(rhs)


# print("lhs1, rhs1 ===>")
_, membs_rhs = expresion(lhs1, rhs1)

for rhs, memb_id in membs_rhs:
    print(f"===> {memb_id}")
    plasmids(rhs)

# print("lhs2, rhs2 ===>")
# expresion(lhs2, rhs2)

# print("lhs3, rhs3 ===>")
# expresion(lhs3, rhs3)


