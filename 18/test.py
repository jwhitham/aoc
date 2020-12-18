
import part1
import part2
import sys

def test(expr, expect_result_1, expect_result_2):
    result = part1.calculate(expr)
    if expect_result_1 != result:
        print("part 1: error: expected", expect_result_1)
        print("got:", result)
        sys.exit(1)

    result = part2.calculate(expr)
    if expect_result_2 != result:
        print("part 2: error: expected", expect_result_2)
        print("got:", result)
        sys.exit(1)

    print("ok:", expect_result_1, expect_result_2)


test("1 + 2 * 3 + 4 * 5 + 6", 71, 231)
test("2 * 3 + (4 * 5)", 26, 46)
test("5 + (8 * 3 + 9 + 3 * 4 * 3)", 437, 1445)
test("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))", 12240, 669060)
test("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2", 13632, 23340)
test("1 + 2 * 3 + 4 * 5 + 6\n"
     "2 * 3 + (4 * 5)\n"
     "5 + (8 * 3 + 9 + 3 * 4 * 3)\n"
     "5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))\n"
     "((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2",
        13632 + 12240 + 437 + 26 + 71,
        231 + 46 + 1445 + 669060 + 23340)
