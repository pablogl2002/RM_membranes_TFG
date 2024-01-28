
# PSystem python library

Library that allows you to create P Systems and evolve them.
## PSystem class and its functions

### How to create a PSystem object?

ps = PSystem(V, base_struct, m_objects, m_rules, p_rules, i0)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `V` | `list` | System's alphabet. Defaults to [] |
| `base_struct` | `str` | Initial system's structure. Defaults to "11" |
| `m_objects` | `dict` | Membrane's objects. Defaults to {} |
| `m_rules` | `dict` | Membrane's rules. Defaults to {} |
| `p_rules` | `dict` | Rules priority in each membrane. Defaults to {}|
| `i0` | `int` | Output membrane. Defaults to 1 |

### ps.steps(n, verbose=False)
Evolve the system 'n' steps. If verbose is True, prints system's structure in each step

### ps.while_evolve(verbose=False)
Evolve the system until finish all possible iterations. If verbose is True, prints system's structure in each step

### ps.evolve(feasible_rules, verbose=False)
Evolve the system choosing a random membrane from feasible_rules list whose items are a tuple of membrane's id and their rules to apply. If verbose is True, prints the membrane where the rules are being applied, the rules applied and the number of times each rule has been applied.

### ps.get_fesible_rules()
Get feasible rules from all the membranes in the current state 

### ps.print_system()
Print system's structure

## Membrane class and its functions

### How to create a membrane

memb = Membrane(V, id, parent, objects, rules, p_rules)

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `V` | `list` | Membrane's alphabet (same as system's) |
| `id` | `int` | Membrane's id |
| `parent` | `int` | Parent Membrane's id. Defaults to None |
| `objects` | `str` | Membrane's objects. Defaults to '' |
| `rules` | `dict` | Membrane's rules. Defaults to {} |
| `p_rules` | `dict` | Rules priority in membrane. Defaults to {} |

### memb.add_child(child_id)
Add child with id 'child_id' to the membrane 'memb'

### memb.add_plasmids(plasmids)
Add all plasmid in 'plasmids:list' to the membrane (not working, because not implemented plasmids yet)

### memb.add_objects(objects)
Add all the objects in 'objects:string' to the membrane 'memb'

### memb.get_feasible_rules()
Get a combination of rules that can be applied all at once in the membrane

## Examples

### _n_ squared

A **P** System generating _n²_, _n_ >= 1

![A **P** System generating n², n >= 1](assets/PSystem_n_squared.png)

```python
from libPS.PSystem import *

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

r_3 = {1:('a','ax'),
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
ps = PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)

ps.while_evolve(verbose=True)
```

#### Output
```terminal
[1 '' [2 '' [3 'af' ]3[4 '' ]4]2]1

--------------------------------------------------------------------------------------------

[membrane 3] rules applied : [3, 1]
memb_id: 3 | n_times: 1 -> rule: ('f', 'ff')
memb_id: 3 | n_times: 1 -> rule: ('a', 'ax')
[1 '' [2 '' [3 'affx' ]3[4 '' ]4]2]1

--------------------------------------------------------------------------------------------

[membrane 3] rules applied : [3, 2]
memb_id: 3 | n_times: 2 -> rule: ('f', 'ff')
memb_id: 3 | n_times: 1 -> rule: ('a', 'x.')
[1 '' [2 'ffffxx' [4 '' ]4]2]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [1, 3]
memb_id: 2 | n_times: 2 -> rule: ('x', 'b')
memb_id: 2 | n_times: 2 -> rule: ('ff', 'f')
[1 '' [2 'bbff' [4 '' ]4]2]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [2, 3]
memb_id: 2 | n_times: 2 -> rule: ('b', 'bc4')
memb_id: 2 | n_times: 1 -> rule: ('ff', 'f')
[1 '' [2 'bbf' [4 'cc' ]4]2]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [2, 4]
memb_id: 2 | n_times: 2 -> rule: ('b', 'bc4')
memb_id: 2 | n_times: 1 -> rule: ('f', 'a.')
[1 'abb' [4 'cccc' ]4]1

--------------------------------------------------------------------------------------------

============================================================================================

{'a': 0, 'b': 0, 'f': 0, 'c': 4, 'x': 0}
```
### k divides n

A **P** system that checks if a number _n_ is divisible by another number _k_. 


![A **P** system deciding whether k divides n](assets/PSystem_k_divides_n.png)

In this case _k_ = 3 divides _n_ = 15 .

```python
from libPS.PSystem import *

n = 15
k = 3

alphabet = ['a','c','x','d']
struct = '122331'
m_objects = {1:'',
            2:'a'*n+'c'*k+'d',
            3:'a'}
r_1 = {1:('dcx','a3')}
r_2 = {1:('ac','x'),
    2:('ax','c'),
    3:('d','d.')}
m_rules = {1:r_1,
        2:r_2,
        3:{}}
p_rules = {1 : [],
        2 : [(1,3),(2,3)],
        3 : []}
i0 = 3
ps = PSystem(V=alphabet, base_struct=struct, m_objects=m_objects, m_rules=m_rules, p_rules=p_rules, i0=i0)

ps.while_evolve(verbose=True)
```
#### Output
```terminal
[1 '' [2 'cccdaaaaaaaaaaaaaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [1]
memb_id: 2 | n_times: 3 -> rule: ('ac', 'x')
[1 '' [2 'daaaaaaaaaaaaxxx' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [2]
memb_id: 2 | n_times: 3 -> rule: ('ax', 'c')
[1 '' [2 'cccdaaaaaaaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [1]
memb_id: 2 | n_times: 3 -> rule: ('ac', 'x')
[1 '' [2 'daaaaaaxxx' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [2]
memb_id: 2 | n_times: 3 -> rule: ('ax', 'c')
[1 '' [2 'cccdaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [1]
memb_id: 2 | n_times: 3 -> rule: ('ac', 'x')
[1 '' [2 'dxxx' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [3]
memb_id: 2 | n_times: 1 -> rule: ('d', 'd.')
[1 'dxxx' [3 'a' ]3]1

--------------------------------------------------------------------------------------------

============================================================================================

{'c': 0, 'd': 0, 'a': 1, 'x': 0}
```

In this other case _k_ = 4 not divides _n_ = 15.

```terminal
[1 '' [2 'ccccdaaaaaaaaaaaaaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [1]
memb_id: 2 | n_times: 4 -> rule: ('ac', 'x')
[1 '' [2 'dxxxxaaaaaaaaaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [2]
memb_id: 2 | n_times: 4 -> rule: ('ax', 'c')
[1 '' [2 'ccccdaaaaaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [1]
memb_id: 2 | n_times: 4 -> rule: ('ac', 'x')
[1 '' [2 'dxxxxaaa' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [2]
memb_id: 2 | n_times: 3 -> rule: ('ax', 'c')
[1 '' [2 'cccdx' ]2[3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 2] rules applied : [3]
memb_id: 2 | n_times: 1 -> rule: ('d', 'd.')
[1 'cccdx' [3 'a' ]3]1

--------------------------------------------------------------------------------------------

[membrane 1] rules applied : [1]
memb_id: 1 | n_times: 1 -> rule: ('dcx', 'a3')
[1 'cc' [3 'aa' ]3]1

--------------------------------------------------------------------------------------------

============================================================================================

{'c': 0, 'd': 0, 'x': 0, 'a': 2}

```

## Notation

### Parameters

Using as example a **P** system deciding whether k divides n, which was used as example of use before:

<table>
    <thead>
        <tr>
            <th>Object</th>
            <th>Parameter</th>
            <th>In code</th>
            <th>In traditional notation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td align="center">PSystem <br> All membs</td>
            <td align="center">alphabet</td>
            <td align="center">['a','c','x','d']</td>
            <td align="center">{a,c,c',d}</td>
        </tr>
        <tr>
            <td align="center">PSystem</td>
            <td align="center">struct</td>
            <td align="center">'122331'</td>
            <td align="center">[<sub>1</sub> [<sub>2</sub> ]<sub>2</sub> [<sub>3</sub> ]<sub>3</sub> ]<sub>1</sub></td>
        </tr>
        <tr>
            <td align="center">memb1</td>
            <td align="center">objects</td>
            <td align="center">''</td>
            <td align="center">&lambda;</td>
        </tr>
        <tr>
            <td align="center">memb2</td>
            <td align="center">objects</td>
            <td align="center">'a'*n+'c'*k+'d'</td>
            <td align="center">a<sup>n</sup>c<sup>k</sup>d</td>
        </tr>
        <tr>
            <td align="center">memb3</td>
            <td align="center">objects</td>
            <td align="center">'a'</td>
            <td align="center">a</td>
        </tr>
        <tr>
            <td align="center">memb1</td>
            <td align="center">rules</td>
            <td align="center">{ 1: ('dcx', 'a3')}</td>
            <td align="center">{ dcc' &rarr; (a, in<sub>3</sub>)}</td>
        </tr>
        <tr>
            <td align="center">memb2</td>
            <td align="center">rules</td>
            <td align="center">{ 1:('ac', 'x'),<br>2:('ax', 'c'),<br>3:('d', 'd.') }</td>
            <td align="center">{ r1: ac &rarr; c',<br>r2: ac' &rarr; c,<br>r3: d &rarr; d&delta; }</td>
        </tr>
        <tr>
            <td align="center">memb3</td>
            <td align="center">rules</td>
            <td align="center">{}</td>
            <td align="center">&Oslash;</td>
        </tr>
        <tr>
            <td align="center">memb1</td>
            <td align="center">p_rules</td>
            <td align="center">[]</td>
            <td align="center">&Oslash;</td>
        </tr>
        <tr>
            <td align="center">memb2</td>
            <td align="center">p_rules</td>
            <td align="center">[ (1,3), (2,3) ]</td>
            <td align="center">{ r1 > r3,r2 > r3 }</td>
        </tr>
        <tr>
            <td align="center">memb3</td>
            <td align="center">p_rules</td>
            <td align="center">[]</td>
            <td align="center">&Oslash;</td>
        </tr>
        <tr>
            <td align="center">PSystem</td>
            <td align="center">m_rules</td>
            <td align="center">{ 1 : memb1.rules,<br>2 : memb2.rules,<br>3 : memb3.rules }</td>
            <td align="center">R<sub>1</sub>, R<sub>2</sub>, R<sub>3</sub></td>
        </tr>
        <tr>
            <td align="center">PSystem</td>
            <td align="center">p_rules</td>
            <td align="center">{ 1 : memb1.p_rules,<br>2 : memb2.p_rules,<br>3 : memb3.p_rules }</td>
            <td align="center">&rho;<sub>1</sub>, &rho;<sub>2</sub>, &rho;<sub>3</sub></td>
        </tr>
    </tbody>
</table>

### Rules

<table>
    <thead>
        <tr>
            <th>Description</th>
            <th>In code</th>
            <th>In traditional notation</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Add an object to a membrane</td>
            <td align="center">Using 2 to enter to memb2 <br> ( 'a', 'ab2' )</td>
            <td align="center">Using in<sub>2</sub> to enter to memb2 <br>a &rarr; a (b,in<sub>2</sub>)</td>
        </tr>
        <tr>
            <td>An object will exit the membrane</td>
            <td align="center">Using 0 to exit the membrane<br>( 'a', 'a0' )</td>
            <td align="center">Using out to exit the membrane<br>a &arr; (a, out)</td>
        </tr>
        <tr>
            <td>Remove a membrane (dissolve)</td>
            <td align="center">Using '.' to dissolve<br>( 'b', '.' )</td>
            <td align="center">Using &delta; to dissolve <br> b &rarr; &delta;</td>
        </tr>
        <tr><th></th><th></th><th></th></tr>
        <tr><td colspan=3 align="center"><b>Priority</b></td></tr>
        <tr>
            <th>Description</th>
            <th>In code</th>
            <th>In traditional notation</th>
        </tr>
        <tr>
            <td>rule1 more priority than rule2</td>
            <td align="center">( 1, 2 )</td>
            <td align="center">r1 > r2</td>
        </tr>
    </tbody>
</table>

## Authors

- [Pablo García López](https://github.com/pablogl2002)