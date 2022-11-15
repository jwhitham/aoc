
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
import collections

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


class Rule:
    def __init__(self) -> None:
        self.number = 0

    def __str__(self) -> str:
        return "Rule{}".format(self.number)

class ProductionRule(Rule):
    def __init__(self) -> None:
        Rule.__init__(self)
        self.productions: typing.List[typing.List[Rule]] = []

    def __str__(self) -> str:
        out: typing.List[str] = []
        out.append(Rule.__str__(self))
        for production in self.productions:
            if len(out) == 1:
                out.append(" =")
            else:
                out.append("\n    |")
            for rule in production:
                out.append(" ")
                out.append(Rule.__str__(rule))

        return "".join(out)

class TerminalRule(Rule):
    def __init__(self, atom: Atom) -> None:
        Rule.__init__(self)
        self.terminal = atom

    def __str__(self) -> str:
        return "{} = terminal('{}')".format(Rule.__str__(self), self.terminal)

def read_input() -> typing.Tuple[ProductionRule, AtomList, typing.List[Rule]]:
    production_rules: typing.Dict[Atom, ProductionRule] = collections.defaultdict(lambda: ProductionRule())
    target_terminals: AtomList = []
    source_rule: typing.Optional[ProductionRule] = None

    for line in open("input", "rt"):
        fields = line.split()
        if len(fields) == 3:
            assert fields[1] == "=>"
            atoms_in = atomise(fields[0])
            assert len(atoms_in) == 1
            atoms_out = atomise(fields[2])

            atom_in = atoms_in[0]
            production_rules[atom_in].productions.append([
                    production_rules[atom_out] for atom_out in atoms_out])

        elif len(fields) == 1:
            assert len(target_terminals) == 0
            target_terminals = atomise(fields[0])

        else:
            assert len(fields) == 0

    terminal_rules: typing.Dict[Atom, TerminalRule] = dict()
    all_rules: typing.List[Rule] = []
    for atom_in in production_rules:
        pr = production_rules[atom_in]
        tr = TerminalRule(atom_in)
        pr.productions.append([tr])
        terminal_rules[atom_in] = tr
        all_rules.append(pr)
        if atom_in == "e":
            assert source_rule is None
            source_rule = pr
        all_rules.append(tr)

    for (i, rule) in enumerate(all_rules):
        rule.number = i

    assert len(target_terminals) != 0
    assert source_rule is not None

    for rule in all_rules:
        print(str(rule))

    return (source_rule, target_terminals, all_rules)

class State:
    def __init__(self, rule: Rule, production: typing.List[Rule],
                       dot_position: int, input_position: int) -> None:
        self.rule = rule
        self.production = production
        self.dot_position = dot_position
        self.input_position = input_position

    def get_next(self) -> typing.Optional[Rule]:
        if self.dot_position >= len(self.production):
            return None
        else:
            return self.production[self.dot_position]

    def __eq__(self, other: object) -> bool:
        return (isinstance(other, State)
                and (self.rule == other.rule)
                and (self.production == other.production)
                and (self.dot_position == other.dot_position)
                and (self.input_position == other.input_position))

    def __str__(self) -> str:
        return ("State(" + ','.join([
                        Rule.__str__(self.rule),
                        "[" + ','.join([Rule.__str__(r) for r in self.production]) + ']',
                        str(self.dot_position), str(self.input_position)]) + ")")


class States(list):
    def __init__(self) -> None:
        list.__init__(self)

    def add(self, item: State) -> None:
        if item in self:
            return
        self.append(item)

def earley_parser() -> None:
    (source_rule, target_terminals, all_rules) = read_input()
    print("")

    states = [States() for i in range(len(target_terminals) + 1)]
    for production in source_rule.productions:
        states[0].add(State(rule=source_rule, production=production, dot_position=0, input_position=0))

    for k in range(len(target_terminals) + 1):
        i = 0
        while i < len(states[k]):
            state = states[k][i]
            rule = state.get_next()
            if rule is not None:
                print(k, i, Rule.__str__(rule))
            else:
                print(k, i, None)
            i += 1
            if rule is not None:
                if isinstance(rule, ProductionRule):
                    print("predictor")
                    for production in rule.productions:
                        s = State(rule=rule, production=production,
                                  dot_position=0, input_position=k)
                        print("  " + str(s))
                        states[k].add(s)
                else:
                    print("scanner")
                    assert isinstance(rule, TerminalRule)
                    if (k < len(target_terminals)) and (rule.terminal == target_terminals[k]):
                        s = State(rule=state.rule,
                                  production=state.production,
                                  dot_position=state.dot_position + 1,
                                  input_position=state.input_position)
                        print("  " + str(s))
                        states[k + 1].add(s)
            else:
                print("complete")
                for state2 in states[state.input_position]:
                    rule = state2.get_next()
                    if isinstance(rule, ProductionRule) and rule == state.rule:
                        s = State(rule=state2.rule,
                                  production=state2.production,
                                  dot_position=state2.dot_position + 1,
                                  input_position=state2.input_position)
                        print("  {} -> {}".format(s, k))
                        states[k].add(s)
    for state in states[-1]:
        if state.rule == source_rule:
            rule = state.get_next()
            if rule is None:
                print("accepted")
                print(str(state))

    print("?")

earley_parser()



