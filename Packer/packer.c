#include <stdio.h>
#include <stdlib.h>
#include <elf.h>

void read_elf64_header(const char *input_elf);


int main(int argc, char *argv[])
{
    if (argc < 2) {
        fprintf(stderr, "Usage : %s <input_elf>\n", argv[0]);
        return 1;
    }

    const char *input_elf = argv[1];
    read_elf64_header(input_elf);

    return 0;
}


void read_elf64_header(const char *input_elf)
{
    FILE *elf = fopen(input_elf, "rb");
    if (!elf) {
        perror("Error opening file");
        return;
    }

    Elf64_Ehdr header;
    if (fread(&header, sizeof(header), 1, elf) != 1) {
        perror("Header reading error");
        return;
    }

    printf("Magic : ");
    for (int i = 0; i < EI_NIDENT; i++) {
        printf("%02x", header.e_ident[i]);
    }
    printf("\n");

    printf("Type : %u\n", header.e_type);
    printf("Machine : %u\n", header.e_machine);
    printf("Version : %u\n", header.e_version);
    printf("Entry point address : %lu\n", header.e_entry);
    printf("Program header offset : %lu\n", header.e_phoff);
    printf("Section header offset : %lu\n", header.e_shoff);
    printf("Flags : %u\n", header.e_flags);
    printf("ELF header size : %u\n", header.e_ehsize);
    printf("Program header size : %u\n", header.e_phentsize);
    printf("Number of program headers : %u\n", header.e_phnum);
    printf("Section header size : %u\n", header.e_shentsize);
    printf("Number of section headers : %u\n", header.e_shnum);
    printf("Section header string table index : %u\n", header.e_shstrndx);

    fclose(elf);
}
