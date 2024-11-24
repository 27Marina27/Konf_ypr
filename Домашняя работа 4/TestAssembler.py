import unittest
import xml.etree.ElementTree as ET  # Добавлен импорт

from assemble import assemble

class TestAssemblerVector(unittest.TestCase):
    def test_vector_max(self):
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

        # Проверяем, что бинарный файл не пуст
        with open("test_output.bin", "rb") as f:
            data = f.read()
        self.assertGreater(len(data), 0)

        # Проверяем, что лог файл не пуст
        tree = ET.parse("test_log.xml")
        root = tree.getroot()
        self.assertGreater(len(root), 0)

if __name__ == "__main__":
    unittest.main()
