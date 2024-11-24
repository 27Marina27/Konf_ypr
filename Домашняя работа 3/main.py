import argparse
import xml.etree.ElementTree as ET
import re
import os

class ConfigConverter:
    def __init__(self):
        self.output = []

    def parse_file(self, file_input):
        try:
            # Если передан путь (str), открываем файл
            if isinstance(file_input, (str, bytes, os.PathLike)):
                with open(file_input, "r", encoding="utf-8") as file:
                    content = file.read()
            else:
                # Если передан StringIO, читаем его напрямую
                content = file_input.read()

            # Проверка на некорректные имена элементов
            invalid_name_match = re.search(r"<([^\s<>/]+)[^>]*>", content)
            if invalid_name_match:
                invalid_name = invalid_name_match.group(1)
                if not re.match(r"^[a-zA-Z_][\w.-]*$", invalid_name):
                    raise ValueError(f"Недопустимое имя элемента: {invalid_name}")

            # После проверки парсим содержимое
            tree = ET.ElementTree(ET.fromstring(content))
            root = tree.getroot()
            self.process_element(root)
        except ET.ParseError as e:
            raise ValueError(f"Ошибка парсинга XML: {e}")

    def process_element(self, element, depth=0):
        """Рекурсивно обрабатывает XML-элементы."""
        indent = "  " * depth
        name = element.tag
        if not re.match(r"^[a-zA-Z_][\w.-]*$", name):
            raise ValueError(f"Недопустимое имя элемента: {name}")

        if len(element) == 0:  # Листовой элемент
            value = element.text.strip() if element.text else ""
            if value.isdigit():
                self.output.append(f"{indent}{name} => {value},")
            else:
                self.output.append(f'{indent}{name} => "{value}",')
        else:  # Словарь
            self.output.append(f"{indent}{name}")
            self.output.append(f"{indent}[")
            for child in element:
                self.process_element(child, depth + 1)
            self.output.append(f"{indent}]")

    def add_comment(self, comment, multiline=False):
        """Добавляет комментарии в вывод."""
        if multiline:
            self.output.append(f"/+ {comment} +/")
        else:
            self.output.append(f"-- {comment}")

    def process_constant(self, expression, name, depth=0):
        """Объявляет константу: значение -> имя"""
        indent = "  " * depth
        self.output.append(f"{indent}{expression} -> {name}")

    def evaluate_expression(self, tokens):
        """Вычисление постфиксного выражения."""
        stack = []
        for token in tokens:
            if token.isdigit():
                stack.append(int(token))
            elif token == "+":
                if len(stack) < 2:
                    raise ValueError("Некорректное постфиксное выражение: недостаточно операндов для операции.")
                b, a = stack.pop(), stack.pop()
                stack.append(a + b)
            elif token == "-":
                if len(stack) < 2:
                    raise ValueError("Некорректное постфиксное выражение: недостаточно операндов для операции.")
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == "pow":
                if len(stack) < 2:
                    raise ValueError("Некорректное постфиксное выражение: недостаточно операндов для операции.")
                b, a = stack.pop(), stack.pop()
                stack.append(a ** b)
            elif token == "mod":
                if len(stack) < 2:
                    raise ValueError("Некорректное постфиксное выражение: недостаточно операндов для операции.")
                b, a = stack.pop(), stack.pop()
                stack.append(a % b)
            else:
                raise ValueError(f"Неизвестный токен: {token}")
        if len(stack) != 1:
            raise ValueError("Некорректное постфиксное выражение")
        return stack.pop()

    def convert(self):
        """Возвращает финальный вывод в формате учебного конфигурационного языка."""
        return "\n".join(self.output)


def main():
    parser = argparse.ArgumentParser(description="Инструмент учебного конфигурационного языка.")
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    # Подкоманда для конвертации XML
    xml_parser = subparsers.add_parser("convert", help="Конвертировать XML в учебный конфигурационный язык")
    xml_parser.add_argument("file", type=str, help="Путь к XML-файлу.")

    # Подкоманда для вычисления постфиксного выражения
    eval_parser = subparsers.add_parser("eval", help="Вычислить постфиксное выражение")
    eval_parser.add_argument("expression", type=str, help="Постфиксное выражение (через пробел).")
    eval_parser.add_argument("result_name", type=str, help="Имя переменной для результата.")

    args = parser.parse_args()

    converter = ConfigConverter()

    if args.command == "convert":
        # Режим преобразования XML
        try:
            converter.parse_file(args.file)
            print(converter.convert())
        except ValueError as e:
            print(f"Ошибка: {e}")

    elif args.command == "eval":
        # Режим вычисления выражения
        try:
            tokens = args.expression.split()
            result = converter.evaluate_expression(tokens)
            print(f"{args.result_name} = {result}")
        except ValueError as e:
            print(f"Ошибка: {e}")

    else:
        print("Ошибка: Укажите команду (convert или eval). Используйте -h для справки.")


if __name__ == "__main__":
    main()
