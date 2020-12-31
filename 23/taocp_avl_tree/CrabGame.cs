using System;

// This version of Crab Game (AOC 2020 day 23) uses a list data structure
// based on a balanced tree. Each value can be found, added and removed in O(log N) time.
// This is not the best solution for the puzzle which can also be solved with a linked
// list: there is no need for the list index to be known at each iteration.


namespace aoc
{

    public class CrabGame
    {
        private taocp_avl_tree.AVLIntegerFindList all_cups;
        private int number_of_cups;

        public CrabGame(string initial_state, int number_of_cups)            
        {
            this.number_of_cups = number_of_cups;
            all_cups = new taocp_avl_tree.AVLIntegerFindList();
            for (int i = 0; i < initial_state.Length; i++)
            {
                all_cups.Insert(i, int.Parse(initial_state.Substring(i, 1)));
            }
            for (int i = initial_state.Length + 1; i <= number_of_cups; i++)
            {
                all_cups.Insert(i, i);
            }
        }

        public void Play(int number_of_rounds)
        {
            for (int i = 1; i <= number_of_rounds; i++)
            {
                int current_cup = all_cups.Value(0);

                // remove cups 1, 2, 3
                int cup1 = all_cups.Value(1);
                int cup2 = all_cups.Value(2);
                int cup3 = all_cups.Value(3);
                all_cups.Delete(1);
                all_cups.Delete(1);
                all_cups.Delete(1);

                // determine destination
                int destination_cup = current_cup - 1;
                while ((destination_cup == cup1) || (destination_cup == cup2)
                    || (destination_cup == cup3) || (destination_cup == 0))
                {
                    if (destination_cup == 0)
                    {
                        destination_cup = number_of_cups + 1;
                    }
                    destination_cup--;
                }

                // insert at destination
                int destination_index = all_cups.Index(destination_cup);
                destination_index = (destination_index + 1) % number_of_cups;
                all_cups.Insert(destination_index, cup3);
                all_cups.Insert(destination_index, cup2);
                all_cups.Insert(destination_index, cup1);

                // rotate so that the next cup is at index 0
                all_cups.Delete(0);
                all_cups.Insert(number_of_cups - 1, current_cup);
            }
        }

        public override string ToString()
        {
            string output = "";
            int current_cup = all_cups.Value(0);
            for (int i = 1; (i <= number_of_cups) && (i <= 10); i++)
            {
                int v = all_cups.Value(i - 1);
                if (v == current_cup)
                {
                    output += " (" + v + ")";
                }
                else
                {
                    output += " " + v;
                }
            }
            return output;
        }

        public string Part1Result()
        {
            int iter = all_cups.Index(1);
            string output = "";
            for (int i = 1; (i <= number_of_cups) && (i <= 8); i++)
            {
                iter = (iter + 1) % number_of_cups;
                output += all_cups.Value(iter).ToString();
            }
            return output;
        }

        public ulong Part2Result()
        {
            int iter = all_cups.Index(1);
            iter = (iter + 1) % number_of_cups;
            ulong r1 = (ulong)all_cups.Value(iter);
            iter = (iter + 1) % number_of_cups;
            ulong r2 = (ulong)all_cups.Value(iter);
            return r1 * r2;  // <-- that's numberwang
        }
    }

    public class CrabGameProgram
    {
        public static void CrabMain()
        {
            string test_input = "389125467";
            string my_input = "158937462";

            CrabGame cg = new CrabGame(test_input, 9);
            cg.Play(10);
            if (cg.Part1Result() != "92658374")
            {
                throw new Exception("test 1 failed");
            }
            cg.Play(90);
            if (cg.Part1Result() != "67384529")
            {
                throw new Exception("test 2 failed");
            }
            Console.WriteLine("part 1 tests ok");

            cg = new CrabGame(test_input, 1000 * 1000);
            cg.Play(10 * 1000 * 1000);
            if (cg.Part2Result() != 149245887792)
            {
                throw new Exception("test 3 failed");
            }
            Console.WriteLine("part 2 tests ok");

            cg = new CrabGame(my_input, 9);
            cg.Play(100);
            Console.WriteLine("part 1 result - " + cg.Part1Result());
            cg = new CrabGame(my_input, 1000000);
            cg.Play(10 * 1000 * 1000);
            Console.WriteLine("part 2 result - " + cg.Part2Result());
        }
    }
}
