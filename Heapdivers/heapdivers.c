// gcc heapdivers.c -o heapdivers -no-pie

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define FLAG_BUFFER 200

void plant_the_flag();
void puts_menu();
void input_case();

typedef struct {
    uintptr_t (*stratagem)();
    char *helldivers_name;
} action;

char choice = '\0';
action *helldivers;

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);

    helldivers = (action*)malloc(sizeof(helldivers)); 
    puts_menu();
    input_case();
}

void plant_the_flag()
{
    char buf[FLAG_BUFFER];
    FILE *f = fopen("flag.txt", "r");
    fgets(buf, FLAG_BUFFER, f);
    fprintf(stdout, "%s\n", buf);
    fflush(stdout);
}

void puts_menu()
{
    puts("Welcome helldivers");
    puts("FOR DEMOCRACY !!");
    puts("Select your stratagem");
    puts("---------------------");
    puts("(E)agle 500kg Bomb");
    puts("(O)rbital Railcannon Strike");
    puts("(A)/AC-8 Autocannon Sentry");
    puts("(S)uper Earth Flag");
    puts("(L)AS-99 Quasar Cannon");
    puts("(F)lee");
}

void input_case()
{
    scanf("%c", &choice);

    if (!isupper(choice)) {
        choice = toupper(choice); 
    }

    switch (choice) {
        case 'E':
            break;

        case 'O':
            break;

        case 'A':
            break;
        
        case 'S':
            break;

        case 'L':
            break;

        case 'F':
            exit(0);

        default:
            puts("[Error] You can't choose another stratagem !");
            exit(1);
    }
}

