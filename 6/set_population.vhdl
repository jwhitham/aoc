library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity set_population is
    generic (NUMBER_OF_QUESTIONS    : Integer;
             COUNT_WIDTH            : Integer);
    port (input_question            : in std_logic_vector (1 to NUMBER_OF_QUESTIONS);
          output_value              : out unsigned (COUNT_WIDTH - 1 downto 0));
end set_population;

architecture behaviour of set_population is

    constant LEFT_QUESTIONS : Integer := NUMBER_OF_QUESTIONS / 2;
    signal left_value       : unsigned (COUNT_WIDTH - 1 downto 0);
    signal right_value      : unsigned (COUNT_WIDTH - 1 downto 0);

begin
    base : if NUMBER_OF_QUESTIONS = 1 generate
        output_value (0) <= input_question (1);
        output_value (COUNT_WIDTH - 1 downto 1) <= (others => '0');
    end generate;

    inductive : if NUMBER_OF_QUESTIONS > 1 generate
        left : entity set_population
            generic map (NUMBER_OF_QUESTIONS => LEFT_QUESTIONS,
                         COUNT_WIDTH => COUNT_WIDTH)
            port map (input_question => input_question (1 to LEFT_QUESTIONS),
                      output_value => left_value);
        right : entity set_population
            generic map (NUMBER_OF_QUESTIONS => NUMBER_OF_QUESTIONS - LEFT_QUESTIONS,
                         COUNT_WIDTH => COUNT_WIDTH)
            port map (input_question => input_question (LEFT_QUESTIONS + 1 to NUMBER_OF_QUESTIONS),
                      output_value => right_value);
        output_value <= left_value + right_value;
    end generate;
end behaviour;
