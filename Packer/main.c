#include <stddef.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <unistd.h>
#include <zlib.h>

void compress_elf(const char *input_file, const char *output_file);
void decompress_and_execute_elf(const char *input_file);

int main(int argc, char *argv[])
{
    if (argc < 3) {
        fprintf(stderr, "Usage : %s <compress|decompress> <input_file> <output_file>");
        return 1;
    }

    const char *action = argv[1];
    const char *input_file = argv[2];
    const char *output_file = argv[3];

    if (strcmp(action, "compress") == 0) {
        compress_elf(input_file, output_file);
    } else if (strcmp(action, "decompress") == 0) {
        decompress_and_execute_elf(input_file);
    } else {
        fprintf(stderr, "Invalid action");
        return 1;
    }
    return 0;
}

void compress_elf(const char *input_file, const char *output_file)
{
    FILE *in = fopen(input_file, "rb");
    FILE *out = fopen(output_file, "wb");

    if (!in || !out) {
        perror("Error opening files");
        return;
    }

    char buffer[1024];
    size_t bytes_read;
}
