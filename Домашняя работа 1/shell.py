import datetime
import os
import subprocess
from vfs import VFS

class Shell:
    def __init__(self, config):
        self.config = config
        self.vfs = VFS(config['vfs_path'])
        self.current_path = '/'

    def execute(self, command):
        parts = command.strip().split()
        if not parts:
            return ''

        cmd = parts[0]
        args = parts[1:]

        if cmd == 'ls':
            return self.ls()
        elif cmd == 'cd':
            return self.cd(args[0]) if args else 'cd: missing argument'
        elif cmd == 'exit':
            return self.exit()
        elif cmd == 'date':
            return self.date()
        elif cmd == 'wc':
            return self.wc(args[0]) if args else 'wc: missing file'
        elif cmd == 'who':
            return self.who()
        else:
            return f"Unknown command: {cmd}"

    def ls(self):
        try:
            contents = self.vfs.list_dir(self.current_path)
            if contents:
                return '\n'.join(contents)
            return 'Empty directory'
        except Exception as e:
            return f"ls: error listing directory: {str(e)}"

    def cd(self, path):
        try:
            if path == '..':  # Переход на уровень выше
                new_path = os.path.dirname(self.current_path.rstrip('/'))
                self.current_path = new_path if new_path else '/'
            else:
                new_path = os.path.join(self.current_path, path).replace('\\', '/')
                if self.vfs.directory_exists(new_path):
                    self.current_path = new_path
                else:
                    return f"cd: no such directory: {path}"
            return f"Changed directory to {self.current_path}"
        except Exception as e:
            return f"cd: error changing directory: {str(e)}"

    def exit(self):
        self.vfs.close()
        return "Exiting..."

    def date(self):
        return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def wc(self, filename):
        try:
            content = self.vfs.read_file(filename)
            lines = content.splitlines()
            words = content.split()
            characters = len(content)
            return f"{len(lines)} {len(words)} {characters} {filename}"
        except KeyError:
            return f"wc: file '{filename}' not found"
        except Exception as e:
            return f"wc: error processing file '{filename}': {str(e)}"

    def who(self):
        try:
            return subprocess.getoutput("who")
        except Exception as e:
            return f"who: error executing command: {str(e)}"
