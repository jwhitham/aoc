import typing

class Atom:
    def __init__(self, symbol) -> None:
        self.symbol = symbol
    def __str__(self) -> str:
        return self.symbol
    def __repr__(self) -> str:
        return self.symbol
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Atom):
            return False
        return self.symbol == other.symbol
    def __hash__(self) -> int:
        return hash(self.symbol)

GAMMA_RULE = Atom("GAMMA")
NO_ATOM = Atom("")
AtomList = typing.List[Atom] 
Table = typing.List["Column"]

def atomise(molecule: str) -> AtomList:
    atoms: AtomList = []
    while len(molecule) > 1:
        assert molecule[0].isupper()
        if molecule[1].isupper():
            # Single letter atom
            atoms.append(Atom(molecule[:1]))
            molecule = molecule[1:]
        else:
            # Double letter atom
            atoms.append(Atom(molecule[:2]))
            molecule = molecule[2:]
    if len(molecule) == 1:
        atoms.append(Atom(molecule))
    return atoms


class Term(object):
    def __init__(self, atom: Atom) -> None:
        self.atom = atom
    def __str__(self) -> str:
        return str(self.atom)
    def __repr__(self) -> str:
        return repr(self.atom)

class Token(Term):
    def __init__(self, token: Atom) -> None:
        Term.__init__(self, token)
        self.token = token
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Token):
            return False
        return self.token == other.token
    def __hash__(self) -> int:
        return hash(self.token)

class Production(object):
    def __init__(self, *terms: Term) -> None:
        self.terms = terms
    def __len__(self) -> int:
        return len(self.terms)
    def __getitem__(self, index) -> Term:
        return self.terms[index]
    def __iter__(self) -> typing.Iterator[Term]:
        return iter(self.terms)
    def __repr__(self) -> str:
        return " ".join(str(t) for t in self.terms)
    def __eq__(self, other) -> bool:
        if not isinstance(other, Production):
            return False
        return self.terms == other.terms
    def __ne__(self, other) -> bool:
        return not (self == other)
    def __hash__(self) -> int:
        return hash(self.terms)

class Rule(Term):
    def __init__(self, atom: Atom, *productions: Production) -> None:
        Term.__init__(self, atom)
        self.productions = list(productions)
    def __repr__(self) -> str:
        return "%s -> %s" % (self.atom, " | ".join(repr(p) for p in self.productions))
    def add(self, *productions) -> None:
        self.productions.extend(productions)

class Action(object):
    def __init__(self, replace_this: AtomList, replacement: AtomList, where: int) -> None:
        self.replace_this = replace_this
        self.replacement = replacement
        self.where = where
    def __str__(self) -> str:
        return "%s -> %s at %s" % (self.replace_this, self.replacement, self.where)
    def __repr__(self) -> str:
        return str(self)
    def apply(self, text: AtomList) -> AtomList:
        assert text[self.where:self.where + len(self.replace_this)] == self.replace_this, (
            text[self.where:self.where + len(self.replace_this)], self.replace_this)

        return text[:self.where] + self.replacement + text[self.where + len(self.replace_this):]

class State(object):
    def __init__(self, atom: Atom, production: Production, dot_index: int,
                    start_column: "Column") -> None:
        self.atom = atom
        self.production = production
        self.start_column = start_column
        self.end_column: typing.Optional[Column] = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
    def __repr__(self) -> str:
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % (self.atom, " ".join(terms), self.start_column, self.end_column)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False
        return (self.atom, self.production, self.dot_index, self.start_column) == \
            (other.atom, other.production, other.dot_index, other.start_column)
    def __ne__(self, other: object) -> bool:
        return not (self == other)
    def __hash__(self) -> int:
        return hash((self.atom, self.production))
    def completed(self) -> bool:
        return self.dot_index >= len(self.production)
    def next_term(self) -> typing.Optional[Term]:
        if self.completed():
            return None
        return self.production[self.dot_index]
    def action(self) -> typing.Optional[Action]:
        if len(self.rules) == 0:
            # Terminal only
            return None
        elif self.atom == GAMMA_RULE:
            # Initialisation only
            return None
        else:
            terms = [p.atom for p in self.production]
            return Action([self.atom], terms, self.start_column.index)

class Column(object):
    def __init__(self, index: int, token: Token) -> None:
        self.index = index
        self.token = token
        self.states: typing.List[State] = []
        self._unique: typing.Set[State] = set()
    def __str__(self) -> str:
        return str(self.index)
    def __len__(self) -> int:
        return len(self.states)
    def __iter__(self) -> typing.Iterator[State]:
        return iter(self.states)
    def __getitem__(self, index) -> State:
        return self.states[index]
    def enumfrom(self, index) -> typing.Generator[typing.Tuple[int, State], None, None]:
        for i in range(index, len(self.states)):
            yield i, self.states[i]
    def add(self, state: State) -> bool:
        if state not in self._unique:
            self._unique.add(state)
            state.end_column = self
            self.states.append(state)
            return True
        return False
    def print_(self, completedOnly = False) -> None:
        print("[%s] %r" % (self.index, self.token))
        print("=" * 35)
        for s in self.states:
            if completedOnly and not s.completed():
                continue
            print(repr(s))
        print()

class Node(object):
    def __init__(self, value: State, children: typing.List["Node"]) -> None:
        self.value = value
        self.children = children
    def __str__(self) -> str:
        return "Node({})".format(self.value)

    def print_(self, level = 0) -> None:
        print("  " * level + str(self.value))
        for child in self.children:
            child.print_(level + 1)
    def collect(self) -> typing.List[State]:
        c = [self.value]
        for child in self.children:
            c.extend(child.collect())
        return c

def predict(col: Column, rule: Rule) -> None:
    for prod in rule.productions:
        col.add(State(rule.atom, prod, 0, col))

def scan(col: Column, state: State, token: Token) -> None:
    if token != col.token:
        return
    col.add(State(state.atom, state.production, state.dot_index + 1, state.start_column))

def complete(col: Column, state: State) -> None:
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        if term.atom == state.atom:
            col.add(State(st.atom, st.production, st.dot_index + 1, st.start_column))

def parse(rule: Rule, text: AtomList) -> typing.Tuple[State, Table]:
    table = [Column(i, Token(tok)) for i, tok in enumerate([NO_ATOM] + text)]
    table[0].add(State(GAMMA_RULE, Production(rule), 0, table[0]))

    for i, col in enumerate(table):
        for state in col:
            if state.completed():
                complete(col, state)
            else:
                term = state.next_term()
                if isinstance(term, Rule):
                    predict(col, term)
                elif i + 1 < len(table):
                    assert isinstance(term, Token)
                    scan(table[i+1], state, term)
        
        #col.print_(completedOnly = True)

    # find gamma rule in last table column (otherwise fail)
    for st in table[-1]:
        if st.atom == GAMMA_RULE and st.completed():
            return (st, table)
    else:
        raise ValueError("parsing failed")

def build_trees(state: State, depth: int) -> typing.List[Node]:
    assert state.end_column is not None
    return build_trees_helper([], state, len(state.rules) - 1, state.end_column, depth)

def build_trees_helper(children: typing.List[Node], state: State,
                       rule_index: int, end_column: Column, depth: int) -> typing.List[Node]:
    if rule_index < 0:
        # beginning of the production
        return [Node(state, children)]
    elif rule_index == 0:
        # first rule in the production
        start_column: typing.Optional[Column] = state.start_column
    else:
        start_column = None
   
    # at the root, state is the gamma rule, and rule is e
    rule = state.rules[rule_index]
    D = 2
    if depth <= D:
        print("begin", depth)
        print("state =", state)
    outputs = []
    for st in end_column:
        # st must appear in the column before state:
        if st is state:
            break
        # skip anything incomplete
        # skip anything that belongs to some other rule
        if not st.completed() or st.atom != rule.atom:
            continue
        # if we're looking for the first rule in the production, match the column
        if start_column is not None and st.start_column != start_column:
            continue

        # st is a completed state
        # where st.atom == rule.atom
        # and st.end_column == end_column
        assert st.end_column == end_column

        if depth <= D:
            print("st =", state)

        # match the earlier rule in the production (if any)
        for sub_tree in build_trees_helper(
                    children=[],
                    state=st,
                    rule_index=len(st.rules) - 1,
                    end_column=end_column,
                    depth=depth + 1):
           
            if depth <= D:
                print("sub_tree =", sub_tree)
            for node in build_trees_helper(
                        children=[sub_tree] + children,
                        state=state,
                        rule_index=rule_index - 1,
                        end_column=st.start_column,
                        depth=depth + 1):
                if depth <= D:
                    print("node =", node)
                    print("end", depth)
                outputs.append(node)
                return outputs
    return outputs

def main() -> None:
    known_atoms: typing.Dict[Atom, Rule] = dict()
    target: AtomList = []

    for line in open("input", "rt"):
        fields = line.split()
        if len(fields) == 3:
            assert fields[1] == "=>"
            atoms_in = atomise(fields[0])
            assert len(atoms_in) == 1
            atoms_out = atomise(fields[2])

            for atom in atoms_in + atoms_out:
                if atom not in known_atoms:
                    known_atoms[atom] = Rule(atom, Production(Token(atom)))

            atom_in = atoms_in[0]
            p = [known_atoms[atom_out] for atom_out in atoms_out]
            known_atoms[atom_in].add(Production(*p))

        elif len(fields) == 1:
            assert len(target) == 0
            target = atomise(fields[0])

        else:
            assert len(fields) == 0

    assert len(target) != 0
    root = known_atoms[Atom("e")]
    (q0, table) = parse(root, target)

    for i in range(len(table)):
        col = table[i]
        print(f"column {i} token {col.token}")
        for j in range(len(col)):
            state = col[j]
            if state.completed():
                print(f"  row {j} state {state}")
        print("")

    try:
        if a_pox_on_this(table, 0, len(table) - 1, GAMMA_RULE, 0):
            print("matched")
        else:
            print("not matched")
    except Exception as e:
        print("crash", e)

def look_left(table: Table,
              stop_left_index: int,
              left_index: int,
              right_index: int, state: State,
              term_index: int, level: int) -> bool:

    if term_index < 0:
        print(f"{level}: accept")
        return True
    if left_index < stop_left_index:
        print(f"{level}: reject")
        return False

    assert right_index >= left_index
    term = state.production.terms[term_index]

    if isinstance(term, Token):
        print(f"{level}: match for terminal {term.atom} at {left_index} .. {right_index}")
        return look_left(table, stop_left_index, left_index, right_index - 1, state, term_index - 1, level + 1)
    else:
        if a_pox_on_this(table, left_index, right_index, term.atom, level + 1):
            print(f"{level}: match for rule {term.atom} in {left_index} .. {right_index}")
            return look_left(table, stop_left_index, left_index, right_index - 1, state, term_index - 1, level + 1)
        else:
            print(f"{level}: no match for {term.atom} in {left_index} .. {right_index}")
            return look_left(table, stop_left_index, left_index - 1, right_index, state, term_index, level + 1)


def a_pox_on_this(table: Table, left_index: int,
                  right_index: int, atom: Atom, level: int) -> bool:

    left_col = table[left_index]
    right_col = table[right_index]
    for j in range(len(right_col) - 1, -1, -1):
        state = right_col[j]
        if ((state.atom == atom)
        and (state.start_column == left_col)
        and state.completed()):
            # found... step down
            print(f"{level}: found {state}")
            if look_left(table, left_index, right_index, right_index, state, len(state.production.terms) - 1, level + 1):
                return True

    return False

if __name__ == "__main__":
    main()
