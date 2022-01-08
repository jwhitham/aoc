import Data.List as List

-- problem inputs
example_input_1 = [16,10,15,5,1,11,7,19,6,12,4] :: [Int]
example_input_2 = [28,33,18,42,31,14,46,20,48,47,24,23,49,45,19,38,39,
                   11,1,32,25,35,8,17,7,9,4,2,34,10,3] :: [Int]
input = [115,134,121,184,78,84,77,159,133,90,71,185,152,165,39,64,85,
         50,20,75,2,120,137,164,101,56,153,63,70,10,72,37,
         86,27,166,186,154,131,1,122,95,14,119,3,99,172,111,
         142,26,82,8,31,53,28,139,110,138,175,108,145,58,76,
         7,23,83,49,132,57,40,48,102,11,105,146,149,66,38,155,
         109,128,181,43,44,94,4,169,89,96,60,69,9,163,116,45,
         59,15,178,34,114,17,16,79,91,100,162,125,156,65] :: [Int]
max_difference = 3

-- a prepared input begins with the starting point from the socket (0 jolts)
-- and ends with the maximum joltage expected by the device (max input + max_difference)
prepare input = List.sort ([0, max_difference + maximum input] ++ input)

-- this is True if a joltage difference is permitted
can_reach a b = ((a + 1) <= b) && (b <= (a + max_difference))

-- used in an intermediate data structure (the Way list)
-- represents the number of ways to reach n jolts
data Way = Way Int Int
instance Show Way where
    show (Way n_ways n) = "{" ++ (show n) ++ " reached " ++ (show n_ways) ++ " ways}"
no_way = (Way 0 0)

-- access an item in the Way list. If depth_n = 1, get the first item.
-- If the item doesn't exist, the answer is no_way.
ways_already_computed :: Int -> [Way] -> Way
ways_already_computed depth_n more =
        (let initial_n = (take (depth_n) more) in
            (if ((length initial_n) == (depth_n))
             then (head (drop (depth_n - 1) initial_n))
             else no_way))

-- count all of the possible ways to go from joltage a to some higher joltage
ways_already_computed_if_reachable :: Int -> Int -> [Way] -> Int
ways_already_computed_if_reachable _ 0 _ = 0
ways_already_computed_if_reachable a depth_n more =
        (let (Way n_ways n) = (ways_already_computed depth_n more) in
            (if (can_reach a n) then n_ways else 0) + 
            (ways_already_computed_if_reachable a (depth_n - 1) more))

-- generate the Way list
ways_to_reach :: [Int] -> [Way]
ways_to_reach [a] = [Way 1 a]
ways_to_reach (a : rest) =
        (let more = (ways_to_reach rest) in
            (let a_ways = (ways_already_computed_if_reachable a max_difference more) in
                ((Way a_ways a) : more)))

-- count up the number of ways to go from 0 jolts to the maximum joltage
-- using the way list
count_arrangements input = 
        (let (Way a_ways _) = (head (ways_to_reach (prepare input))) in a_ways)

-- test against examples
test = (((count_arrangements example_input_1) == 8)
        && ((count_arrangements example_input_2) == 19208))

-- solve the problem
main = (if test then print(count_arrangements input)
        else print("Error"))
