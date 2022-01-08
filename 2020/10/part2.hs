import Data.List as List

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

prepare input = List.sort ([0, 3 + maximum input] ++ input)

can_reach a b = ((a + 1) <= b) && (b <= (a + 3))

data Way = Way Int Int

ways_to_reach :: [Int] -> [Way]

ways_to_reach (a : b : c : d : rest) =
        (let ((Way b_ways _) : (Way c_ways _) : (Way d_ways _) : more) =
                ways_to_reach (b : c : d : rest) in
            (let a_ways = ((if (can_reach a b) then b_ways else 0) +
                     (if (can_reach a c) then c_ways else 0) +
                     (if (can_reach a d) then d_ways else 0)) in
                ((Way a_ways a) : (Way b_ways b) : (Way c_ways c) :
                            (Way d_ways d) : more)))
ways_to_reach [a, b, c] =
        (let ((Way b_ways _) : (Way c_ways _) : more) =
                ways_to_reach [b, c] in
            (let a_ways = ((if (can_reach a b) then b_ways else 0) +
                     (if (can_reach a c) then c_ways else 0)) in
                [Way a_ways a, Way b_ways b, Way c_ways c]))

ways_to_reach [a, b] =
        (let [(Way b_ways _)] = ways_to_reach [b] in
            (let a_ways = ((if (can_reach a b) then b_ways else 0)) in
                [Way a_ways a, Way b_ways b]))

ways_to_reach [a] = [Way 1 a]

count_arrangements input = 
        (let Way a_ways _ = (head (ways_to_reach (prepare input))) in
            a_ways)

test = (((count_arrangements example_input_1) == 8)
        && ((count_arrangements example_input_2) == 19208))

main = (if test then print(count_arrangements input)
        else print("Error"))
