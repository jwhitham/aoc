
from pathlib import Path
import unittest
import typing

def unique_patterns(filename: Path) -> int:
    count = 0
    for display in open(filename, "rt"):
        (ten_patterns, output) = display.split("|")
        for pattern in output.split():
            if len(pattern) in [
                    2,      # value 1
                    4,      # value 4
                    3,      # value 7
                    7,      # value 8
                    ]:
                count += 1

    return count

def test_unique_patterns() -> None:
    assert unique_patterns(Path("part1test.txt")) == 26

def classify_candidates(all_patterns: typing.Set[str],
                        candidate_1: str,
                        candidate_2: str,
                        count_x: int,
                        count_y: int) -> typing.Tuple[str, str]:
    count_1 = count_2 = 0
    for pattern in all_patterns:
        if candidate_1 in pattern:
            count_1 += 1
        if candidate_2 in pattern:
            count_2 += 1

    assert count_1 != count_2
    assert count_1 in [count_x, count_y]
    assert count_2 in [count_x, count_y]
    if count_1 == count_x:
        candidate_x = candidate_1
        candidate_y = candidate_2
    else:
        candidate_x = candidate_2
        candidate_y = candidate_1

    return (candidate_x, candidate_y)

def normalise(pattern: typing.Union[str, typing.Set[str]]) -> str:
    if isinstance(pattern, str):
        pattern = set(pattern)

    for i in pattern:
        assert len(i) == 1

    return "".join(sorted(pattern))


def deduce(all_patterns: typing.Set[str]) -> typing.Dict[str, int]:
    # Expect 10 unique patterns
    assert len(all_patterns) == 10

    # Find segment a (which is 7 - 1)
    segment_cf = ""
    segment_bdcf = ""
    segment_acf = ""
    segment_abcdefg = "abcdefg"
    for pattern in all_patterns:
        if len(pattern) == 2:
            segment_cf = pattern
        if len(pattern) == 3:
            segment_acf = pattern
        if len(pattern) == 4:
            segment_bdcf = pattern

    assert segment_cf
    assert segment_bdcf
    assert segment_acf

    # Initially we know 4 of the numbers
    translation: typing.Dict[str, int] = {
            segment_cf: 1,
            segment_acf: 7,
            segment_bdcf: 4,
            segment_abcdefg: 8,
        }
            
    segment_a = normalise(set(segment_acf) - set(segment_cf))
    assert len(segment_a) == 1
    
    # Find segments bd (which is 4 - 1)
    segment_bd = normalise(set(segment_bdcf) - set(segment_cf))
    assert len(segment_bd) == 2

    # b -> 6 patterns
    # d -> 7 patterns
    (segment_b, segment_d) = classify_candidates(
                    all_patterns=all_patterns,
                    candidate_1=segment_bd[0], candidate_2=segment_bd[1],
                    count_x=6, count_y=7)
    # 0 is identified
    translation[normalise(set(segment_abcdefg) - set(segment_d))] = 0

    # c -> 8 patterns
    # f -> 9 patterns
    (segment_c, segment_f) = classify_candidates(
                    all_patterns=all_patterns,
                    candidate_1=segment_cf[0], candidate_2=segment_cf[1],
                    count_x=8, count_y=9)
    # 2, 6 are identified
    translation[normalise(set(segment_abcdefg) - set(segment_c))] = 6
    translation[normalise(set(segment_abcdefg) - set(segment_b) - set(segment_f))] = 2
    
    # Got abcdf
    # Not got eg
    # e -> 4 patterns
    # g -> 7 patterns
    segment_eg = normalise(set("abcdefg") - set(segment_acf) - set(segment_bd))
    (segment_e, segment_g) = classify_candidates(
                    all_patterns=all_patterns,
                    candidate_1=segment_eg[0], candidate_2=segment_eg[1],
                    count_x=4, count_y=7)
    # Now everything can be identified
    translation[normalise(set(segment_abcdefg) - set(segment_b) - set(segment_e))] = 3
    translation[normalise(set(segment_abcdefg) - set(segment_c) - set(segment_e))] = 5
    translation[normalise(set(segment_abcdefg) - set(segment_e))] = 9

    return translation

def normalise_line(line: str) -> typing.Set[str]:
    all_patterns: typing.Set[str] = set()
    for pattern in line.split():
        if pattern != "|":
            all_patterns.add(normalise(pattern))
    return all_patterns

def test_deduce() -> None:
    translation = deduce(normalise_line(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"))

    assert translation[normalise("ab")] == 1
    assert translation[normalise("dab")] == 7
    assert translation[normalise("eafb")] == 4
    assert translation[normalise("acedgfb")] == 8
    assert translation[normalise("cdfbe")] == 5
    assert translation[normalise("gcdfa")] == 2
    assert translation[normalise("fbcad")] == 3
    assert translation[normalise("cefabd")] == 9
    assert translation[normalise("cdfgeb")] == 6
    assert translation[normalise("cagedb")] == 0

def decode(line: str) -> int:
    translation = deduce(normalise_line(line))
    (_, output) = line.split("|")
    value = 0
    for pattern in output.split():
        value *= 10
        value += translation[normalise(pattern)]
    return value

def test_decode() -> None:
    assert decode("be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe") == 8394
    assert decode("edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc") == 9781
    assert decode("fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg") == 1197
    assert decode("fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb") == 9361
    assert decode("aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea") == 4873
    assert decode("fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb") == 8418
    assert decode("dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe") == 4548
    assert decode("bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef") == 1625
    assert decode("egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb") == 8717
    assert decode("gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce") == 4315

def decode_sum(filename: Path) -> int:
    total = 0
    for line in open(filename, "rt"):
        total += decode(line)
    return total

def main() -> None:
    print("part 1:", unique_patterns(Path("part1.txt")))
    print("part 2:", decode_sum(Path("part1.txt")))

if __name__ == "__main__":
    main()


