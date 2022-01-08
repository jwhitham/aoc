
.text
.global _main
_main:

    movl    $0, output_counter

read_next_line:
/* read input */
    pushl   $text_buffer
    pushl   $character
    pushl   $second_index
    pushl   $first_index
    pushl   $input_format
    call    _scanf
    add     $20, %esp

/* detect errors and end of file */
    cmp     $0, %eax
    jle     end_of_file

    cmp     $4, %eax
    jne     input_error

/* process the input */
    mov     character, %bl
    mov     $0, %ecx
    
    mov     $text_buffer, %esi
    add     (first_index), %esi
    cmp     -1(%esi), %bl
    jne     check_second_index

/* seen at first index */
    incl    %ecx

check_second_index:
    mov     $text_buffer, %esi
    add     (second_index), %esi
    cmp     -1(%esi), %bl
    jne     compare_to_minimum_and_maximum

/* seen at second index */
    incl    %ecx

compare_to_minimum_and_maximum:
    cmp     $1, %ecx
    jne     reject

/* Accept */
    incl    output_counter
    jmp     read_next_line

reject:
    jmp     read_next_line

end_of_file:
    pushl   output_counter
    pushl   $output_format
    call    _printf
    add     $8, %esp

    pushl   $0
    call    _exit

input_error:
    pushl   %eax
    pushl   $error_format
    call    _printf
    add     $8, %esp

    pushl   $1
    call    _exit

.data
first_index:
    .long   0
second_index:
    .long   0
character:
    .long   0
text_buffer:
    .space  256
output_counter:
    .long   0

input_format:
    .ascii "%u-%u %c: %s\0"
output_format:
    .ascii "number %d\n\0"
error_format:
    .ascii "Input format error: %d\n\0"

