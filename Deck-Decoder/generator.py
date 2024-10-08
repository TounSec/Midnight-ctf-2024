from miasm.arch.x86.arch import mn_x86
from miasm.core.locationdb import LocationDB
from Crypto.Cipher.ARC4 import ARC4Cipher
import random
import shufflegen

random.seed(b"zefzfjiozejn")
result = []
# mn = [("add", True), ("sub", True), ("ror", False),
#       ("rol", False), ("shr", False), ("shl", False), ("xor", True), ("or", True), ("xchg", True), ("and", True), ("imul", True)]
mn = {
        1: ["dec", "inc", "bswap", "not", "mul"],
        2: [("add", True), ("sub", True), ("ror", False),("rol", False), ("shr", False), ("shl", False), ("xor", True), ("or", True), ("xchg", True), ("imul", True)],
        }

registre = {
        64: ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "r8", "r9", "r10", "r11"],
        32: ["eax", "ebx", "ecx", "edx", "esi", "edi"],
        16: ["ax", "bx", "cx", "dx", "si", "di"],
        8:  ["al", "bl", "cl", "dl", "sil", "dil"],
        }
cond = ['CMOVO', 'CMOVNO', 'CMOVB', 'CMOVAE', 'CMOVZ', 'CMOVNZ', 'CMOVBE', 'CMOVA', 'CMOVS', 'CMOVNS', 'CMOVPE', 'CMOVNP', 'CMOVL', 'CMOVGE', 'CMOVLE', 'CMOVG']
loc_db = LocationDB()

for element in registre[64]:
    if element != "rdi":
        if element != "rax":
            result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {element.upper()}", loc_db, 64))))
        instruction = f"MOV {element}, {random.randint(0, 0xffffffffffffffff)}"
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))
    
        instruction = f"XOR {element}, rdi"
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))
        # instruction = f"XOR {element}, rsi"
        # result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))

for _ in range(1500):
    i = random.randint(1,10)
    arch = random.choice([64, 32, 16, 8])

    if i <= 2:
        r1 = random.choice(registre[arch])
        instruction = random.choice(mn[1])
        
        if instruction == "bswap":
            r1 = random.choice(registre[random.choice([64, 32])])

        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{instruction} {r1}".upper(), loc_db, 64))))
    else:
        
        instruction = random.choice(mn[2])
        r1 = random.choice(registre[arch])

        if instruction[1] == True:
            r2 = random.choice([e for e in registre[arch] if e != r1])
            if instruction[0] in ["imul"]:
                choice = random.choice([64,32,16])
                r1 , r2 = random.choice(registre[choice]), random.choice(registre[choice])

            elif instruction[0] != "xchg":
                if random.randint(0, 1):
                    if random.randint(0, 1):
                        arch = random.choice([64, 32, 16])
                        tmpreg = random.choice(registre[arch]) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"CMP {random.choice(registre[8])} {random.randint(0, 2**8)}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{random.choice(cond)} {random.choice([e for e in registre[arch] if e != tmpreg])}, {tmpreg}".upper(), loc_db, 64))))
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64))))

                    else:
                        tmpreg = random.choice(registre[arch]) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"MOV {tmpreg}, {random.randint(0, 2**arch)}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{instruction[0]} {random.choice([e for e in registre[arch] if e != tmpreg])}, {tmpreg}".upper(), loc_db, 64))))
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64))))
                    continue
        else:
            if instruction[0] in ["shl", "shr"]:
                r2 = (random.randint(0, arch//8))
            else:
                r2 = (random.randint(0, arch))

        instruction = f"{instruction[0]}  {r1}, {r2}"
        l = mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))
        choice = random.choice(l)
        result.append(choice)
        # print(choice)
        # print()

for element in registre[64]:
    if element != "rax":
        instruction = f"XOR RAX, {element}"
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(instruction.upper(), loc_db, 64))))

for element in registre[64][::-1]: 
    if element != "rdi" and element != "rax":
        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {element.upper()}", loc_db, 64))))

result.append(b"\xc3")
open("output.hexx", "wb").write(b"".join(result))
# for e in result:
#     print(e.hex())
# exit(1)
for i in range(len(result)):
    result[i] = len(result[i]).to_bytes(1,"little")+result[i]
print("{")
c = ARC4Cipher(bytes.fromhex("e1a4646ee8acd20f4578dbea4a79380a"))
for elm in result:
    encrypted_part = c.encrypt(elm[1:])
    encrypted_part_hex = ''.join(f'\\x{byte:02x}' for byte in encrypted_part)
    print(f"\"\\x{elm[0]:02x}{encrypted_part_hex}\", ", end ="")
print("}")