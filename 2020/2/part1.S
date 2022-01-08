
.text
.global _main
_main:

    movl    $0, output_counter

read_next_line:
/* read input */
    pushl   $text_buffer
    pushl   $character
    pushl   $maximum
    pushl   $minimum
    pushl   $input_format
    call    _scanf
    add     $20, %esp

/* detect errors and end of file */
    cmp     $0, %eax
    jle     end_of_file

    cmp     $4, %eax
    jne     input_error

/* process the input */
    mov     $text_buffer, %esi
    mov     character, %bl
    mov     $0, %ecx

check_next_byte:
    mov     (%esi), %al
    inc     %esi

    cmp     $0, %al
    jz      compare_to_minimum_and_maximum

    cmp     %al, %bl
    jnz     check_next_byte
    
/* Found matching byte */
    inc     %ecx
    jmp     check_next_byte

compare_to_minimum_and_maximum:

	movl	maximum, %eax
	cmpl	%eax, %ecx
	jg      reject

	movl	minimum, %eax
	cmpl	%eax, %ecx
	jl      reject 

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
minimum:
    .long   0
maximum:
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

