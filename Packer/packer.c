#include <stdio.h>
#include <stdlib.h>
#include <elf.h>

Elf64_Shdr *find_text_section(const char *elf, size_t *text_section_size);

int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Usage : %s <input_elf>\n", argv[0]);
        return 1;
    }

    const char *input_elf = argv[1];
    size_t text_section_size;
    Elf64_Shdr *text_section_header = find_text_section(input_elf, &text_section_size);
    if (!text_section_header) {
        perror("Text section is empty");
        return 1;
    }

    void *text_section_data = malloc(text_section_size);
    if (!text_section_data) {
        perror("Memory allocation error for text section data");
        return 1;
    }

    FILE *elf = fopen(input_elf, "rb");
    if (!elf) {
        perror("Opening file error");
        free(text_section_data); 
        return 1;
    }

    fseek(elf, text_section_header->sh_offset, SEEK_SET);
    if (fread(text_section_data, 1, text_section_size, elf) != text_section_size) {
        perror("Reading text section error");
        free(text_section_data);
        return 1;
    }

    printf("Bytes of text section\n");
    for (size_t i = 0; i < text_section_size && i < 8; i++) {
        printf("%02x", ((unsigned char*)text_section_data)[i]);
    }
    printf("\n");

    fclose(elf);
    free(text_section_data); 
    return 0;
}

Elf64_Shdr *find_text_section(const char *input_elf, size_t *text_section_size)
{
    FILE *elf = fopen(input_elf, "rb");
    if (!elf) {
        perror("Opening file error");
        return NULL;
    }

    Elf64_Ehdr header;
    if (fread(&header, sizeof(header), 1, elf) != 1) {
        perror("Header reading error");
        return NULL;
    }

    Elf64_Shdr *sections_headers = malloc(header.e_shentsize * header.e_shnum);
    if (!sections_headers) {
        perror("Memory allocation error for section headers");
        return NULL;
    }

    fseek(elf, header.e_shoff, SEEK_SET);
    if (fread(sections_headers, header.e_shentsize, header.e_shnum, elf) != header.e_shnum) {
        perror("Reading section headers error");
        free(sections_headers);
        return NULL;
    }

    Elf64_Shdr *text_section = NULL;
    for (int i = 0; i < header.e_shnum; i++) {
        if (sections_headers[i].sh_type == SHT_PROGBITS &&
            (sections_headers[i].sh_flags & SHF_EXECINSTR)) {
                text_section = &sections_headers[i];
                break;
        }
    }

    if (!text_section) {
        fprintf(stderr, "Section text not found");
        free(sections_headers);
        return NULL;
    }

    *text_section_size = text_section->sh_size;
    return text_section;
}
