
import re
from typing import Dict, List

def parser() -> Dict[int, List[Dict[str, int]]]:
    re_game = re.compile(r"^Game (\d+): (.*\S)\s*$")
    re_cube = re.compile(r"^\s*(\d+) (green|blue|red)\s*$")
    parsed_games = {}
    for line in open("input", "rt"):
        m = re_game.match(line)
        assert m is not None
        game_id = int(m.group(1))
        parsed_subsets = []
        for subset in m.group(2).split(";"):
            parsed_cubes = {}
            for cube in subset.split(","):
                m = re_cube.match(cube)
                assert m is not None
                count = int(m.group(1))
                colour = m.group(2)
                parsed_cubes[colour] = count
            parsed_subsets.append(parsed_cubes)
        parsed_games[game_id] = parsed_subsets
    return parsed_games

def part1() -> int:
    total = 0
    for (game_id, game) in parser().items():
        possible = True
        for subset in game:
            if ((subset.get("red", 0) > 12)
            or (subset.get("green", 0) > 13)
            or (subset.get("blue", 0) > 14)):
                possible = False
        if possible:
            total += game_id
    return total

def part2() -> int:
    total = 0
    for (game_id, game) in parser().items():
        minimum = {}
        for subset in game:
            for colour in subset:
                minimum[colour] = max(minimum.get(colour, 0),
                            subset.get(colour, 0))

        power = 1
        for colour in minimum:
            power *= minimum[colour]
        total += power
    return total

if __name__ == "__main__":
    print(part1())
    print(part2())




        
