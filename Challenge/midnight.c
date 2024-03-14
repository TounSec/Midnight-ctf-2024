 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void swap (int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
void printArray (int arr[], int n)
{
    for (int i = 0; i < n; i++)
        printf("%d, ", arr[i]);
    printf("\n");
}
 
void randomize ( int arr[], int n)
{
    
    for (int i = n-1; i > 0; i--)
    {
        int j = rand() % (i+1);
        swap(&arr[i], &arr[j]);
    }
}

int * decrypt(int arr[], int n){
    int *r = malloc(n*sizeof(int));
    for (size_t i = 0; i < n; i++)
    {
        r[i] = i;
    }
    int *a = calloc(n,sizeof(int));

    randomize(r,n);
    for (size_t i = 0; i < n; i++)
    {
        a[r[i]] = arr[i];
    }
    return a;
}

int shuffled_arr[] = {1,3,2};

int main(int argc, char **argv)
{    
    int n = sizeof(shuffled_arr)/ sizeof(shuffled_arr[0]);
    int *arr = calloc(n,sizeof(int));
    srand(123);
    arr = decrypt(shuffled_arr,n);
    printArray(arr,n);
    return 0;
}