#include <stdio.h>
#include <stdint.h>
#include <string.h>
uint64_t challenge(uint64_t input);

uint64_t validtable[32] = {0xc9c30458ae310b48, 0x3a156b4cd400205b};
int main(int argc, char **argv){
    uint8_t valid = 0;
    char buffer[32] = {0};
    // fgets(buffer, 32, stdin);
    
    for (uint8_t i = 0; i < 0xff; i++)
    {
        printf("%X: %lX\n", i, challenge(i));
        
    }
    printf("%X: %lX\n", 0xff, challenge(0xff));
                      
    // if(challenge('M')==0xf3d66f147a312b13){
    //     printf("Congrats");
    // }
    // else{
    //     printf("Nope...");
    // }
    return 1;
    // char key[] = "MIDNIGHT{COUCOULESBOSS}";
    // uint64_t t = 0;
    // for (size_t i = 0; i < strlen(key); i++)
    // {
    //     for (size_t k = 1; k < 9; k++)
    //     {
    //         t |= (uint64_t)key[i]<<8*k;
    //         // printf("%lX\n", t);
    //     }
        
    //     printf("%c: %lX\n", key[i], challenge(key[i]));
    //     t = 0;
    // }
    // return 1;
}