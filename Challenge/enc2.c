 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

void swap (uint8_t **a, uint8_t **b)
{
    uint8_t *temp = *a;
    *a = *b;
    *b = temp;
}
 
// A utility function to print an array
void printArray (uint8_t *arr[], unsigned long n)
{
    printf("{ ");
    for (unsigned long i = 0; i < n; i++){
        printf("\"\\x%02X", arr[i][0]);
        for (unsigned long k = 0; k < arr[i][0]; k++)
        {
            printf("\\x%02X", arr[i][k+1]);
        }
        printf("\", ");
    }
    printf("}\n");
}
 
void randomize (uint8_t * arr[], unsigned long n)
{
    
    for (unsigned long i = n-1; i > 0; i--)
    {
        unsigned long j = rand() % (i+1);
        swap(&arr[i], &arr[j]);
    }
}

void encrypt(uint8_t * arr[], unsigned long n, int seed){
    srand(1203);
    randomize(arr,n);
}
uint8_t *t[] 
int main(int argc, char **argv)
{
    unsigned long a = atoi(argv[1]);
    unsigned long n = sizeof(t)/ sizeof(t[0]);
    encrypt(t, n, a);
    printArray(t, n);
}

