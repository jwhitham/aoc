library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;

entity question_counter_part_2 is
    generic (NUMBER_OF_QUESTIONS    : Integer;
             COUNT_WIDTH            : Integer);
    port (input_question            : in std_logic_vector (1 to NUMBER_OF_QUESTIONS);
          end_of_line               : in std_logic;
          end_of_group              : in std_logic;
          output_value              : out unsigned (COUNT_WIDTH - 1 downto 0); 
          clock                     : in std_logic;
          reset                     : in std_logic);
end question_counter_part_2;

architecture behaviour of question_counter_part_2 is
    signal total_for_file   : unsigned (COUNT_WIDTH - 1 downto 0);
    signal total_for_group  : unsigned (COUNT_WIDTH - 1 downto 0);
    signal intersection_for_group : std_logic_vector (1 to NUMBER_OF_QUESTIONS);
    signal intersection_valid     : std_logic;

    component set_population is
        generic (NUMBER_OF_QUESTIONS    : Integer;
                 COUNT_WIDTH            : Integer);
        port (input_question            : in std_logic_vector (1 to NUMBER_OF_QUESTIONS);
              output_value              : out unsigned (COUNT_WIDTH - 1 downto 0));
    end component set_population;

begin

    output_value <= total_for_file;
    
    pop : set_population
        generic map (NUMBER_OF_QUESTIONS => NUMBER_OF_QUESTIONS,
                     COUNT_WIDTH => COUNT_WIDTH)
        port map (input_question => intersection_for_group,
                  output_value => total_for_group);

    process (clock) is
    begin
        if clock = '1' and clock'event then
            if reset = '1' then
                total_for_file <= (others => '0');
                intersection_for_group <= (others => '1');
                intersection_valid <= '0';
            else
                if end_of_group = '1' then
                    if intersection_valid = '1' then
                        total_for_file <= total_for_file + total_for_group;
                    end if;
                    intersection_for_group <= (others => '1');
                    intersection_valid <= '0';
                elsif end_of_line = '1' then
                    intersection_for_group <= intersection_for_group and input_question;
                    intersection_valid <= '1';
                end if;
            end if;
        end if;
    end process;
end behaviour;
