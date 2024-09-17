import re
import sys
"""
def tokenize(asm_code):
    lines = asm_code.strip().split('\n')
    tokens = []
    for line in lines:
        line_tokens = re.findall(r'\w+|\d+', line)
        tokens.extend(line_tokens)
    return tokens

def assemble(tokens):
    instructions = {
        'MOV': 0x01,
        'ADD': 0x02,
        'SUB': 0x03,
        'JMP': 0x04
    }
    registers = {
        'A': 0x10,
        'B': 0x11
    }
    machine_code = []
    i = 0
    while i < len(tokens):
        op = tokens[i]
        if op in instructions:
            machine_code.append(instructions[op])
            if op == 'MOV':
                reg = tokens[i + 1]
                value = int(tokens[i + 2])
                machine_code.append(registers[reg])
                machine_code.append(value)
                i += 3
            elif op in ['ADD', 'SUB']:
                reg1 = tokens[i + 1]
                reg2 = tokens[i + 2]
                machine_code.append(registers[reg1])
                machine_code.append(registers[reg2])
                i += 3
            elif op == 'JMP':
                address = int(tokens[i + 1])
                machine_code.append(address)
                i += 2
        else:
            raise ValueError(f"Unknown instruction: {op}")
    return machine_code

def save_to_binary(machine_code, filename):
    with open(filename, 'wb') as f:
        f.write(bytearray(machine_code))

def main():
    tokens = tokenize(asm_code)
    print("Tokens:", tokens)
    machine_code = assemble(tokens)
    print("Machine Code (Hex):", ' '.join(f'{byte:02X}' for byte in machine_code))
    save_to_binary(machine_code, 'output.bin')

if __name__ == "__main__":
    main()
"""

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
            l = d.bit_lenght()
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
    return tokens

def pass1(tokens):
    return

def pass2(tokens, labels):
    return
