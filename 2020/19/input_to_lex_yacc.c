
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

static const char* separator = "\n%%\n";

int main(int argc, char ** argv)
{
    FILE*   input_fd;
    FILE*   lex_fd;
    FILE*   yacc_fd;
    char    line[BUFSIZ + 1];

    if (argc != 2) {
        fputs("specify the input file name\n", stderr);
        return 1;
    }
    input_fd = fopen(argv[1], "rt");
    if (!input_fd) {
        perror("input error");
        return 1;
    }

    lex_fd = fopen("lex.l", "wt");
    if (!lex_fd) {
        perror("lex output error");
        return 1;
    }
    yacc_fd = fopen("yacc.y", "wt");
    if (!yacc_fd) {
        perror("yacc output error");
        return 1;
    }

    fputs("%{\n"
          "#include \"yacc.tab.h\"\n"
          "extern int read_input(char* buffer, int* bytes_read, int max_bytes);\n"
          "#define YY_NO_INPUT\n"
          "#define YY_NO_UNPUT\n"
          "#undef YY_INPUT\n"
          "#define YY_INPUT(b,r,s) read_input(b,&r,s)\n"
          "%}\n\n", lex_fd);
    fputs(separator, lex_fd);
    fputs("%{\n"
          "#include <stdio.h>\n"
          "extern void yyerror(const char *s);\n"
          "int yywrap();\n"
          "extern int yylex();\n"
          "extern int read_input(char* buffer, int* bytes_read, int max_bytes);\n"
          "%}\n"
          "%glr-parser\n\n", yacc_fd);
    fputs(separator, yacc_fd);
    fputs("root : N0\n", yacc_fd);


    while (fgets(line, BUFSIZ, input_fd)) {
        char* scan = line;
        long int value;
        char* quote;
        char* endptr = NULL;

        value = strtol(scan, &endptr, 10);
        if (endptr == scan) {
            continue;
        }

        scan = endptr + 1;
        quote = strchr(scan, '"');
        fprintf(yacc_fd, "N%d : ", (int) value);

        if (quote) {
            // terminal rule
            fprintf(lex_fd, "%c { return '%c'; }\n", quote[1], quote[1]);
            fprintf(yacc_fd, "'%c';\n", quote[1]);
        } else {
            // non-terminal rule
            while (scan) {
                char* next = NULL;
                char* stop = strchr(scan, '|');
                if (stop) {
                    stop[0] = '\0';
                    next = stop + 1;
                } else {
                    next = NULL;
                }
                value = strtol(scan, &endptr, 10);
                while (endptr != scan) {
                    scan = endptr + 1;
                    fprintf(yacc_fd, " N%d", (int) value);
                    value = strtol(scan, &endptr, 10);
                }
                scan = next;
                if (scan) {
                    fprintf(yacc_fd, " |");
                } else {
                    fprintf(yacc_fd, ";\n");
                }
            }
        }
    }
    fputs(separator, lex_fd);
    fputs(separator, yacc_fd);

    fclose(lex_fd);
    fclose(yacc_fd);
    fclose(input_fd);
    return 0;
}

