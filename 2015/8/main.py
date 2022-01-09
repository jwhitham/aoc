# part 1's string escaping rules are the same as Python's, so use eval
a=open("input", "rt").read().replace("\n","")
print("part 1:", len(a) - len(eval("".join(a))))

# part 2 could be done with 'repr' if only repr didn't try to be
# smart, using both quote types
def enc(x):
    y = '"'
    for c in x:
        if c in r'\"':
            y += '\\'
        y += c
    y += '"'
    return y

assert enc(r'""') == r'"\"\""'
assert enc(r'"abc"') == r'"\"abc\""'
assert enc(r'"aaa\"aaa"') == r'"\"aaa\\\"aaa\""'
assert enc(r'"\x27"') == r'"\"\\x27\""'
assert len(enc(r'"\x27"')) == 11

b=[enc(x.strip()) for x in open("input", "rt")]
print("part 2:", len("".join(b)) - len(a))
