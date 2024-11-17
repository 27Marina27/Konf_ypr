import unittest
from shell import Shell
from vfs import VFS

class TestShell(unittest.TestCase):
    def setUp(self):
        config = {
            'user': 'user1',
            'host': 'localhost',
            'vfs_path': 'test.zip'
        }
        self.shell = Shell(config)

    def test_ls(self):
        # Test ls in root directory
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('test', result)
        self.assertIn('test2', result)
        self.assertIn('test3', result)

        # Test ls in a specific directory
        self.shell.cd('test')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('bbb.txt', result)

        self.shell.cd('..')
        self.shell.cd('test2')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('eee.txt', result)
        self.assertIn('qqq.txt', result)

        self.shell.cd('..')
        self.shell.cd('test3')
        result = self.shell.ls()
        self.assertIsInstance(result, str)
        self.assertIn('ddd.txt', result)
        self.assertIn('fff.txt', result)

        # Test ls with an empty directory (optional, if needed)

    def test_cd(self):
        # Test cd to existing directory
        result = self.shell.cd('test')
        self.assertIn('Changed directory to', result)

        # Test cd to non-existing directory
        result = self.shell.cd('non_existing_directory')
        self.assertIn('cd: no such directory', result)

        # Test cd to parent directory
        self.shell.cd('test')
        result = self.shell.cd('..')
        self.assertIn('Changed directory to', result)

    def test_who(self):
        # Test who returns string
        result = self.shell.who()
        self.assertIsInstance(result, str)

        # Проверка, что результат содержит имя пользователя
        self.assertIn(self.shell.config['user1'], result)

        # Проверка для локали
        self.shell.config['host'] = 'remote_host'
        result = self.shell.who()
        self.assertIn('remote_host', result)


if __name__ == '__main__':
    unittest.main()
