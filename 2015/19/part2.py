
# Ah, it's the annual question on context-free grammars.
# TBH I hoped that part 1 was going somewhere else with this...
# I'll just make sure I can actually solve it, before attempting this in Rust.
#
# .. yes, as in, the answer is accepted by the AOC website.
# But there are shift/reduce conflicts in the grammar, so it's
# not LALR(1). "ply" only supports LALR(1) and SLR. The default
# behaviour of "ply" is to shift, and that seems to lead to the expected
# answer in this case, but not all - for example, "HOHOHO" can't be solved
# by this. The shift/reduce conflicts block moving to the "plex"
# crate in Rust because that requires a grammar with no
# conflicts. However, I can also try the "lalrpop" crate, this
# seems to offer choices beyond LALR(1).
#
# lalrpop is easier to use than plex. In lalrpop the grammar is written
# in a DSL that is partly Rust, and the parser code is generated from that.
# This integrates nicely with "cargo build", which includes the ability to
# run "build scripts" (Rust programs) during the build - this is great
# for supporting parser generators. In contrast, plex uses Rust macros
# to define the grammar, which is very clever but can result in errors that
# are hard to understand, and it requires a nightly build of Rust because
# the relevant features did not become part of the stable version at any
# point between 2017 and 2022. It took ages to figure out how to
# express a grammar in a form that plex could understand, whereas
# lalrpop made this easy. The only wonkiness with lalrpop was that its
# tutorial has an unstated assumption that source files are in a "src"
# subdirectory, this led to a difficult-to-debug build error when the parser
# file was generated in an unexpected place.
#
# Unfortunately lalrpop can't be used to solve the problem either,
# even with its LR(1) parser, as the grammar is ambiguous. 
#
# A simpler method must be intended, though I did already try various
# obvious simple tricks in the hope of having to avoid dealing with
# parsers. 


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
grammar;
""")

out.append("""
pub Root: u32 = {
    <x:Rule_e> => x,
}
""")

group: typing.Dict[Atom, typing.List[AtomList]] = dict()

for atom in tokens:
    group[atom] = []

for (atom_in, atoms_out) in rules:
    group[atom_in].append(atoms_out)

for atom_in in sorted(group):
    out.append(f"""
Rule_{atom_in.lower()}: u32 = """)
    out.append(r"{" + "\n")
    for atoms_out in sorted(group[atom_in]):
        out.append('   ')
        for (num, atom_out) in enumerate(atoms_out):
            out.append(f' <x{num}:Rule_{atom_out.lower()}>')
        out.append(f' => 1')
        for (num, _) in enumerate(atoms_out):
            out.append(f' + x{num}')
        out.append(',\n')
    out.append(f"""
    TOKEN_{atom_in.upper()},
""")
    out.append(r'}' + "\n")

for atom in sorted(tokens):
    out.append('TOKEN_{}: u32 = <s:r"{}"> => 0;\n'.format(
                atom.upper(), atom.upper()))

subspace = dict(globals())
open("calculator1.lalrpop", "wt").write(''.join(out))
