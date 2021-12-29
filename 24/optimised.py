
from pythonised import *

def calc_factory(a, b, c):
    def calc(inp, z):
        w = inp
        x = mod_round_toward_zero(z, 26) + b
        z = div_round_toward_zero(z, a)
        if x == w:
            pass
        else:
            z = z * 26
            z = z + w + c
        return z
    return calc

calc0a = calc_factory(1, 11, 16)
calc1a = calc_factory(1, 12, 11)
calc2a = calc_factory(1, 13, 12)
calc3a = calc_factory(26, -5, 12)       # 7 is special
calc4a = calc_factory(26, -3, 12)       # 9 is special
calc5a = calc_factory(1, 14, 2)
calc6a = calc_factory(1, 15, 11)
calc7a = calc_factory(26, -16, 4)
calc8a = calc_factory(1, 14, 12)
calc9a = calc_factory(1, 15, 9)
calc10a = calc_factory(26, -7, 10)      # 2 is special
calc11a = calc_factory(26, -11, 11)
calc12a = calc_factory(26, -6, 6)       # 5 is special
calc13a = calc_factory(26, -11, 15)

