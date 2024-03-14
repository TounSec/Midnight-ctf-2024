 
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
void swap (int *a, int *b)
{
    int temp = *a;
    *a = *b;
    *b = temp;
}
 
// A utility function to print an array
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

void encrypt(int arr[], int n){
    srand(123);
    randomize(arr,n);
}

int main(int argc, char **argv)
{
    int a = atoi(argv[1]);
    int arr[] = {1,2,3};
    int n = sizeof(arr)/ sizeof(arr[0]);
    encrypt(arr, n);
    printArray(arr,n);
}
