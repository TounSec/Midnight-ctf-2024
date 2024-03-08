from miasm.arch.x86.arch import mn_x86
from miasm.core.locationdb import LocationDB
import random


random.seed(b"0xTASOEURLASCENSEUR")
result = []
# mn = [("add", True), ("sub", True), ("ror", False),
#       ("rol", False), ("shr", False), ("shl", False), ("xor", True), ("or", True), ("xchg", True), ("and", True), ("imul", True)]
mn = {
        1: ["dec", "inc", "bswap", "not", "mul"],
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
    #     choice = random.choice(registre[64])
    #     # result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"PUSH {random.choice(registre[64])}".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"vmovdqu MM0 {random.choice(registre[64])}".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"MOVQ MM1 {random.choice(registre[64])}".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"punpckhbw MM0 MM1".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"MOVQ {random.choice(registre[64])}, XMM0".upper(), loc_db, 64)))) 
    #     result.append(random.choice(mn_x86.asm(mn_x86.fromstring(f"EMMS".upper(), loc_db, 64)))) 

    else:
        
        instruction = random.choice(mn[2])
        r1 = random.choice(registre[arch])

        if instruction[1] == True:
            r2 = random.choice(registre[arch])
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
0: 9E154644F3E00CA2
1: C6FE74E48989140F
2: 25D54E8EB0F0D2DE
3: CCFF2FC46F2E72A0
4: 97F67154CE6D8D31
5: 28F80DB616A32E3F
6: 3777D0BD82ED0D0
7: FE84213ED7427053
8: 88A0A677505D55FC
9: F599EFC4F48E5D98
A: 5C1771682EA3FD9E
B: 369D5E56C0CAA59A
C: AF783E62A0638083
D: 1503D6844610B76D
E: C8444046AB77FF17
F: AF11C934595F6407
10: CDBD7C765E920303
11: 66BDC264E190C383
12: E293B9DBF1B7B9D0
13: FE0A4E62C55EC64F
14: A7E978F433C19743
15: BADB8441686223F
16: B5B809A4BE9B2392
17: 77BF1B24F0B8FC48
18: B1AC8264459B7B04
19: 95228B3033BA6219
1A: 5A9C60A4A7681B21
1B: 532C5A24FDAB16E6
1C: 1D7A1A8ABB597142
1D: 41D93F4B446AC1F2
1E: 4561EEC456ACF57F
1F: BCFFDF6493C9E347
20: 435AD285A2904270
21: 48C8F01B7B2EF861
22: 68870652ED8772F1
23: 87D957BE593068FD
24: 302EF89375B1BC90
25: 3D6B4984454695AA
26: 382258CB156E6AE3
27: F91409EB15DFB2B6
28: D1E737AB40C832E0
29: 397C10D628137F8A
2A: 1BB25FBC1D4DF9F0
2B: 8293F8F7204649B0
2C: 426C7708E2148432
2D: AABA373614BF8753
2E: E35613C0F5600C8
2F: 8D4AA1ABDDFFADC8
30: A0307EBA21505D9C
31: 89A0FCB481DF1437
32: E1743FE932320B86
33: 3E5E178BEE1B53B1
34: 5A9CC624E7B03B34
35: F62C4CA4D5741D4A
36: C43214D4D6023732
37: 5D35C8C4E3CA9839
38: 5160B7E4125A6383
39: EBC677DB961E689B
3A: BDC40604E1CEE4AC
3B: 46DF2D64BA64CFF2
3C: 6CCBE14BA9CAAB1
3D: 88C60D044E40B4FE
3E: FD6A2A245EE3E85A
3F: 60DED1E4711DE5C9
40: 3B5135440B3236D9
41: 495B3F2EE2729CB5
42: C392C84B951E72F4
43: 4FB07B1E42B3B197
44: 2D5D774AE2182489
45: FB71E9E947CEA75D
46: 24D751B4BEE49834
47: 2C921276D9A34228
48: D3AD7964CCE61AF6
49: 1E4E399E10C3CB82
4A: 4F3CA51432C98D3B
4B: 59DA20AB5DCA91B5
4C: EACE6CD653DA832E
4D: F3D66F147A312B13
4E: CA4A2A844CDA5B92
4F: C852EDB85F1F760F
50: 674AD3D4B9DF66EC
51: 9A2F783BC35EECCA
52: 24D9DA148B84166E
53: 4F3A709ACFFC6629
54: EA8C69248DDBB3A6
55: 9C091974FCEEBFE2
56: 7594C5A4C924BF1E
57: C21E5244BB9933E7
58: 9BC0A58611514FEA
59: 1EB4952FEDAC8E90
5A: E3EF83ABD77909D2
5B: C7E4ED04298F99D3
5C: 41444A1FED9F4807
5D: ADDE56260AC32194
5E: AF96B7B8F34A94E3
5F: D7C5748908C471F1
60: 45C62FC47B00614A
61: 7114DC0473D99C91
62: 160B55885249BDA6
63: 742AB63CE61B3CF0
64: A150A80493F84917
65: A698A33A67A469E3
66: 3A85FCAB9F376F3A
67: D9613348145F6B0
68: C78D8C24C6A2A7C2
69: 632767605914B8F9
6A: 99CDF2A4557AF3EF
6B: A8DB170C654D2246
6C: 2A8CC7A4FA8C1B40
6D: 7F25FB84A88D1998
6E: 4EBA3AC480EF97F2
6F: A5823E4A2FA0481D
70: 47072E4451EB91AE
71: 4B16427FA51E62EC
72: 30E36BDEC304DF08
73: 89D429727B6D9A54
74: A780551B0F4889A1
75: 4A228DFCD894CEB6
76: 358223849921257B
77: DA91528EC28D2E4A
78: 1136F44AC0D9E39D
79: 89720C06B5C1E3EE
7A: 56458B042C912E44
7B: B7D8FC731E6AD3EB
7C: 28A54F62FA9C38BA
7D: 6FA6B73837D3420A
7E: 749C205CCE2BB60D
7F: 9944E5F4F25ABEE7
80: 6F6F66ABD69AB216
81: B12F1F8B1B5DB789
82: 1414400FD436A036
83: FE0B9952FCC511DD
84: D7695376AC686DD3
85: 97413CDE122D13F5
86: F0DF732BDCF703AA
87: A9A5DA1844398237
88: CB590472C5341BE0
89: D661B9FBD7733DEE
8A: 4F882174754A5D26
8B: 11BAAEABF02465B5
8C: 6166B78BF9F1E9E5
8D: B8E062AB3FAA6271
8E: 131CE4C4C01C0DCB
8F: 378307A15B5CF0C4
90: 3DC9FDDFF3A882BB
91: CFC54ACC4DC9542C
92: 67C3EE561456616E
93: CB33E789E3344568
94: 5B7AE3977AD56C9A
95: CE52B76DDCE68E5C
96: 5311FEC4609686C0
97: 4ADB7762D73A7146
98: 1859F3E0C6F368DD
99: 563D79D487DAF894
9A: B622CA94C1D42973
9B: 2230181B3B4F8EDF
9C: 8AB7254B492B253
9D: 37BFF8A695321B3E
9E: 3B5A4C6464E3BFE1
9F: 612258C96AD6EA58
A0: 93D007CAEDAEF37E
A1: 127E05944ABBD04C
A2: A816A09B48FA69AC
A3: 428573057C2F0AC9
A4: EE61F90E7E4776AE
A5: 18903F54FB083064
A6: 2AC56084E91C9194
A7: 18940BA48BC23D10
A8: 693375BC20AD515B
A9: 74E912E94C836200
AA: 5C10166B3A34B010
AB: 43FA666AE276AD23
AC: AE8DE344C1248D9F
AD: 5CC2990407A8CE23
AE: 534066C939B56EE4
AF: DB361DC4D2445378
B0: DC0C15948E88A7A8
B1: 7B076B864367D15A
B2: 44D9D422FD54974A
B3: 6A18E6847E78A6B6
B4: E249332B9845A3FB
B5: 598984E427F877B3
B6: 2EC4EE8C76F64A61
B7: 87D61852B9760C10
B8: F56C6664495459DA
B9: D0A6A7AC3FAFCAF2
BA: 12CEA9F4E751F467
BB: FC405E8B4F547484
BC: FDC051C4232602CD
BD: E4E2D0CE9F84B5D6
BE: DB4D2184DD1A374D
BF: 7EE6BFC63513A69A
C0: 71E4D3D555EA7CC3
C1: 3F767FA4F8042396
C2: F412491599A5C844
C3: 1ACEE4BA6004CC07
C4: 9BC9AFF21AD81A1E
C5: 1B0A62020F9DD2B3
C6: 50F4FF6B4B2A0575
C7: 91A4560FE1394A13
C8: 2E903BDB91DB0BD0
C9: 271A476BB895771F
CA: FB5EB09A586ED0B7
CB: AB15A186C0AA328
CC: BCA2BCEB9D584473
CD: B7F872641CBEDEC3
CE: 1264504AD77B63A
CF: A9B89EE4AAF23725
D0: 277D5604A3B06D70
D1: A49585EC84C82204
D2: 83704D24A919F36E
D3: 6D7926A425EAEC74
D4: FE2E631F1F83E1BB
D5: CDA842C41BD6B5CB
D6: 77CB4D7BF0BD1782
D7: 1D8B00D4DAFD040D
D8: 2E61B704FE2417C8
D9: A45AC5284400D8CD
DA: 42FA98BB00E79C6
DB: DB70514449BFFD6C
DC: 91DEC66A2360572F
DD: 5F11118B5E2CB751
DE: 4899A6CB5FABB347
DF: 88167C9A837E0837
E0: ABAFA75B3AAFFDF7
E1: 38CFDDF4DCC736AE
E2: ED3FB39671BAADFB
E3: 58587FAB04B8BDB5
E4: A29238D815A936AD
E5: F704F428A65D589E
E6: C6EBA5E4758D7193
E7: 52FBEC4266F1581
E8: AF4EEF845E5FAA03
E9: 1F45FF4499136770
EA: 365A91B69F9F96A2
EB: B522049E1CBB16
EC: 2D92C71D48C7FAF2
ED: F0B6A984BC9CDBEB
EE: 21F8620013F0AFC8
EF: B584DFD417E92FC0
F0: 99877044646937BC
F1: 9E3BDE04552BA367
F2: 7F366624FA6C881A
F3: 6378B6E4353FF03B
F4: 3E03DA403C86F4D
F5: D5257364B884457F
F6: 2EC20FD280B3702E
F7: 4B1622D4BD3CA2D1
F8: 8B4C6CC3CFB4FE9
F9: F48320E53596D0C2
FA: 14BE650BDC1C25E4
FB: E849E2B6CCD2920F
FC: 10219F2B8EF0B197
FD: 840908402DBCBB5
FE: DC552E24B55D25A8
FF: 5929484B6536D1D4
"""