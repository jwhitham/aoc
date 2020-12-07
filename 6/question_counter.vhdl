library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity question_counter is
    generic (NUMBER_OF_QUESTIONS    : Integer;
             COUNT_WIDTH            : Integer);
    port (input_question            : in std_logic_vector (1 to NUMBER_OF_QUESTIONS);
          input_valid               : in std_logic;
          output_value              : out unsigned (COUNT_WIDTH - 1 downto 0); 
          clock                     : in std_logic;
          reset                     : in std_logic);
end question_counter;

architecture behaviour of question_counter is
    signal counter          : unsigned (COUNT_WIDTH - 1 downto 0);
    signal new_value        : unsigned (COUNT_WIDTH - 1 downto 0);

    component set_population is
        generic (NUMBER_OF_QUESTIONS    : Integer;
                 COUNT_WIDTH            : Integer);
        port (input_question            : in std_logic_vector (1 to NUMBER_OF_QUESTIONS);
              output_value              : out unsigned (COUNT_WIDTH - 1 downto 0));
    end component set_population;

begin

    output_value <= counter;
    
    pop : set_population
        generic map (NUMBER_OF_QUESTIONS => NUMBER_OF_QUESTIONS,
                     COUNT_WIDTH => COUNT_WIDTH)
        port map (input_question => input_question,
                  output_value => new_value);

    process (clock) is
    begin
        if clock = '1' and clock'event then
            if reset = '1' then
                counter <= (others => '0');
            elsif input_valid = '1' then
                counter <= counter + new_value;
            end if;
        end if;
    end process;
end behaviour;
