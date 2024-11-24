import unittest
import xml.etree.ElementTree as ET  # Добавлен импорт

from interpret import interpret

class TestInterpretVector(unittest.TestCase):
    def test_vector_max(self):
        # Выполняем интерпретацию
        interpret("test_output.bin", "memory.xml", (10, 16))

        # Проверяем результат интерпретации
        tree = ET.parse("memory.xml")
        root = tree.getroot()
        memory = {int(cell.attrib['index']): int(cell.text) for cell in root}
        for addr in range(10, 16):
            self.assertEqual(memory[addr], 148)  # Все результаты должны быть 148

if __name__ == "__main__":
    unittest.main()
