#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <zlib.h>

void compress_img(const char *input_file, const char *output_file);
void decompress_img(const char *compressed_img);

int main(int argc, char *argv[])
{
    if (argc < 4) {
        fprintf(stderr, "Usage : %s <compress|decompress> <input_file> <output_file>\n", argv[0]);
        return 1;
    }

    const char *action = argv[1];
    const char *input_file = argv[2];
    const char *output_file = argv[3];

    if (strcmp(action, "compress") == 0) {
        compress_img(input_file, output_file);
    } else if (strcmp(action, "decompress") == 0) {
        decompress_img(input_file);
    } else {
        fprintf(stderr, "Invalid action. Use 'compress' or 'decompress'\n");
        return 1;
    }
    return 0;
}

// Fonction of compress executable image
void compress_img(const char *input_file, const char *output_file)
{
    FILE *in = fopen(input_file, "rb");
    FILE *out = fopen(output_file, "wb");

    if (!in || !out) {
        perror("Error openings files");
        return;
    }

    char buffer[1024];
    size_t bytes_read;

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), in) ) > 0) {
        uLong compressed_size = compressBound(bytes_read);
        Bytef *compressed_data = malloc(compressed_size);

        if (compress(compressed_data, &compressed_size, (const Bytef*)buffer, bytes_read) != Z_OK) {
            perror("Compressions error");
            return;
        }
        fwrite(buffer, 1, bytes_read, out);
        free(compressed_data);
    }
    fclose(in);
    fclose(out);
}

// Fonction of decompress executable image
void decompress_img_and_execute(const char *compressed_img)
{
   FILE *in = fopen(compressed_img, "rb");

    if (!in) {
        perror("Error opening compressed file");
        return;
    }


    // Read and decompress executable image
    char buffer[1024];
    size_t bytes_read;

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), in)) > 0) {
        uLong uncompressed_size = bytes_read * 2;
        Bytef *uncompressed_data = malloc(uncompressed_size);

        if (uncompress(uncompressed_data, &uncompressed_size, (const Bytef*)buffer, bytes_read) != Z_OK) {
            perror("Decompression error");
            return;
        }

        void *executable_memory = mmap(
            NULL,
            uncompressed_size,
            PROT_READ   | PROT_WRITE | PROT_EXEC,
            MAP_PRIVATE | MAP_ANONYMOUS,
            -1,
            0
        );

        if (executable_memory == MAP_FAILED) {
            perror("Memory allocation error");
            return;
        }
        memcpy(executable_memory, uncompressed_data, uncompressed_size);

        if (mprotect(executable_memory, uncompressed_size, PROT_READ | PROT_EXEC) == -1) {
            perror("Error changing permissions");
            return;
        }
    }
    // Execute image
    ((void (*)())executable_img)();

    munmap(executable_memory, uncompressed_size);
    free(uncompressed_data);

    fclose(in);

}
