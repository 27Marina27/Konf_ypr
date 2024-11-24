import struct
import xml.etree.ElementTree as ET
import sys

def interpret(binary_path, memory_output_path, memory_range):
    with open(binary_path, 'rb') as f:
        binary_data = f.read()

    memory = [0] * 1024  # Example memory space
    pointer = 0

    while pointer < len(binary_data):
        opcode = binary_data[pointer]
        pointer += 1

        if opcode == 184:  # LOAD
            b, c = struct.unpack_from('<HI', binary_data, pointer)
            pointer += 6
            memory[b] = c
        elif opcode == 229:  # READ
            b, c = struct.unpack_from('<HH', binary_data, pointer)
            pointer += 4
            memory[c] = memory[b]
        elif opcode == 43:  # WRITE
            b, c, d = struct.unpack_from('<HHH', binary_data, pointer)
            pointer += 6
            memory[b + c] = memory[d]
        elif opcode == 206:  # MAX
            b, c, d = struct.unpack_from('<HHH', binary_data, pointer)
            pointer += 6
            memory[b] = max(memory[c], memory[d])
        else:
            raise ValueError(f"Unknown opcode: {opcode}")

    # Write memory to XML
    root = ET.Element('memory')
    for i in range(memory_range[0], memory_range[1]):
        entry = ET.SubElement(root, 'cell', index=str(i))
        entry.text = str(memory[i])

    tree = ET.ElementTree(root)
    tree.write(memory_output_path)

if __name__ == '__main__':
    memory_range = list(map(int, sys.argv[3].split(':')))
    interpret(sys.argv[1], sys.argv[2], memory_range)
