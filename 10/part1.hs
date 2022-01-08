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

count_gaps [] _ = 0
count_gaps [_] _ = 0
count_gaps (smaller : larger : rest) gap_size = 
            ((if (larger - smaller) == gap_size then 1 else 0) +
             (count_gaps (larger : rest) gap_size))

count_1_gaps input = count_gaps (prepare input) 1
count_3_gaps input = count_gaps (prepare input) 3

test = (((count_1_gaps example_input_1) == 7)
        && ((count_3_gaps example_input_1) == 5)
        && ((count_1_gaps example_input_2) == 22)
        && ((count_3_gaps example_input_2) == 10))

main = (if test then print((count_1_gaps input) * (count_3_gaps input))
        else print("Error"))
