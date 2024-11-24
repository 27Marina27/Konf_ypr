import argparse
import subprocess
import os


def get_commits_with_parents(repo_path, file_name):
    try:
        cmd = ['git', '-C', repo_path, 'log', '--pretty=format:%H %P', '--', file_name]
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        commits_with_parents = []
        for line in result.stdout.splitlines():
            parts = line.split()
            commit_hash = parts[0]
            parents = parts[1:] if len(parts) > 1 else []
            commits_with_parents.append((commit_hash, parents))
        return commits_with_parents
    except subprocess.CalledProcessError as e:
        print(f"Error executing git command: {e}")
        print(f"Command output: {e.output}")
        return []


def build_dependency_graph(repo_path, file_name):
    commits_with_parents = get_commits_with_parents(repo_path, file_name)
    edges = []
    for commit, parents in commits_with_parents:
        for parent in parents:
            edges.append((commit, parent))
    return edges


def generate_mermaid_code(edges):
    mermaid_lines = ["graph TD"]
    for child, parent in edges:
        mermaid_lines.append(f"    {parent} --> {child}")
    return "\n".join(mermaid_lines)


def generate_png(mermaid_code, output_png):
    # Указываем полный путь к mmdc, если он не найден
    mmdc_path = r'C:\Users\marin\AppData\Roaming\npm\mmdc.cmd'  # Замените на ваш путь, если нужно
    temp_file = 'temp.mmd'

    # Сохраняем временный файл с мермейд кодом
    with open(temp_file, 'w') as f:
        f.write(mermaid_code)

    # Добавляем путь к mmdc в текущий процесс, если нужно
    os.environ['PATH'] += r';C:\Users\marin\AppData\Roaming\npm'

    # Генерируем PNG с использованием mmdc
    try:
        subprocess.run([mmdc_path, '-i', temp_file, '-o', output_png], check=True)
        print(f"PNG файл сохранен как {output_png}")
    except subprocess.CalledProcessError as e:
        print(f"Ошибка при генерации PNG: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate a dependency graph for git commits affecting a specific file.")
    parser.add_argument('repo_path', help="Path to the git repository.")
    parser.add_argument('output_file', help="Path to the output file for the generated Mermaid code.")
    parser.add_argument('output_png', help="Path to the output PNG file.")
    parser.add_argument('file_name', help="Name of the file to filter commits.")

    args = parser.parse_args()

    # Строим граф зависимости
    edges = build_dependency_graph(args.repo_path, args.file_name)
    mermaid_code = generate_mermaid_code(edges)

    # Сохраняем Mermaid код в файл
    with open(args.output_file, 'w') as f:
        f.write(mermaid_code)

    print(f"Mermaid код сохранен в {args.output_file}")

    # Генерируем PNG
    generate_png(mermaid_code, args.output_png)


if __name__ == "__main__":
    main()
