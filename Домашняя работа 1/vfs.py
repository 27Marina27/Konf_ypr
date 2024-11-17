import zipfile

class VFS:
    def __init__(self, zip_path):
        self.zip_file = zipfile.ZipFile(zip_path, 'r')
        self.current_path = '/'

    def list_dir(self, path):
        try:
            all_files = self.zip_file.namelist()  # Получаем список всех файлов в архиве
            normalized_path = path.lstrip('/')  # Убираем начальный "/"

            if normalized_path and not normalized_path.endswith('/'):
                normalized_path += '/'  # Убедимся, что путь заканчивается "/"

            contents = set()
            for file in all_files:
                if file.startswith(normalized_path):  # Проверяем, лежит ли файл в каталоге
                    relative_path = file[len(normalized_path):].lstrip('/')
                    first_part = relative_path.split('/')[0]
                    if first_part:
                        contents.add(first_part)  # Добавляем уникальные файлы/папки в результат

            return sorted(contents)
        except Exception as e:
            raise Exception(f"Error reading directory '{path}': {str(e)}")

    def list_files(self, path):
        return [file for file in self.zip_file.namelist() if file.startswith(path)]

    def read_file(self, path):
        try:
            with self.zip_file.open(path) as f:
                return f.read().decode('utf-8')
        except KeyError:
            raise KeyError(f"There is no file named '{path}' in the archive")
        except Exception as e:
            raise Exception(f"Error reading file '{path}': {str(e)}")

    def directory_exists(self, path):
        normalized_path = path.lstrip('/')
        if not normalized_path.endswith('/'):
            normalized_path += '/'
        return any(file.startswith(normalized_path) for file in self.zip_file.namelist())

    def close(self):
        self.zip_file.close()
