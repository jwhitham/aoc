
with Ada.Text_IO;

procedure part1 is

    type t_key is new Long_Long_Integer;
    type t_loop_size is new Natural;

    subject : constant t_key := 7;
    modulus : constant t_key := 20201227;

    function get_loop_size (public : t_key) return t_loop_size is
        value       : t_key := 1;
        loop_size   : t_loop_size := 1;
    begin
        loop
            value := value * subject;
            value := value rem modulus;
            exit when value = public;
            loop_size := loop_size + 1;
        end loop;
        return loop_size;
    end get_loop_size;

    function get_encryption_key (public : t_key;
                                 size : t_loop_size) return t_key is
        value       : t_key := 1;
    begin
        for i in 1 .. size loop
            value := value * public;
            value := value rem modulus;
        end loop;
        return value;
    end get_encryption_key;


    key, pk1, pk2   : t_key;
    ls              : t_loop_size;
begin
    if (get_loop_size (17807724) /= 11) or else
        (get_loop_size (5764801) /= 8) or else
        (get_encryption_key (17807724, 8) /= 14897079) then
        Ada.Text_IO.Put_Line ("part 1 test failed");
    else
        pk1 := 18499292;
        pk2 := 8790390;
        ls := get_loop_size (pk1);
        key := get_encryption_key (pk2, ls);

        Ada.Text_IO.Put_Line ("part 1 result "
                              & t_key'Image (key));
    end if;
end part1;

