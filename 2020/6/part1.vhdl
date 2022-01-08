use std.textio.all;

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity part1 is
end part1;

architecture behaviour of part1 is
    constant NUMBER_OF_QUESTIONS    : Integer := 26;
    constant COUNT_WIDTH            : Integer := 16;
    signal input_question           : std_logic_vector (1 to NUMBER_OF_QUESTIONS);
    signal end_of_line              : std_logic;
    signal end_of_group             : std_logic;
    signal output_value             : unsigned (COUNT_WIDTH - 1 downto 0); 
    signal clock                    : std_logic;
    signal reset                    : std_logic;

    component question_counter is
        generic (NUMBER_OF_QUESTIONS    : Integer;
                 COUNT_WIDTH            : Integer);
        port (input_question            : in std_logic_vector (1 to NUMBER_OF_QUESTIONS);
              end_of_line               : in std_logic;
              end_of_group              : in std_logic;
              output_value              : out unsigned (COUNT_WIDTH - 1 downto 0); 
              clock                     : in std_logic;
              reset                     : in std_logic);
    end component question_counter;
     
begin
    qc : question_counter
        generic map (NUMBER_OF_QUESTIONS => NUMBER_OF_QUESTIONS,
                     COUNT_WIDTH => COUNT_WIDTH)
        port map (input_question => input_question,
                  end_of_line => end_of_line,
                  end_of_group => end_of_group,
                  output_value => output_value,
                  clock => clock, reset => reset);

    process
        variable input_line  : Line;
        variable output_line : Line;
        variable v           : Integer;
        file input_file      : Text is in "input";
    begin
        reset <= '1';
        clock <= '1';
        end_of_group <= '0';
        end_of_line <= '0';
        input_question <= (others => '0');
        wait for 10 ns;

        reset <= '0';
        clock <= '0';
        wait for 10 ns;

        while not endfile (input_file) loop
            readline (input_file, input_line);

            -- format the data as a 26-bit input
            input_question <= (others => '0');
            for i in input_line'Range loop
                v := Character'Pos (input_line (i));
                v := v + 1 - Character'Pos ('a');
                if v >= 1 and v <= NUMBER_OF_QUESTIONS then
                    input_question (v) <= '1';
                end if;
            end loop;

            end_of_group <= '0';
            end_of_line <= '0';

            if input_line'Length = 0 then
                -- reached the end of a group
                end_of_group <= '1';
            else
                end_of_line <= '1';
            end if;

            clock <= '1';
            wait for 10 ns;
            clock <= '0';
            wait for 10 ns;
        end loop;

        -- reached the end of the final group
        input_question <= (others => '0');
        end_of_group <= '1';
        end_of_line <= '0';

        clock <= '1';
        wait for 10 ns;
        clock <= '0';
        wait for 10 ns;

        -- obtain output
        write (output_line, to_integer (output_value));
        writeline (output, output_line);
        wait;
    end process;
end behaviour;
