import unittest
import xml.etree.ElementTree as ET  # Добавлен импорт

from interpret import interpret
from assemble import assemble

class TestFullPipeline(unittest.TestCase):
    def test_full_pipeline(self):
        # Исходная программа
        input_program = """
        LOAD 0 10
        LOAD 1 25
        LOAD 2 70
        LOAD 3 90
        LOAD 4 5
        LOAD 5 30
        LOAD 6 148
        MAX 10 0 6
        MAX 11 1 6
        MAX 12 2 6
        MAX 13 3 6
        MAX 14 4 6
        MAX 15 5 6
        """
        with open("test_program.txt", "w") as f:
            f.write(input_program)

        # Выполняем ассемблирование
        assemble("test_program.txt", "test_output.bin", "test_log.xml")

        # Выполняем интерпретацию
        interpret("test_output.bin", "memory.xml", (10, 16))

        # Проверяем результат
        tree = ET.parse("memory.xml")
        root = tree.getroot()
        memory = {int(cell.attrib['index']): int(cell.text) for cell in root}
        for addr in range(10, 16):
            self.assertEqual(memory[addr], 148)  # Все результаты должны быть 148

if __name__ == "__main__":
    unittest.main()
