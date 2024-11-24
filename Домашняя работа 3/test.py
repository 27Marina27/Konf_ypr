import unittest





from io import StringIO
from main import ConfigConverter


class TestConfigConverter(unittest.TestCase):
    def setUp(self):
        self.converter = ConfigConverter()

    def test_parse_file_valid_xml(self):
        valid_xml = "<root><child>123</child></root>"
        self.converter.parse_file(StringIO(valid_xml))
        expected_output = "root\n[\n  child => 123,\n]"
        self.assertEqual(self.converter.convert(), expected_output)

    def test_parse_file_invalid_xml(self):
        invalid_xml = "<root><child>123</root>"
        with self.assertRaises(ValueError) as context:
            self.converter.parse_file(StringIO(invalid_xml))
        self.assertIn("Ошибка парсинга XML", str(context.exception))

    def test_parse_file_invalid_element_name(self):
        invalid_name_xml = "<1invalid><child>123</child></1invalid>"
        with self.assertRaises(ValueError) as context:
            self.converter.parse_file(StringIO(invalid_name_xml))
        self.assertIn("Недопустимое имя элемента", str(context.exception))

    def test_process_element_nested(self):
        nested_xml = "<root><level1><level2>value</level2></level1></root>"
        self.converter.parse_file(StringIO(nested_xml))
        expected_output = "root\n[\n  level1\n  [\n    level2 => \"value\",\n  ]\n]"
        self.assertEqual(self.converter.convert(), expected_output)

    def test_add_comment_single_line(self):
        self.converter.add_comment("This is a comment")
        expected_output = "-- This is a comment"
        self.assertEqual(self.converter.convert(), expected_output)

    def test_add_comment_multiline(self):
        self.converter.add_comment("This is a multiline comment", multiline=True)
        expected_output = "/+ This is a multiline comment +/"
        self.assertEqual(self.converter.convert(), expected_output)

    def test_process_constant(self):
        self.converter.process_constant("123", "MY_CONSTANT")
        expected_output = "123 -> MY_CONSTANT"
        self.assertEqual(self.converter.convert(), expected_output)

    def test_evaluate_expression_valid(self):
        tokens = ["3", "4", "+", "2", "pow"]
        result = self.converter.evaluate_expression(tokens)
        self.assertEqual(result, 49)

    def test_evaluate_expression_invalid(self):
        tokens = ["3", "+"]
        with self.assertRaises(ValueError) as context:
            self.converter.evaluate_expression(tokens)
        self.assertIn("Некорректное постфиксное выражение", str(context.exception))

    def test_convert_output(self):
        xml = "<root><child>123</child></root>"
        self.converter.parse_file(StringIO(xml))
        output = self.converter.convert()
        self.assertEqual(output, "root\n[\n  child => 123,\n]")


if __name__ == "__main__":
    unittest.main()
