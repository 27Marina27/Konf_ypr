import struct
import xml.etree.ElementTree as ET
import sys

COMMANDS = {
    'LOAD': 184,
    'READ': 229,
    'WRITE': 43,
    'MAX': 206,
}

def assemble(input_path, output_path, log_path):
    with open(input_path, 'r') as file:
        lines = file.readlines()

    binary_data = bytearray()
    root = ET.Element('log')

    for line in lines:
        parts = line.strip().split()

        if not parts:
            continue  # Пропускаем пустые строки

        command = parts[0]
        args = list(map(int, parts[1:]))
        
        if command not in COMMANDS:
            raise ValueError(f"Unknown command: {command}")

        opcode = COMMANDS[command]
        
        if command == 'LOAD':
            if len(args) != 2:
                raise ValueError(f"LOAD expects 2 arguments, got {len(args)}")
            b, c = args
            binary_data.extend(struct.pack('<BHI', opcode, b, c))
        elif command == 'READ':
            if len(args) != 2:
                raise ValueError(f"READ expects 2 arguments, got {len(args)}")
            b, c = args
            binary_data.extend(struct.pack('<BHH', opcode, b, c))
        elif command == 'WRITE':
            if len(args) != 3:
                raise ValueError(f"WRITE expects 3 arguments, got {len(args)}")
            b, c, d = args
            binary_data.extend(struct.pack('<BHHH', opcode, b, c, d))
        elif command == 'MAX':
            if len(args) != 3:
                raise ValueError(f"MAX expects 3 arguments, got {len(args)}")
            b, c, d = args
            binary_data.extend(struct.pack('<BHHH', opcode, b, c, d))

        # Add log entry
        log_entry = ET.SubElement(root, 'instruction', command=command)
        for i, arg in enumerate(args):
            log_entry.set(f'arg{i+1}', str(arg))

    # Save binary file
    with open(output_path, 'wb') as f:
        f.write(binary_data)

    # Save XML log
    tree = ET.ElementTree(root)
    tree.write(log_path)

if __name__ == '__main__':
    assemble(sys.argv[1], sys.argv[2], sys.argv[3])
