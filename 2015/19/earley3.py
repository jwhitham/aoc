import typing

class Term(object):
    def __init__(self, name: str) -> None:
        self.name = name
    def __str__(self) -> str:
        return self.name
    def __repr__(self) -> str:
        return self.name

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
    def __init__(self, name: str, *productions: Production) -> None:
        Term.__init__(self, name)
        self.productions = list(productions)
    def __repr__(self) -> str:
        return "%s -> %s" % (self.name, " | ".join(repr(p) for p in self.productions))
    def add(self, *productions) -> None:
        self.productions.extend(productions)

class State(object):
    def __init__(self, name: str, production: Production, dot_index: int,
                    start_column: "Column") -> None:
        self.name = name
        self.production = production
        self.start_column = start_column
        self.end_column = None
        self.dot_index = dot_index
        self.rules = [t for t in production if isinstance(t, Rule)]
    def __repr__(self) -> str:
        terms = [str(p) for p in self.production]
        terms.insert(self.dot_index, u"$")
        return "%-5s -> %-16s [%s-%s]" % (self.name, " ".join(terms), self.start_column, self.end_column)
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, State):
            return False
        return (self.name, self.production, self.dot_index, self.start_column) == \
            (other.name, other.production, other.dot_index, other.start_column)
    def __ne__(self, other: object) -> bool:
        return not (self == other)
    def __hash__(self) -> int:
        return hash((self.name, self.production))
    def completed(self) -> bool:
        return self.dot_index >= len(self.production)
    def next_term(self) -> typing.Optional[Term]:
        if self.completed():
            return None
        return self.production[self.dot_index]

class Column(object):
    def __init__(self, index, token) -> None:
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
    def add(self, state) -> bool:
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
    def __init__(self, value, children) -> None:
        self.value = value
        self.children = children
    def print_(self, level = 0) -> None:
        print("  " * level + str(self.value))
        for child in self.children:
            child.print_(level + 1)

def predict(col: Column, rule: Rule) -> None:
    for prod in rule.productions:
        col.add(State(rule.name, prod, 0, col))

def scan(col: Column, state: State, term: Term) -> None:
    token = term.name
    if token != col.token:
        return
    col.add(State(state.name, state.production, state.dot_index + 1, state.start_column))

def complete(col: Column, state: State) -> None:
    if not state.completed():
        return
    for st in state.start_column:
        term = st.next_term()
        if not isinstance(term, Rule):
            continue
        if term.name == state.name:
            col.add(State(st.name, st.production, st.dot_index + 1, st.start_column))

GAMMA_RULE = "GAMMA"

def parse(rule, text) -> State:
    table = [Column(i, tok) for i, tok in enumerate([None] + text.lower().split())]
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
                    assert term is not None
                    scan(table[i+1], state, term)
        
        #col.print_(completedOnly = True)

    # find gamma rule in last table column (otherwise fail)
    for st in table[-1]:
        if st.name == GAMMA_RULE and st.completed():
            return st
    else:
        raise ValueError("parsing failed")

def build_trees(state):
    return build_trees_helper([], state, len(state.rules) - 1, state.end_column)

def build_trees_helper(children, state, rule_index, end_column):
    if rule_index < 0:
        return [Node(state, children)]
    elif rule_index == 0:
        start_column = state.start_column
    else:
        start_column = None
    
    rule = state.rules[rule_index]
    outputs = []
    for st in end_column:
        if st is state:
            break
        if st is state or not st.completed() or st.name != rule.name:
            continue
        if start_column is not None and st.start_column != start_column:
            continue
        for sub_tree in build_trees(st):
            for node in build_trees_helper([sub_tree] + children, state, rule_index - 1, st.start_column):
                outputs.append(node)
    return outputs


SYM = Rule("SYM", Production(Term("a")))
OP = Rule("OP", Production(Term("+")))
EXPR = Rule("EXPR", Production(SYM))
EXPR.add(Production(EXPR, OP, EXPR))

for i in range(1,9):
    text = " + ".join(["a"] * i)
    q0 = parse(EXPR, text)
    forest = build_trees(q0)
    print(len(forest), text)


N = Rule("N", Production(Term("time")), Production(Term("flight")), Production(Term("banana")), 
    Production(Term("flies")), Production(Term("boy")), Production(Term("telescope")))
D = Rule("D", Production(Term("the")), Production(Term("a")), Production(Term("an")))
V = Rule("V", Production(Term("book")), Production(Term("eat")), Production(Term("sleep")), Production(Term("saw")))
P = Rule("P", Production(Term("with")), Production(Term("in")), Production(Term("on")), Production(Term("at")),
    Production(Term("through")))

PP = Rule("PP")
NP = Rule("NP", Production(D, N), Production(Term("john")), Production(Term("houston")))
NP.add(Production(NP, PP))
PP.add(Production(P, NP))

VP = Rule("VP", Production(V, NP))
VP.add(Production(VP, PP))
S = Rule("S", Production(NP, VP), Production(VP))

for tree in build_trees(parse(S, "book the flight through houston")):
    print("--------------------------")
    tree.print_()

for tree in build_trees(parse(S, "john saw the boy with the telescope")):
    print("--------------------------")
    tree.print_()











