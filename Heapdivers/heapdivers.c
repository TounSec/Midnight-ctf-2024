// gcc heapdivers.c -o heapdivers -no-pie -fstack-protector-all

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <unistd.h>

#define FLAG_BUFFER 200

typedef struct {
    uintptr_t (*stratagem)();
    char *helldivers_name;
} action;

char choice = '\0';
action *helldivers;

void plant_the_flag();
void puts_menu();
void input_case();
void call_stragem(action *call);
char *information_reception();
void eagle();
void orbital();
void extraction();
void earth();
void quasar();

int main()
{
    setvbuf(stdout, NULL, _IONBF, 0);
    helldivers = (action*)malloc(sizeof(helldivers));

    puts_menu();
    input_case();
    call_stragem(helldivers);

    return 0;
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
    puts("[E]agle 500kg Bomb");
    puts("[O]rbital Railcannon Strike");
    puts("E[x]traction");
    puts("[S]uper Earth Flag");
    puts("[L]AS-99 Quasar Cannon");
    puts("[F]lee");
}

void input_case()
{
    scanf(" %c", &choice);

    if (!isupper(choice)) {
        choice = toupper(choice); 
    }

    switch (choice) {
        case 'E':
            helldivers->stratagem = (void*)eagle;
            puts("Wait helldivers, we need to confirm your identity !");
            puts("Please announce your code name");
            helldivers->helldivers_name = information_reception(); 
            break;

        case 'O':
            helldivers->stratagem = (void*)orbital;
            break;

        case 'X':
            helldivers->stratagem = (void*)extraction;
            break;
        
        case 'S':
            break;

        case 'L':
            quasar();
            break;

        case 'F':
            exit(0);

        default:
            puts("[Error] You can't choose another stratagem !");
            exit(1);
    }
}

void call_stragem(action *call)
{
    (*call->stratagem)();
}

char *information_reception()
{
    char *line = malloc(100);
    size_t max = 100, len = 0;
    int c;

    if (line == NULL) {
        return NULL;
    }

    while ((c = fgetc(stdin)) != EOF) {
        if (len+1 >= max) {
            max *= 2;

            char *linen = realloc(line, max);
            if (linen == NULL) {
                free(line);
                return NULL;
            }
            line = linen;
        }
        line[len++] = c;
        if (c == '\n') {
            break;
        }
    }
    line[len] = '\0';
    return line;
}

void eagle()
{
    puts("(E)agle 500kg Bomb is coming. Step aside !");
}

void orbital()
{
    puts("Okay helldivers, we sent a Orbital Railcannon Strike. Take care");
}

void extraction()
{
    char authorisation = '\0';

    puts("Do you really want to extract helldivers ?[Y/N]"); 
    scanf(" %c", &authorisation);

    if (toupper(authorisation) == 'Y') {
        puts("The Falcon is coming to extract you !");
        free(helldivers);

    } else {
        puts("Heard helldivers, continue the mission");
    }
}

void earth()
{

}

void quasar()
{
    char *last_world = (char*)malloc(8);

    puts("You overloaded your cannon, its going to explode. Flee !!!");
    puts("A world for the end ?");
    read(0, last_world, 8);
}
