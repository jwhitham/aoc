using System;

namespace aoc
{
    public class CrabGame
    {
        private class Cup
        {
            public uint previous = 0;
            public uint next = 0;
        }

        private Cup[] all_cups;
        private uint current_cup;
        private uint number_of_cups;

        public CrabGame(string initial_state, uint number_of_cups)            
        {
            this.number_of_cups = number_of_cups;
            all_cups = new Cup[number_of_cups + 1];
            for (uint i = 1; i <= number_of_cups; i++)
            {
                all_cups[i] = new Cup();
            }
            this.current_cup = uint.Parse(initial_state.Substring(0, 1));

            uint previous = this.current_cup;
            for (uint i = 0; i < (uint) initial_state.Length; i++)
            {
                uint current = uint.Parse(initial_state.Substring((int)i, 1));
                all_cups[current].previous = previous;
                all_cups[previous].next = current;
                previous = current;
            }
            for (uint current = (uint) initial_state.Length + 1; current <= number_of_cups; current++)
            {
                all_cups[current].previous = previous;
                all_cups[previous].next = current;
                previous = current;
            }
            // link around the end of the list
            all_cups[previous].next = this.current_cup;
            all_cups[this.current_cup].previous = previous;
        }

        private void Remove(uint cup)
        {
            uint previous = all_cups[cup].previous;
            uint next = all_cups[cup].next;
            all_cups[previous].next = next;
            all_cups[next].previous = previous;
            all_cups[cup].previous = 0;
            all_cups[cup].next = 0;
        }

        private void Insert(uint where, uint what)
        {
            uint next = all_cups[where].next;
            all_cups[where].next = what;
            all_cups[what].next = next;
            all_cups[next].previous = what;
            all_cups[what].previous = where;
        }

        public void Play(uint number_of_rounds)
        {
            for (uint i = 1; i <= number_of_rounds; i++)
            {
                uint cup1 = all_cups[current_cup].next;
                uint cup2 = all_cups[cup1].next;
                uint cup3 = all_cups[cup2].next;
                Remove(cup3);
                Remove(cup2);
                Remove(cup1);
                uint destination = current_cup - 1;
                while ((destination == cup1) || (destination == cup2)
                    || (destination == cup3) || (destination == 0))
                {
                    if (destination == 0)
                    {
                        destination = number_of_cups + 1;
                    }
                    destination--;
                }
                Insert(destination, cup3);
                Insert(destination, cup2);
                Insert(destination, cup1);
                // rotate the board
                current_cup = all_cups[current_cup].next;
            }
        }

        public override string ToString()
        {
            uint iter = current_cup;
            string output = "";
            for (uint i = 1; (i <= number_of_cups) && (i <= 10); i++)
            {
                output += " " + iter.ToString();
                iter = all_cups[iter].next;
                if (iter == current_cup)
                {
                    break;
                }
            }
            return output;
        }

        public string Part1Result()
        {
            uint iter = all_cups[1].next;
            string output = "";
            for (uint i = 1; (i <= number_of_cups) && (i <= 8); i++)
            {
                output += iter.ToString();
                iter = all_cups[iter].next;
            }
            return output;
        }

        public ulong Part2Result()
        {
            uint iter = all_cups[1].next;
            ulong r1 = (ulong)iter;
            iter = all_cups[iter].next;
            ulong r2 = (ulong)iter;
            return r1 * r2;  // <-- that's numberwang
        }
    }

    class Program
    {
        static void Main(string[] args)
        {
            string test_input = "389125467";
            string my_input = "158937462";

            TestAVL2.Test();
            TestAVL.Test();

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

            cg = new CrabGame(test_input, 1000 * 1000);
            cg.Play(10 * 1000 * 1000);
            if (cg.Part2Result() != 149245887792)
            {
                throw new Exception("test 3 failed");
            }

            cg = new CrabGame(my_input, 9);
            cg.Play(100);
            Console.WriteLine("part 1 result - " + cg.Part1Result());
            cg = new CrabGame(my_input, 1000000);
            cg.Play(10 * 1000 * 1000);
            Console.WriteLine("part 2 result - " + cg.Part2Result());
        }
    }
}
