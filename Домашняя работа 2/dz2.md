# **Вариатн 31**
Разработать инструмент командной строки для визуализации графа
зависимостей, включая транзитивные зависимости. Сторонние средства для
получения зависимостей использовать нельзя.

Зависимости определяются для git-репозитория. Для описания графа
зависимостей используется представление Mermaid. Визуализатор должен
выводить результат на экран в виде кода.

Построить граф зависимостей для коммитов, в узлах которого содержатся
хеш-значения. Граф необходимо строить только для тех коммитов, где фигурирует
файл с заданным именем.

Ключами командной строки задаются:
* Путь к программе для визуализации графов.
* Путь к анализируемому репозиторию.
* Путь к файлу-результату в виде кода.
* Файл с заданным именем в репозитории.

Все функции визуализатора зависимостей должны быть покрыты тестами.

# **Пример**
![1](https://github.com/27Marina27/Konf_ypr/blob/main/конф.управление/photo_2024-11-24_13-53-39.jpg)
![2](https://github.com/27Marina27/Konf_ypr/blob/main/конф.управление/output.png)
# **Тесты**
![3](https://github.com/27Marina27/Konf_ypr/blob/main/конф.управление/photo_2024-11-24_13-58-10.jpg)
