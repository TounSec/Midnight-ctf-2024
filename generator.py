from miasm.arch.x86.arch import mn_x86
from miasm.core.locationdb import LocationDB
import random


def rotate_right_32bit(value, shift):
    shift %= 32  # Ensure the shift is within the 32-bit boundary
    return (value >> shift) | (value << (32 - shift)) & 0xFFFFFFFF

a = random.randint(0,0xffffffff)
b = random.randint(0,0xffffffff)

random.seed(b"0xTASOEURLASCENSEUR")
result = []
mn = [("add", True), ("sub", True), ("ror", False),
      ("rol", False), ("shr", False), ("shl", False), ("xor", True), ("or", True), ("xchg", True), ("and", True)]
registre = {
        64: ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"],
        32: ["eax", "ebx", "ecx", "edx", "esi", "edi"],
        16: ["ax", "bx", "cx", "dx", "si", "di"],
        8:  ["al", "bl", "cl", "dl", "sil", "dil"],
        }

loc_db = LocationDB()

for element in registre[64]:
    if element != "rdi":
        if element != "rax":
            result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {element.upper()}", loc_db, 64))))
        instruction = f"MOV {element}, {random.randint(0, 0xffffffffffffffff)}"
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))
    
        instruction = f"XOR {element}, rdi"
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))
for _ in range(1000):
    instruction = random.choice(mn)
    arch = random.choice([64, 32, 16, 8])
    r1 = random.choice(registre[arch])

    if instruction[1] == True:
        r2 = random.choice(registre[arch])
        if instruction[0] != "xchg":
           if random.randint(0, 1):
                tmpreg = random.choice(registre[arch]) 
                result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64)))) 
                result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"MOV {tmpreg}, {random.randint(0, 2**arch)}".upper(), loc_db, 64)))) 
                result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{instruction[0]} {random.choice(registre[arch])}, {tmpreg}".upper(), loc_db, 64))))
                result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64))))
    else:
        if instruction[0] in ["shl", "shr"]:
            r2 = (random.randint(0, arch//4))
        else:
            r2 = (random.randint(0, arch))

    instruction = f"{instruction[0]}  {r1}, {r2}"
    l = mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))
    choice = random.choice(l)
    result.append(choice)
    print(choice)
    print()

for element in registre[64]:
    if element != "rax":
        instruction = f"XOR RAX, {element}"
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))

for element in registre[64][::-1]: 
    if element != "rdi" and element != "rax":
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {element.upper()}", loc_db, 64))))

result.append(b"\xc3")
stringfinal = b"".join(result)
open("output.hex","wb").write(stringfinal.hex().encode())
