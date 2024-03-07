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
# mn = [("add", True), ("sub", True), ("ror", False),
#       ("rol", False), ("shr", False), ("shl", False), ("xor", True), ("or", True), ("xchg", True), ("and", True), ("imul", True)]
mn = {
        1: ["dec", "inc", "bswap", "not"],
        2: [("add", True), ("sub", True), ("ror", False),("rol", False), ("shr", False), ("shl", False), ("xor", True), ("or", True), ("xchg", True), ("and", True), ("imul", True)],
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
for _ in range(1000):
    i = random.randint(1,10)
    arch = random.choice([64, 32, 16, 8])

    if i <= 2:
        r1 = random.choice(registre[arch])
        instruction = random.choice(mn[1])
        
        if instruction == "bswap":
            r1 = random.choice(registre[random.choice([64, 32])])

        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{instruction} {r1}".upper(), loc_db, 64))))
    # elif i == 3:
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"XOR ECX ECX".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"XOR ECX {random.randint(0, 2**8)}".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"LOOP".upper(), loc_db, 64))))
    else:
        
        instruction = random.choice(mn[2])
        r1 = random.choice(registre[arch])

        if instruction[1] == True:
            r2 = random.choice(registre[arch])
            if instruction[0] == "imul":
                choice = random.choice([64,32,16])
                r1 , r2 = random.choice(registre[choice]), random.choice(registre[choice])

            elif instruction[0] != "xchg":
                if random.randint(0, 1):
                    if random.randint(0, 1):
                        arch = random.choice([64, 32, 16])
                        tmpreg = random.choice(registre[arch]) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"CMP {random.choice(registre[8])} {random.randint(0, 2**8)}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{random.choice(cond)} {random.choice(registre[arch])}, {tmpreg}".upper(), loc_db, 64))))
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64))))

                    else:
                        tmpreg = random.choice(registre[arch]) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"MOV {tmpreg}, {random.randint(0, 2**arch)}".upper(), loc_db, 64)))) 
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"{instruction[0]} {random.choice(registre[arch])}, {tmpreg}".upper(), loc_db, 64))))
                        result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"POP {registre[64][registre[arch].index(tmpreg)]}".upper(), loc_db, 64))))
                    continue
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


"""
['AAA', 'AAS', 'AAD', 'AAM', 'ADC', 'ADD', 'AND', 'BNDMOV', 'BSF', 'BSR', 'BSWAP', 'BT', 'BTC', 'BTR', 'BTS', 'CALL', 'CBW', 'CWDE', 'CDQE', 'CLC', 'CLD', 'CLI', 'CLTS', 'CMC', 'CMOVO', 'CMOVNO', 'CMOVB', 'CMOVAE', 'CMOVZ', 'CMOVNZ', 'CMOVBE', 'CMOVA', 'CMOVS', 'CMOVNS', 'CMOVPE', 'CMOVNP', 'CMOVL', 'CMOVGE', 'CMOVLE', 'CMOVG', 'CMP', 'CMPSB', 'CMPSW', 'CMPSD', 'CMPSQ', 'CMPXCHG', 'CMPXCHG8B', 'CMPXCHG16B', 'COMISS', 'COMISD', 'CPUID', 'CWD', 'CDQ', 'CQO', 'DAA', 'DAS', 'DEC', 'DIV', 'ENTER', 'FWAIT', 'F2XM1', 'FABS', 'FADD', 'FADDP', 'FIADD', 'FBLD', 'FBLDP', 'FCHS', 'FNCLEX', 'FCMOVB', 'FCMOVE', 'FCMOVBE', 'FCMOVU', 'FCMOVNB', 'FCMOVNE', 'FCMOVNBE', 'FCMOVNU', 'FCOM', 'FCOMP', 'FCOMPP', 'FCOMI', 'FCOMIP', 'FUCOMI', 'FUCOMIP', 'FCOS', 'FDECSTP', 'FDIV', 'FDIVP', 'FIDIV', 'FDIVR', 'FDIVRP', 'FIDIVR', 'FFREE', 'FICOM', 'FICOMP', 'FILD', 'FINCSTP', 'FNINIT', 'FIST', 'FISTP', 'FISTTP', 'FLD', 'FLD1', 'FLDL2T', 'FLDL2E', 'FLDPI', 'FLDLG2', 'FLDLN2', 'FLDZ', 'FLDCW', 'FLDENV', 'FMUL', 'FMULP', 'FIMUL', 'FNOP', 'FPATAN', 'FPREM', 'FPREM1', 'FPTAN', 'FRNDINT', 'FRSTOR', 'FNSAVE', 'FSCALE', 'FSIN', 'FSINCOS', 'FSQRT', 'FST', 'FSTP', 'FNSTCW', 'FNSTENV', 'FNSTSW', 'FSUB', 'FSUBP', 'FISUB', 'FSUBR', 'FSUBRP', 'FISUBR', 'FTST', 'FUCOM', 'FUCOMP', 'FUCOMPP', 'FXAM', 'FXCH', 'FXRSTOR', 'FXSAVE', 'STMXCSR', 'LDMXCSR', 'FXTRACT', 'FYL2X', 'FYL2XP1', 'HLT', 'ICEBP', 'IDIV', 'IMUL', 'IN', 'INC', 'INSB', 'INSW', 'INSD', 'INT', 'INTO', 'INVD', 'INVLPG', 'IRET', 'IRETD', 'IRETQ', 'JO', 'JNO', 'JB', 'JAE', 'JZ', 'JNZ', 'JBE', 'JA', 'JS', 'JNS', 'JPE', 'JNP', 'JL', 'JGE', 'JLE', 'JG', 'JCXZ', 'JECXZ', 'JRCXZ', 'JMP', 'LAHF', 'LAR', 'LEA', 'LES', 'LDS', 'LSS', 'LFS', 'LGS', 'LGDT', 'LIDT', 'LFENCE', 'MFENCE', 'SFENCE', 'LEAVE', 'LODSB', 'LODSW', 'LODSD', 'LODSQ', 'LOOP', 'LOOPE', 'LOOPNE', 'LSL', 'MONITOR', 'MOV', 'MOVSB', 'MOVSW', 'MOVSD', 'MOVSQ', 'MOVSX', 'MOVSXD', 'MOVUPS', 'MOVSS', 'MOVUPD', 'MOVD', 'MOVQ', 'MOVMSKPS', 'MOVMSKPD', 'MOVNTI', 'ADDSS', 'ADDSD', 'SUBSS', 'SUBSD', 'MULSS', 'MULSD', 'DIVSS', 'DIVSD', 'ROUNDSS', 'ROUNDSD', 'PMINSW', 'UCOMISS', 'UCOMISD', 'MOVZX', 'MUL', 'NEG', 'NOP', 'NOT', 'OR', 'OUT', 'OUTSB', 'OUTSW', 'OUTSD', 'SETALC', 'POPW', 'POP', 'POPA', 'POPAD', 'POPFW', 'POPFD', 'POPFQ', 'PREFETCH0', 'PREFETCH1', 'PREFETCH2', 'PREFETCHNTA', 'PREFETCHW', 'PUSHW', 'PUSH', 'PUSHA', 'PUSHAD', 'PUSHFW', 'PUSHFD', 'PUSHFQ', 'RCL', 'RCR', 'ROL', 'ROR', 'RDMSR', 'RDPMC', 'RDTSC', 'RET', 'RETF', 'RSM', 'SAHF', 'SAL', 'SAR', 'SCASB', 'SCASW', 'SCASD', 'SCASQ', 'SHL', 'SHR', 'SBB', 'SETO', 'SETNO', 'SETB', 'SETAE', 'SETZ', 'SETNZ', 'SETBE', 'SETA', 'SETS', 'SETNS', 'SETPE', 'SETNP', 'SETL', 'SETGE', 'SETLE', 'SETG', 'SGDT', 'SHLD', 'SHRD', 'SIDT', 'SLDT', 'SMSW', 'STC', 'STD', 'STI', 'STOSB', 'STOSW', 'STOSD', 'STOSQ', 'STR', 'SUB', 'SYSCALL', 'SYSENTER', 'SYSEXIT', 'SYSRET', 'TEST', 'UD2', 'VERR', 'VERW', 'WBINVD', 'WRMSR', 'XADD', 'XCHG', 'XLAT', 'XOR', 'XGETBV', 'MOVAPD', 'MOVAPS', 'MOVDQU', 'MOVDQA', 'MOVHPD', 'MOVHPS', 'MOVLPD', 'MOVLPS', 'MOVHLPS', 'MOVLHPS', 'MOVDQ2Q', 'MOVQ2DQ', 'PADDB', 'PADDW', 'PADDD', 'PADDQ', 'PSUBB', 'PSUBW', 'PSUBD', 'PSUBQ', 'ADDPS', 'ADDPD', 'SUBPS', 'SUBPD', 'MULPS', 'MULPD', 'DIVPS', 'DIVPD', 'XORPS', 'XORPD', 'ANDPS', 'ANDPD', 'ANDNPS', 'ANDNPD', 'ORPS', 'ORPD', 'PAND', 'PANDN', 'POR', 'PXOR', 'MINPS', 'MINSS', 'MINPD', 'MINSD', 'MAXPS', 'MAXPD', 'MAXSD', 'MAXSS', 'CMPEQPS', 'CMPEQPD', 'CMPEQSS', 'CMPEQSD', 'CMPLTPS', 'CMPLTPD', 'CMPLTSS', 'CMPLTSD', 'CMPLEPS', 'CMPLEPD', 'CMPLESS', 'CMPLESD', 'CMPUNORDPS', 'CMPUNORDPD', 'CMPUNORDSS', 'CMPUNORDSD', 'CMPNEQPS', 'CMPNEQPD', 'CMPNEQSS', 'CMPNEQSD', 'CMPNLTPS', 'CMPNLTPD', 'CMPNLTSS', 'CMPNLTSD', 'CMPNLEPS', 'CMPNLEPD', 'CMPNLESS', 'CMPNLESD', 'CMPORDPS', 'CMPORDPD', 'CMPORDSS', 'CMPORDSD', 'PSHUFB', 'PSHUFD', 'PSHUFLW', 'PSHUFHW', 'CVTDQ2PD', 'CVTDQ2PS', 'CVTPD2DQ', 'CVTPD2PI', 'CVTPD2PS', 'CVTPI2PD', 'CVTPI2PS', 'CVTPS2DQ', 'CVTPS2PD', 'CVTPS2PI', 'CVTSD2SI', 'CVTSD2SS', 'CVTSI2SD', 'CVTSI2SS', 'CVTSS2SD', 'CVTSS2SI', 'CVTTPD2PI', 'CVTTPD2DQ', 'CVTTPS2DQ', 'CVTTPS2PI', 'CVTTSD2SI', 'CVTTSS2SI', 'PALIGNR', 'PSRLQ', 'PSRLD', 'PSRLDQ', 'PSRLW', 'PSRAW', 'PSRAD', 'PSLLQ', 'PSLLD', 'PSLLW', 'PSLLDQ', 'PMAXUB', 'PMAXUW', 'PMAXUD', 'PMAXSW', 'PMINUB', 'PMINUW', 'PMINUD', 'PCMPEQB', 'PCMPEQW', 'PCMPEQD', 'PCMPGTB', 'PCMPGTW', 'PCMPGTD', 'PCMPEQQ', 'PCMPGTQ', 'PUNPCKHBW', 'PUNPCKHWD', 'PUNPCKHDQ', 'PUNPCKHQDQ', 'PUNPCKLBW', 'PUNPCKLWD', 'PUNPCKLDQ', 'PUNPCKLQDQ', 'UNPCKHPS', 'UNPCKHPD', 'UNPCKLPS', 'UNPCKLPD', 'PINSRB', 'PINSRD', 'PINSRQ', 'PINSRW', 'PEXTRB', 'PEXTRD', 'PEXTRQ', 'PEXTRW', 'SQRTPD', 'SQRTPS', 'SQRTSD', 'SQRTSS', 'PMOVMSKB', 'SHUFPS', 'SHUFPD', 'AESENC', 'AESDEC', 'AESENCLAST', 'AESDECLAST', 'PACKSSWB', 'PACKSSDW', 'PACKUSWB', 'PMULLW', 'PMULHUW', 'PMULHW', 'PMULUDQ', 'PSUBUSB', 'PSUBUSW', 'PSUBSB', 'PSUBSW', 'PADDUSB', 'PADDUSW', 'PADDSB', 'PADDSW', 'PMADDWD', 'PSADBW', 'PAVGB', 'PAVGW', 'MASKMOVQ', 'MASKMOVDQU', 'EMMS', 'INCSSP', 'RDSSP', 'SAVEPREVSSP', 'RSTORSSP', 'WRSS', 'WRUSS', 'SETSSBSY', 'CLRSSBSY', 'ENDBR64', 'ENDBR32']


M: 981BC1D52D7431D6
I: 2BB63972733CF9B6
D: 1FAD56A2F0611409
N: 54C0663CE5E5CDE
I: 2BB63972733CF9B6
G: EEF36B282A9FFEC7
H: BE8DA63E0D748C64
T: C7B378983FD7EADF
{: 91C78ABB5237A49A
C: 744C4D495302BDAC
O: 973613FE7740172A
U: 3CBA79B23996036
C: 744C4D495302BDAC
O: 973613FE7740172A
U: 3CBA79B23996036
L: 627AC4B3BE24E88C
E: 98AC3E827694B482
S: 2D39E226DBFE8B55
B: 143B0A655A85FB96
O: 973613FE7740172A
S: 2D39E226DBFE8B55
S: 2D39E226DBFE8B55
}: B7CE09FA42D98513

"""