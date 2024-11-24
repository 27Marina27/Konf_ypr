import unittest
from unittest.mock import patch
from dependency_graph import get_commits_with_parents, build_dependency_graph, generate_mermaid_code


class TestGitDependencyGraph(unittest.TestCase):

    @patch('subprocess.run')
    def test_get_commits_with_parents(self, mock_run):
        mock_run.return_value.stdout = "abc123 def456 ghi789\njkl012"
        mock_run.return_value.returncode = 0

        result = get_commits_with_parents(
            r'C:\Users\marin\PycharmProjects\testRep\test', 'test.txt')

        expected_result = [
            ('abc123', ['def456', 'ghi789']),
            ('jkl012', [])
        ]
        self.assertEqual(result, expected_result)
        mock_run.assert_called_once_with(
            ['git', '-C', r'C:\Users\marin\PycharmProjects\testRep\test',
             'log', '--pretty=format:%H %P', '--', 'test.txt'],
            capture_output=True,
            text=True,
            check=True
        )

    @patch('subprocess.run')
    def test_build_dependency_graph(self, mock_run):

        mock_run.return_value.stdout = "abc123 def456 ghi789\njkl012"
        mock_run.return_value.returncode = 0

        result = build_dependency_graph(
            r'C:\Users\marin\PycharmProjects\testRep\test', 'test.txt')

        expected_result = [
            ('abc123', 'def456'),
            ('abc123', 'ghi789')
        ]
        self.assertEqual(result, expected_result)

        mock_run.assert_called_once_with(
            ['git', '-C', r'C:\Users\marin\PycharmProjects\testRep\test',
             'log', '--pretty=format:%H %P', '--', 'test.txt'],
            capture_output=True,
            text=True,
            check=True
        )

    def test_generate_mermaid_code(self):
        edges = [('abc123', 'def456'), ('abc123', 'ghi789')]
        result = generate_mermaid_code(edges)

        expected_result = (
            "graph TD\n"
            "    def456 --> abc123\n"
            "    ghi789 --> abc123"
        )
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()