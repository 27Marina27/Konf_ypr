
## **Задание 1**

```
local groups = [std.format("ИКБО-%d-20", i) for i in std.range(1, 25)];

local students = [
    { age: 19, group: groups[3], name: "Иванов И.И." },
    { age: 18, group: groups[4], name: "Петров П.П." },
    { age: 18, group: groups[4], name: "Сидоров С.С." },
    { age: 20, group: groups[5], name: "Кузнецов К.К." }
];

{
  groups: groups,
  students: students,
  subject: "Конфигурационное управление"
}

```
## **Задание 2**
```
let Group = Text

let groups =
      [ "ИКБО-1-20"
      , "ИКБО-2-20"
      , "ИКБО-3-20"
      , "ИКБО-4-20"
      , "ИКБО-5-20"
      , "ИКБО-6-20"
      , "ИКБО-7-20"
      , "ИКБО-8-20"
      , "ИКБО-9-20"
      , "ИКБО-10-20"
      , "ИКБО-11-20"
      , "ИКБО-12-20"
      , "ИКБО-13-20"
      , "ИКБО-14-20"
      , "ИКБО-15-20"
      , "ИКБО-16-20"
      , "ИКБО-17-20"
      , "ИКБО-18-20"
      , "ИКБО-19-20"
      , "ИКБО-20-20"
      , "ИКБО-21-20"
      , "ИКБО-22-20"
      , "ИКБО-23-20"
      , "ИКБО-24-20"
      ]

let Student =
      { age : Natural, group : Group, name : Text }

let students =
      [ { age = 19, group = "ИКБО-4-20", name = "Иванов И.И." }
      , { age = 18, group = "ИКБО-5-20", name = "Петров П.П." }
      , { age = 18, group = "ИКБО-5-20", name = "Сидоров С.С." }
      , { age = 20, group = "ИКБО-10-20", name = "Новиков Н.Н." }
      ]

let data =
      { groups = groups, students = students, subject = "Конфигурационное управление" }

in  data
```
## **Задание 3/4/5**
```
import random

def parse_bnf(text):
    ''' Преобразовать текстовую запись БНФ в словарь. '''
    grammar = {}
    rules = [line.split('=') for line in text.strip().split('\n')]
    for name, body in rules:
        grammar[name.strip()] = [alt.split() for alt in body.split('|')]
    return grammar

def generate_phrase(grammar, start):
    ''' Сгенерировать случайную фразу. '''
    if start in grammar:
        seq = random.choice(grammar[start])
        return ''.join([generate_phrase(grammar, name) for name in seq])
    return str(start)

def main():
    #ЗАДАНИЕ 3
    choice = input("Нажмите 3 для вывода BNF: ")
    if choice == "3":
        BNF = '''E = 0 | 1'''
        print(BNF)
        for i in range(10):
            print(generate_phrase(parse_bnf(BNF), 'E'))
    #ЗАДАНИЕ 4
    choice = input("Нажмите 4 для вывода BNF: ")
    if choice == "4":
        BNF = '''E = E E | () | {}'''
        print(BNF)
        for i in range(10):
            print(generate_phrase(parse_bnf(BNF), 'E'))
    #ЗАДАНИЕ 5
    choice = input("Нажмите 5 для вывода BNF: ")
    if choice == "5":
        BNF = '''E = E & E | E | E | ( E ) | ~ E | x | y'''
        print(BNF)
        for i in range(10):
            print(generate_phrase(parse_bnf(BNF), 'E'))

if __name__ == "__main__":
    main()
```

