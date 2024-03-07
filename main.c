#include <stdio.h>
#include <stdint.h>
#include <string.h>
uint64_t challenge(uint64_t input);

int main(){
    char key[] = "MIDNIGHT{COUCOULESBOSS}";
    uint64_t t = 0;
    for (size_t i = 0; i < strlen(key); i++)
    {
        for (size_t k = 1; k < 9; k++)
        {
            t |= (uint64_t)key[i]<<8*k;
            // printf("%lX\n", t);
        }
        
        printf("%c: %lX\n", key[i], challenge(t));
        t = 0;
    }
    return 1;
}