
# Ah, it's the annual question on context-free grammars.
# TBH I hoped that part 1 was going somewhere else with this...
# I'll just make sure I can actually solve it, before attempting this in Rust.

import typing

Atom = str
AtomList = typing.List[Atom] 
Molecule = str

def atomise(molecule: Molecule) -> AtomList:
    atoms: AtomList = []
    while len(molecule) > 1:
        assert molecule[0].isupper()
        if molecule[1].isupper():
            # Single letter atom
            atoms.append(molecule[:1])
            molecule = molecule[1:]
        else:
            # Double letter atom
            atoms.append(molecule[:2])
            molecule = molecule[2:]
    if len(molecule) == 1:
        atoms.append(molecule)
    return atoms


rules: typing.List[typing.Tuple[Atom, AtomList]] = []
initial_value: AtomList = []

for line in open("input", "rt"):
    fields = line.split()
    if len(fields) == 3:
        assert fields[1] == "=>"
        atoms_in = atomise(fields[0])
        assert len(atoms_in) == 1
        rules.append((atoms_in[0], atomise(fields[2])))
    elif len(fields) == 1:
        initial_value = atomise(fields[0])

rules.sort()
tokens: typing.Set[Atom] = set()

for (atom_in, atoms_out) in rules:
    tokens.add(atom_in)
    for atom_out in atoms_out:
        tokens.add(atom_out)

out: typing.List[str] = []
out.append("""
class grammar:
    tokens = (
""")
for atom in sorted(tokens):
    out.append("'TOKEN_{}',\n".format(atom.upper()))

out.append(")\n")
for atom in sorted(tokens):
    out.append("    t_TOKEN_{} = '{}'\n".format(atom.upper(), atom))

out.append("""
    t_ignore = ""

    def t_error(t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Precedence rules
    precedence = ()

    def p_root_expr(p):
        'root : e'
        p[0] = p[1]

""")

group: typing.Dict[Atom, typing.List[AtomList]] = dict()

for atom in tokens:
    group[atom] = []

for (atom_in, atoms_out) in rules:
    group[atom_in].append(atoms_out)

for atom_in in sorted(group):
    out.append(f"""
    def p_{atom_in.lower()}_base(p):
        '''{atom_in.lower()} : TOKEN_{atom_in.upper()}'''
        p[0] = 0 # ("{atom_in}", [])
""")
    for atoms_out in sorted(group[atom_in]):
        out.append(f"""

    def p_{atom_in.lower()}_{'_'.join(atoms_out)}(p):
        '''{atom_in.lower()} : """)
        for atom_out in atoms_out:
            out.append(f' {atom_out.lower()}')
        out.append(f"""'''
        p[0] = sum(p[1:]) + 1 # ("{atom_in} => {''.join(atoms_out)}", p[1:])
""")

out.append("""
    def p_error(p):
        if p is None:
            print("Syntax error (p is None)")
        else:
            print("Syntax error at '%s'" % p.value)
""")

subspace = dict(globals())
exec(compile("".join(out), "part2tmp.py", "exec"), subspace)
grammar = subspace["grammar"]

import ply.lex as lex  # type: ignore
import ply.yacc as yacc  # type: ignore

lex.lex(module=grammar)
yacc.yacc(debug=False, module=grammar)
solution = yacc.parse(''.join(initial_value))
print(solution)

