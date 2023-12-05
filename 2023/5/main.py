
import sys
import typing

class Range:
    def __init__(self, range_start: int, length: int) -> None:
        self.range_start = range_start
        self.length = length

class LocRange(Range):
    # Represents a location range
    def __repr__(self) -> str:
        return "LocRange({}..{})".format(self.range_start, self.range_start + self.length)

class MapRange(Range):
    # Represents a mapping range (x1..y1) -> (x2..y2)
    def __init__(self, src_range_start: int,
                    dest_range_start: int, length: int) -> None:
        Range.__init__(self, src_range_start, length)
        self.dest_range_start = dest_range_start

    def __repr__(self) -> str:
        return "MapRange({}..{} -> {}..{})".format(self.range_start,
                    self.range_start + self.length,
                    self.dest_range_start,
                    self.dest_range_start + self.length)

class Point:
    # Represents the start or end point of a range
    def __init__(self, location: int, is_start: bool, is_map: bool, link: Range) -> None:
        self.location = location
        self.is_start = is_start
        self.is_map = is_map
        self.link = link

    def priority(self) -> int:
        # Controls the sorting order for multiple points in a list
        if self.is_map:
            return 2 if self.is_start else 1
        else:
            return 3 if self.is_start else 0

    def __repr__(self) -> str:
        return "Point({} s={} m={} l={})".format(self.location,
                self.is_start, self.is_map, self.link)

    def __lt__(self, other: typing.Any) -> bool:
        if not isinstance(other, Point):
            return False
        if self.location < other.location:
            return True
        if self.location > other.location:
            return False
        if self.priority() < other.priority():
            return True
        return False

def check_ranges(ranges: typing.Sequence[Range]) -> None:
    # Check that a list of ranges is valid (Ranges must not overlap)
    try:
        points: typing.List[Point] = []
        for r in ranges:
            points.append(Point(r.range_start, True, False, r))
            points.append(Point(r.range_start + r.length, False, False, r))

        points.sort()
        expect_start = True
        expect_location = -sys.maxsize
        for point in points:
            assert point.is_start == expect_start
            if expect_start:
                assert point.location >= expect_location
            else:
                assert point.location > expect_location
            expect_start = not expect_start
            expect_location = point.location
        assert expect_start == True
    except:
        print("Overlapping or invalid ranges")
        for r in ranges:
            print(r)
        raise
        

class Map:
    # Represents a collection of mapping ranges
    # The ranges aren't allowed to overlap

    def __init__(self) -> None:
        self.map_ranges: typing.List[MapRange] = []

    def add(self, r: MapRange):
        self.map_ranges.append(r)
        check_ranges(self.map_ranges)

    def remap(self, cur_loc_ranges: typing.List[LocRange]) -> typing.List[LocRange]:

#       print("")
#       print("IN")
        check_ranges(cur_loc_ranges)

        # Get a list of all of the points where a range begins or ends
        points: typing.List[Point] = []
        r: Range
        for r in self.map_ranges:
            points.append(Point(r.range_start, True, True, r))
            points.append(Point(r.range_start + r.length, False, True, r))
#           print(r)
        for r in cur_loc_ranges:
            points.append(Point(r.range_start, True, False, r))
            points.append(Point(r.range_start + r.length, False, False, r))
#           print(r)

        points.sort()

        new_loc_ranges: typing.List[LocRange] = []
        remap_delta = 0
        cur_loc_range: typing.Optional[LocRange] = None
        cur_range_start = 0

        for point in points:
#           print(point)
            if point.is_map:
                # Beginning or end of a map range: the remap delta will change here
                # The new location range may need to be split or deleted
                if cur_loc_range is not None:
                    if point.location != cur_range_start:
                        # Split the input range here
                        new_loc_ranges[-1].length = point.location - cur_range_start
                        assert new_loc_ranges[-1].length >= 1, new_loc_ranges[-1].length
#                       print("Split - range out:", new_loc_ranges[-1])
                    else:
                        # Empty range created - no split
                        new_loc_ranges.pop()

                # Update the remap delta
                if point.is_start:
                    assert remap_delta == 0
                    map_range = typing.cast(MapRange, point.link)
                    remap_delta = map_range.dest_range_start - map_range.range_start
                else:
                    remap_delta = 0

                # The new location range may need to be recreated
                if cur_loc_range is not None:
                    cur_range_start = point.location
                    new_loc_ranges.append(LocRange(point.location + remap_delta, 0))

#               print("New remap delta", remap_delta)
                
            else:
                # Beginning or end of a location range
                if point.is_start:
                    assert cur_loc_range is None
                    new_loc_ranges.append(LocRange(point.location + remap_delta, 0))
                    cur_loc_range = typing.cast(LocRange, point.link)
                    cur_range_start = point.location
#                   print("Start - range in:", cur_loc_range)
                else:
                    assert cur_loc_range is not None
                    if point.location != cur_range_start:
                        # Range is not empty - set the length
                        new_loc_ranges[-1].length = point.location - cur_range_start
#                       print("End - range out:", new_loc_ranges[-1], point)
                        assert new_loc_ranges[-1].length >= 1
                    else:
                        # Empty range created - remove
                        new_loc_ranges.pop()
                    cur_loc_range = None

#       print("OUT")
#       for r in new_loc_ranges:
#           print(r)

        assert remap_delta == 0
        assert cur_loc_range is None
        check_ranges(new_loc_ranges)
        return new_loc_ranges

def part(part: int, fname: str) -> int:
    seeds = []
    maps = []

    for line in open(fname, "rt"):
        fields = line.split()
        if (len(fields) > 1) and (fields[0] == "seeds:"):
            if part == 1:
                seeds = [LocRange(int(x), 1) for x in fields[1:]]
            else:
                seeds = [LocRange(int(fields[i]), int(fields[i + 1]))
                        for i in range(1, len(fields), 2)]

        elif (len(fields) == 2) and (fields[1] == "map:"):
            maps.append(Map())

        elif len(fields) == 3:
            (dest_range_start, src_range_start, length) = [
                    int(x) for x in fields]
            maps[-1].add(MapRange(src_range_start, dest_range_start, length))

        else:
            assert len(fields) == 0

    min_loc = sys.maxsize
    for seed in seeds:
        loc_ranges = [seed]
        for m in maps:
#           print(loc_ranges)
            loc_ranges = m.remap(loc_ranges)
#       print(loc_ranges)
#       print("")

        for loc_range in loc_ranges:
            min_loc = min(loc_range.range_start, min_loc)

    return min_loc

def main():
    assert part(1, "test") == 35
    assert part(1, "input") == 579439039
    print(part(1, "input"))
    assert part(2, "test") == 46
    print(part(2, "input"))

if __name__ == "__main__":
    main()
