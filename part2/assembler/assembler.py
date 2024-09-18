import re
import sys

instructions = {
    'NOP':      0x00,
    'LXI B':    0x01,
    'STAX B':   0x02,
    'INX B':    0x03,
    'INR B':    0x04,
    'DCR B':    0x05,
    'MVI B':    0x06,
    'RLC':      0x07,
    'DAD B':    0x09,
    'LDAX B':   0x0A,
    'DCX B':    0x0B,
    'INR C':    0x0C,
    'DCR C':    0x0D,
    'MVI C':    0x0E,
    'RRC':      0x0F,
    'LXI D':    0x11,
    'STAX D':   0x12,
    'INX D':    0x13,
    'INR D':    0x14,
    'DCR D':    0x15,
    'MVI D':    0x16,
    'RAL':      0x17,
    'DAD D':    0x19,
    'LDAX D':   0x1A,
    'DCX D':    0x1B,
    'INR E':    0x1C,
    'DCR E':    0x1D,
    'MVI E':    0x1E,
    'RAR':      0x1F,
    'RIM':      0x20,
    'LXI H':    0x21,
    'SHLD':     0x22,
    'INX H':    0x23,
    'INR H':    0x24,
    'DCR H':    0x25,
    'MVI H':    0x26,
    'DAA':      0x27,
    'DAD H':    0x29,
    'LHLD':     0x2A,
    'DCX H':    0x2B,
    'INR L':    0x2C,
    'DCR L':    0x2D,
    'MVI L':    0x2E,
    'CMA':      0x2F,
    'SIM':      0x30,
    'LXI SP':   0x31,
    'STA':      0x32,
    'INX SP':   0x33,
    'INR M':    0x34,
    'DCR M':    0x35,
    'MVI M':    0x36,
    'STC':      0x37,
    'DAD SP':   0x39,
    'LDA':      0x3A,
    'DCX SP':   0x3B,
    'INR A':    0x3C,
    'DCR A':    0x3D,
    'MVI A':    0x3E,
    'CMC':      0x3F,
    'MOV B,B':  0x40,
    'MOV B,C':  0x41,
    'MOV B,D':  0x42,
    'MOV B,E':  0x43,
    'MOV B,H':  0x44,
    'MOV B,L':  0x45,
    'MOV B,M':  0x46,
    'MOV B,A':  0x47,
    'MOV C,B':  0x48,
    'MOV C,C':  0x49,
    'MOV C,D':  0x4A,
    'MOV C,E':  0x4B,
    'MOV C,H':  0x4C,
    'MOV C,L':  0x4D,
    'MOV C,M':  0x4E,
    'MOV C,A':  0x4F,
    'MOV D,B':  0x50,
    'MOV D,C':  0x51,
    'MOV D,D':  0x52,
    'MOV D,E':  0x53,
    'MOV D,H':  0x54,
    'MOV D,L':  0x55,
    'MOV D,M':  0x56,
    'MOV D,A':  0x57,
    'MOV E,B':  0x58,
    'MOV E,C':  0x59,
    'MOV E,D':  0x5A,
    'MOV E,E':  0x5B,
    'MOV E,H':  0x5C,
    'MOV E,L':  0x5D,
    'MOV E,M':  0x5E,
    'MOV E,A':  0x5F,
    'MOV H,B':  0x60,
    'MOV H,C':  0x61,
    'MOV H,D':  0x62,
    'MOV H,E':  0x63,
    'MOV H,H':  0x64,
    'MOV H,L':  0x65,
    'MOV H,M':  0x66,
    'MOV H,A':  0x67,
    'MOV L,B':  0x68,
    'MOV L,C':  0x69,
    'MOV L,D':  0x6A,
    'MOV L,E':  0x6B,
    'MOV L,H':  0x6C,
    'MOV L,L':  0x6D,
    'MOV L,M':  0x6E,
    'MOV L,A':  0x6F,
    'MOV M,B':  0x70,
    'MOV M,C':  0x71,
    'MOV M,D':  0x72,
    'MOV M,E':  0x73,
    'MOV M,H':  0x74,
    'MOV M,L':  0x75,
    'HLT':      0x76,
    'MOV M,A':  0x77,
    'MOV A,B':  0x78,
    'MOV A,C':  0x79,
    'MOV A,D':  0x7A,
    'MOV A,E':  0x7B,
    'MOV A,H':  0x7C,
    'MOV A,L':  0x7D,
    'MOV A,M':  0x7E,
    'MOV A,A':  0x7F,
    'ADD B':    0x80,
    'ADD C':    0x81,
    'ADD D':    0x82,
    'ADD E':    0x83,
    'ADD H':    0x84,
    'ADD L':    0x85,
    'ADD M':    0x86,
    'ADD A':    0x87,
    'ADC B':    0x88,
    'ADC C':    0x89,
    'ADC D':    0x8A,
    'ADC E':    0x8B,
    'ADC H':    0x8C,
    'ADC L':    0x8D,
    'ADC M':    0x8E,
    'ADC A':    0x8F,
    'SUB B':    0x90,
    'SUB C':    0x91,
    'SUB D':    0x92,
    'SUB E':    0x93,
    'SUB H':    0x94,
    'SUB L':    0x95,
    'SUB M':    0x96,
    'SUB A':    0x97,
    'SBB B':    0x98,
    'SBB C':    0x99,
    'SBB D':    0x9A,
    'SBB E':    0x9B,
    'SBB H':    0x9C,
    'SBB L':    0x9D,
    'SBB M':    0x9E,
    'SBB A':    0x9F,
    'ANA B':    0xA0,
    'ANA C':    0xA1,
    'ANA D':    0xA2,
    'ANA E':    0xA3,
    'ANA H':    0xA4,
    'ANA L':    0xA5,
    'ANA M':    0xA6,
    'ANA A':    0xA7,
    'XRA B':    0xA8,
    'XRA C':    0xA9,
    'XRA D':    0xAA,
    'XRA E':    0xAB,
    'XRA H':    0xAC,
    'XRA L':    0xAD,
    'XRA M':    0xAE,
    'XRA A':    0xAF,
    'ORA B':    0xB0,
    'ORA C':    0xB1,
    'ORA D':    0xB2,
    'ORA E':    0xB3,
    'ORA H':    0xB4,
    'ORA L':    0xB5,
    'ORA M':    0xB6,
    'ORA A':    0xB7,
    'CMP B':    0xB8,
    'CMP C':    0xB9,
    'CMP D':    0xBA,
    'CMP E':    0xBB,
    'CMP H':    0xBC,
    'CMP L':    0xBD,
    'CMP M':    0xBE,
    'CMP A':    0xBF,
    'RNZ':      0xC0,
    'POP B':    0xC1,
    'JNZ':      0xC2,
    'JMP':      0xC3,
    'CNZ':      0xC4,
    'PUSH B':   0xC5,
    'ADI':      0xC6,
    'RST 0':    0xC7,
    'RZ':       0xC8,
    'RET':      0xC9,
    'JZ':       0xCA,
    'CZ':       0xCC,
    'CALL':     0xCD,
    'ACI':      0xCE,
    'RST 1':    0xCF,
    'RNC':      0xD0,
    'POP D':    0xD1,
    'JNC':      0xD2,
    'OUT':      0xD3,
    'CNC':      0xD4,
    'PUSH D':   0xD5,
    'SUI':      0xD6,
    'RST 2':    0xD7,
    'RC':       0xD8,
    'JC':       0xDA,
    'IN':       0xDB,
    'CC':       0xDC,
    'SBI':      0xDE,
    'RST 3':    0xDF,
    'RPO':      0xE0,
    'POP H':    0xE1,
    'JPO':      0xE2,
    'XTHL':     0xE3,
    'CPO':      0xE4,
    'PUSH H':   0xE5,
    'ANI':      0xE6,
    'RST 4':    0xE7,
    'RPE':      0xE8,
    'PCHL':     0xE9,
    'JPE':      0xEA,
    'XCHG':     0xEB,
    'CPE':      0xEC,
    'XRI':      0xEE,
    'RST 5':    0xEF,
    'RP':       0xF0,
    'POP PSW':  0xF1,
    'JP':       0xF2,
    'DI':       0xF3,
    'CP':       0xF4,
    'PUSH PSW': 0xF5,
    'ORI':      0xF6,
    'RST 6':    0xF7,
    'RM':       0xF8,
    'SPHL':     0xF9,
    'JM':       0xFA,
    'EI':       0xFB,
    'CM':       0xFC,
    'CPI':      0xFE,
    'RST 7':    0xFF
}

"Nacitanie kodu -> tokenizacia -> syntax check -> preklad na strojovy kod(mapovanie instrukcii, generovanie strojoveho kodu), -> vystup?"

"""
2 pass assembler -> 
    pass1: precitat instrukcie a dat cisla na kazdu lokaciu instrukcie nech mozes vypocitat label hodnoty

    pass2: precitat instrukcie a zajebat to do strojoveho kodu
"""
#konvertuje decimal na 8bit dvojkovy komplement v binarke

def dec2comp8(d, linenum):
    try:
        if d > 0:
            l = d.bit_length()
            v = "00000000"
            v = v[0:8-1] + format(dt, 'b')[:]
        elif d < 0:
            dt = 128 + d
            l = dt.bit_length()
            v = "10000000"
            v = v[0:8-1] + format(dt, 'b')[:]
        else:
            v = "00000000"
    except:
        print('Invalid decimal number on line %d' % (linenum))
        exit()
    return v

#decimal na 8bit binary
def dec2bin8(d, linenum):
    if d > 0:
        l = d.bit_length()
        v = "00000000"
        v = v[0:8-1] + format(d, 'b')
    elif d == 0:
        v = "00000000"
    else:
        print('invalid adresa na %d: ' & (linenum))
        exit()
    return v

def tokenize(fp): 
    tokens = []
    fp.seek(0)

    lines = fp.readlines()

    for line in lines:
        ls = line.strip()
        uls = ''
        for c in ls:
            if c != '#':
                uls = uls + c
            else:
                break
        #skip prazdnych riadkov
        if len(uls) == 0:
            continue

        #split na medzery
        words = uls.split()

        newwords = []
        for word in words:
            newwords.append(word.lower())
        tokens.append(newwords)
    print(tokens)
    return tokens

# -> najst labely (najcastejsie dvojbodka), ulozit adresu instrukcie a priradit labely
def pass1(tokens):
    labels = {}
    pc = 0
    for i, line in enumerate(tokens):
        if len(line) == 0:
            continue
        if ':' in line[0]:
            labels[line[0].replace(':', '')] = pc
        else:
            pc += 1
    
    return labels
#namapovat instrukcie na strojovy kod, ak odkazuje na label, nahradit ho adresou z prveho prechodu
def pass2(tokens, labels):
    machine_code = []
    for line in tokens:
        if ':' in line[0]:
            continue
        opcode = instructions.get(line[0], None)
        if opcode:
            if line[1] in labels:
                operand = dec2bin8(labels[line[1]], 0)
            else:
                operand = dec2bin8(int(line[1]), 0)
            machine_code.append(opcode + operand)

    if machine_code == []:
        print("kokot")
    return machine_code

def main(argv):
    if len(argv) < 2:
        print('Usage: python %s <filename>' % (argv[0]))
        exit()
    fp = open(argv[1], 'r')
    tokens = tokenize(fp)
    fp.close


    labels = pass1(tokens)
    machine_code = pass2(tokens, labels)

    return

if __name__ == "__main__":
    main(sys.argv)
