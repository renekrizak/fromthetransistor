
def tokenize(asm_code):
    lines = asm_code.strip().split('')
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
