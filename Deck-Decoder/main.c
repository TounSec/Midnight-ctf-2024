#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <stdlib.h>
// uint64_t challenge(uint64_t input1);

uint64_t checker[] = {0x751E22F6AFDC1D1A, 0x25E2D8737E1EE778, 0x5FA5062A2A463E93, 0x31E402F96E8BDF97, 0x835BE6989055C8F7, 0x5D96E686BBBB53FA, 0xECE6FF58CDD9D31A, 0xC21A2CBC37DBC25F, 0x504E496158267321, 0x1E7F1D0186F1EC8C, 0x177A0713EE72684C, 0x701183528F5AC6CF, 0xB732A1AFDC2F5679, 0x76C06994CE3A61BC, 0xF5F06AB9884DE54F, 0x701183528F5AC6CF, 0x5A37ADF157A8C201, 0xC094D5287D091C4F, 0xF5F06AB9884DE54F, 0x3DAA050C3B50450E, 0xA93C0AF6A0E9C41C, 0xF5D4CBAB3B2C88A3, 0xA27A01B298EC17A8, 0x5FCEFDDD776A26F0, 0xDEBDE5DBB1C1C4B3, 0xE08C572F24190AB, 0xD512D32829E4869, 0xFFBD122F4A434777};


uint8_t checkey(char *key, void *challenge){
    uint64_t t1 = 0;
    uint8_t valider = 1;
    unsigned long taille_pass = sizeof(checker)/sizeof(checker[0])+1;
    if(strlen(key) == taille_pass){
        for (size_t i = 0; i <taille_pass-1; i++)
        {
            for (size_t l = 0; l < 7; l+=2){
                t1 |= (uint64_t)(key[i])<<(8*l);
                t1 |= (uint64_t)(key[i+1])<<(8*(l+1));     
            }
            valider &= (challenge(t1)==checker[i]);
            t1 = 0;
        }
    }
    return valider;
}

