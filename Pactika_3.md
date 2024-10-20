
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
## **Задание 3**
## **Задание 4**
## **Задание 5**
