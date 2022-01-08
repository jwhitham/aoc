
int getNumberForIndex(int[] startingNumbers, int requestedIndex) {

    if (requestedIndex <= startingNumbers.length) {
        return startingNumbers[requestedIndex - 1];
    }

    def seenAtIndex = [:]

    for (i in 0 .. startingNumbers.length - 1) {
        seenAtIndex[startingNumbers[i]] = i
    }

    int lastItem = startingNumbers[startingNumbers.length - 1]

    for (int currentIndex in startingNumbers.length .. requestedIndex - 1) {
        int previousLastItem = lastItem

        if (seenAtIndex.containsKey(lastItem)) {
            lastItem = currentIndex - seenAtIndex[lastItem] - 1
        } else {
            lastItem = 0
        }

        seenAtIndex[previousLastItem] = currentIndex - 1
        currentIndex ++
    }
    return lastItem
}

int[] test_input = [0, 3, 6];
assert getNumberForIndex(test_input, 1) == 0
assert getNumberForIndex(test_input, 2) == 3
assert getNumberForIndex(test_input, 3) == 6
assert getNumberForIndex(test_input, 4) == 0
assert getNumberForIndex(test_input, 5) == 3
assert getNumberForIndex(test_input, 6) == 3
assert getNumberForIndex(test_input, 7) == 1
assert getNumberForIndex(test_input, 8) == 0
assert getNumberForIndex(test_input, 9) == 4
assert getNumberForIndex(test_input, 10) == 0
assert getNumberForIndex(test_input, 2020) == 436

int[] real_input = [6,19,0,5,7,13,1];

println("part 1 result is " + getNumberForIndex(real_input, 2020));
println("part 2 result is " + getNumberForIndex(real_input, 30000000));

