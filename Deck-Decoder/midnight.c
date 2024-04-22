 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <openssl/aes.h>
#include <openssl/rc4.h>
#include <sys/mman.h>
#include <unistd.h>
#include <signal.h>
#include "midnight.h"

uint8_t mysuperkey[16] = "\xe1\xa4\x64\x6e\xe8\xac\xd2\x0f\x45\x78\xdb\xea\x4a\x79\x38\x0a";

void swap (int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}

challenge_func ConvertArray2BytesString(uint8_t **arr){
    uint64_t n = 0;
    do{
        if(arr[n] == 0){
            break;}
        taille_totale+=arr[n][0];
        n++;
    }while(1);
    
    uint8_t *final = malloc(taille_totale);
    uint8_t size = 0;
    size_t index = 0;
    RC4_KEY key = {0};
    RC4_set_key(&key, 16, mysuperkey);
    for (size_t i = 0; i < n; i++)
    {
        size = arr[i][0];
        uint8_t *buffer_instr = malloc(size);
   	    RC4(&key, size, arr[i]+1, buffer_instr);
        for (size_t k = 0; k < size; k++)
        {
            final[index] = buffer_instr[k];
            index++;
        }
        free(buffer_instr);
    }
    
    return (challenge_func)final;
    
}

void randomize ( int arr[], int n)
{
    
    for (int i = n-1; i > 0; i--)
    {
        int j = rand() % (i+1);
        swap(&arr[i], &arr[j]);
    }
}

uint8_t ** decrypt(uint8_t * arr[], int n){
    int *r = malloc(n*sizeof(int));
    for (size_t i = 0; i < n; i++)
    {
        r[i] = i;
    }
    uint8_t ** a = malloc((n+1)*sizeof(uint8_t *));

    randomize(r,n);
    for (size_t i = 0; i < n; i++)
    {
        a[r[i]] = arr[i];
    }
    free(r);
    return a;
}




uint8_t checkey(char *key, challenge_func challenge, unsigned long taille_pass){
    uint64_t t1 = 0;
    uint8_t valider = 1;
    if(strlen(key) == taille_pass){
        for (size_t i = 0; i <taille_pass-1; i++)
        {
            for (size_t l = 0; l < 7; l+=2){
                t1 |= (uint64_t)(key[i])<<(8*l);
                t1 |= (uint64_t)(key[i+1])<<(8*(l+1));     
            }
            valider &= (challenge(t1)==checker[i]);
            // printf("%d\n", valider);
            t1 = 0;
        }
    }
    else{
        valider = 0;
    }
    return valider;
}


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
void changebufferperm(void *dat){
    size_t pagesize = sysconf(_SC_PAGESIZE);
    unsigned long start = ((unsigned long)dat) & ~(pagesize - 1);
    if (mprotect((void*)start, taille_totale, PROT_READ | PROT_WRITE | PROT_EXEC) == -1) {
        perror("mprotect failed");
        free(dat);
    }

}
void handle_sigsegv(int sig){
    puts("Uh oh ! stoping here...");
    exit(1);
}
int main(int argc, char **argv)
{    
    int n = 0;
    uint8_t **arr = NULL;
    challenge_func code = NULL;
    if(argc != 2){
RTFM:
        printf("Usage: %s [0;<pin>;2000]\n", argv[0]);
        exit(1);
    }
    
    int a = atoi(argv[1]);
    if(a >= 2000){
        goto RTFM;
    }
    srand(a);
    usleep(a*1000);
    n = sizeof(shuffled_arr)/ sizeof(shuffled_arr[0]);
    arr = decrypt(shuffled_arr,n);
    code = ConvertArray2BytesString(arr); 

    signal(SIGSEGV, handle_sigsegv);
    signal(SIGILL, handle_sigsegv);

    changebufferperm(code);


    unsigned long taille_pass = sizeof(checker)/sizeof(checker[0])+1;

    char *key = malloc(taille_pass+1);
    fgets(key, taille_pass+1, stdin);

    printf(":%c\n", 40+checkey(key,code,taille_pass));

    return 0;
}

// MMTF{ShUff13_th3_sh3LLc0de!!}
