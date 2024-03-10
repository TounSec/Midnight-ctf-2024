#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <unistd.h>
#include <yvals.h>

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
        for (size_t i = 0; i < bytes_read; i++) {
            buffer[i] /= 2;
        }
        fwrite(buffer, 1, bytes_read, out);
    }
    fclose(in);
    fclose(out);
}

// Fonction of decompress executable image
void decompress_img(const char *compressed_img)
{
   FILE *in = fopen(compressed_img, "rb");

    if (!in) {
        perror("Error opening compressed file");
        return;
    }

    // Read the size of the original executable image
    fseek(in, 0, SEEK_END);
    long file_size = ftell(in);
    fseek(in, 0, SEEK_SET);

    // Allocate memory for executable image
    void *executable_img = mmap(
        NULL,
        file_size,
        PROT_READ   | PROT_WRITE    | PROT_EXEC,
        MAP_PRIVATE | MAP_ANONYMOUS,
        -1,
        0
    );

    if (executable_img == MAP_FAILED) {
        perror("Memory allocation error");
        return;
    }

    // Read and decompress executable image
    char buffer[1024];
    size_t bytes_read;

    while ((bytes_read = fread(buffer, 1, sizeof(buffer), in)) > 0) {
        for (size_t i = 0; i < bytes_read; i++) {
            buffer[i] *= 2;
        }
        memcpy(executable_img, buffer, bytes_read);
    }
    fclose(in);

    // Execute image
    ((void (*)())executable_img)();
}
