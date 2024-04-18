 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <openssl/aes.h>
#include <openssl/rc4.h>
#include <sys/mman.h>
#include <unistd.h>

uint8_t mysuperkey[16] = "\xe1\xa4\x64\x6e\xe8\xac\xd2\x0f\x45\x78\xdb\xea\x4a\x79\x38\x0a";


void swap (int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

uint8_t * ConvertArray2BytesString(uint8_t **arr){
    uint64_t n = 0;
    uint8_t **saveptr = arr;
    while (*arr++ != 0){n++;}
    arr = saveptr;
    uint8_t *final = calloc(n, 1);
    uint8_t size = 0;
    size_t index = 0;
    RC4_KEY key = {0};
    
    for (size_t i = 0; i < n; i++)
    {
        size = arr[i][0];
    	RC4_set_key(&key, 16, mysuperkey);
   	RC4(&key, size, arr[i]+1, arr[i]+1);
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

uint8_t *shuffled_arr[] = {"\x10\x43\x71\x30\xe0\x6d\xf4\x19\x05\x09\x85\x58\xf4\xea\xc6\xca\xaa", "\x07\x41\x73\x32\xe2\x6f\xf6\x1b"};

uint8_t **load_memory(){
	unsigned long n = 0;
	unsigned short taille = 0;
	n = sizeof(shuffled_arr)/ sizeof(shuffled_arr[0]);
    	
	uint8_t **arr = calloc(n,sizeof(void *));

	for(unsigned int i=0; i<n; i++){
		taille = shuffled_arr[i][0]+1;
		arr[i] = malloc(taille);
		memcpy(arr[i], shuffled_arr[i], taille);
	}
	return arr;
}

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


    arr = load_memory();
    arr = decrypt(arr,n);
    code = ConvertArray2BytesString(arr); 
    
    printf("::: %s\n", code);
    return 0;
}
