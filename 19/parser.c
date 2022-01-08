
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

static int error_flag = 0;
static char line[BUFSIZ + 1];
static char* read_ptr;

extern int yyparse();

int read_input(char* buffer, int* bytes_read, int max_bytes)
{
    *bytes_read = 0;
    if (max_bytes > 0) {
        if (read_ptr[0] != '\0') {
            buffer[0] = *read_ptr;
            read_ptr++;
            *bytes_read = 1;
        }
    }
    return 0;
}

void yyerror (const char *s) {
    error_flag = 1;
}

int yywrap() {
    return -1;
}

int main(int argc, char ** argv)
{
    FILE*   input_fd;
    int     count = 0;

    if (argc != 2) {
        fputs("specify the input file name\n", stderr);
        return 1;
    }
    input_fd = fopen(argv[1], "rt");
    if (!input_fd) {
        perror("input error");
        return 1;
    }

    while (fgets(line, BUFSIZ, input_fd)) {
        int only_whitespace = 1;
        int contains_colon = 0;
        int i;

        // ignore lines containing only whitespace
        // or containing ':'
        for (i = 0; line[i] != '\0'; i++) {
            if (!isspace(line[i])) {
                only_whitespace = 0;
            }
            if (line[i] == ':') {
                contains_colon = 1;
            }
        }
        if (only_whitespace || contains_colon) {
            continue;
        }
        // valid line for matching
        read_ptr = line;
        error_flag = 0;
        yyparse();

        if (error_flag) {
            printf("invalid: %s", line);
        } else {
            printf("ok: %s", line);
            count++;
        }
    }
    fclose(input_fd);
    printf("result is %d\n", count);
    return 0;
}

