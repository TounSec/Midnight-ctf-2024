 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <openssl/aes.h>
#include <openssl/rc4.h>
#include <sys/mman.h>
#include <unistd.h>

uint8_t mysuperkey[16] = "\xe1\xa4\x64\x6e\xe8\xac\xd2\x0f\x45\x78\xdb\xea\x4a\x79\x38\x0a";

uint8_t dechiffre_RC4(uint8_t *dat, uint8_t sz){
    RC4_KEY key;
    RC4_set_key(&key, 16, mysuperkey);
    uint8_t *r = malloc(sz);
    if(r == NULL){
        return -1;
    }
    RC4(&key, sz, dat, r);
    long pagesize = sysconf(_SC_PAGESIZE);
    uintptr_t start = (uintptr_t)dat;
    uintptr_t pagestart = start & -pagesize;
    size_t padding = start - pagestart;
    if (mprotect((void*)pagestart, sz + padding, PROT_READ | PROT_WRITE) == -1) {free(r);return -1;}
    memcpy(dat, r, sz);
    if(mprotect((void*)pagestart, sz + padding, PROT_READ)==-1){
        return -1;
    }
    free(r);
    return 0;
}   
void swap (int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

uint8_t * ConvertArray2BytesString(uint8_t *arr[16]){
    uint64_t n = 0;
    uint8_t **saveptr = arr;
    while (*arr++ != 0){n++;}
    arr = saveptr;
    uint8_t *final = calloc(n, 1);
    uint8_t size = 0;
    size_t index = 0;
    for (size_t i = 0; i < n; i++)
    {
        size = arr[i][0];
        final = realloc(final,index+size );
        if(dechiffre_RC4(arr[i]+1, size) == -1){
            exit(1);
        }
        for (size_t k = 0; k < size; k++)
        {
            final[index] = arr[i][k+1];
            index++;
        }
    }
    return final;
    
}

void randomize ( int arr[], int n)
{
    
    for (int i = n-1; i > 0; i--)
    {
        int j = rand() % (i+1);
        swap(&arr[i], &arr[j]);
    }
}

uint8_t ** decrypt(uint8_t *arr[], int n){
    int *r = malloc(n*sizeof(int));
    for (size_t i = 0; i < n; i++)
    {
        r[i] = i;
    }
    uint8_t **a = calloc(n,sizeof(arr[0]));
    randomize(r,n);
    for (size_t i = 0; i < n; i++)
    {
        a[r[i]] = arr[i];
    }
    return a;
}

uint8_t *shuffled_arr[] = {"\x09\x41\x41\x41\x41\x41\x41\x41\x42\x42\x41\x41\x41\x41\xff","BBBBBBBBBBBBBBBB","\x09\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43\x43", "DDDDDDDDDDDDDDDD", "EEEEEEEEEEEEEEEE", "FFFFFFFFFFFFFFFF"};


int main(int argc, char **argv)
{    

    int n = 0;
    uint8_t **arr = NULL;
    uint8_t *code = NULL;
    if(argc != 2){
        printf("Usage: ./%s <pin>\n", argv[0]);
        exit(1);
    }
    srand(atoi(argv[1]));

    n = sizeof(shuffled_arr)/ sizeof(shuffled_arr[0]);

    arr = calloc(n,sizeof(shuffled_arr[0]));
    arr = decrypt(shuffled_arr,n);
    code = ConvertArray2BytesString(arr);

    return 0;
}