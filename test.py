"""
This file contains test coverage for the tool
"""
from typing import List
import publisher
import unittest
PRINT = 0
PRINT_HELP = 1
WRITE = 2
READ = 3
log = []
publisher.log = lambda x: log.append([PRINT, x])
publisher.print_help = lambda: log.append([PRINT_HELP])
publisher.list_dir = lambda x: folders[x] if x in folders else []
publisher.read_file = lambda x: [log.append([READ, x]), ''][1]
publisher.write_file = lambda x, y: log.append([WRITE, x, y])
publisher.is_dir = lambda x: x in folders

folders = {
    'project1': ['test', 'one.md', 'two.md', 'three.md'],
    'project1/test': ['four.md', 'five.html'],
    'project2': ['project2.md'],
    '.': ['one.md', 'test'],
    './test': ['two.md']
}

def convert(args: List[str]) -> int:
    """
    This function mocks the tool being run from the terminal
    """
    log.clear()
    return publisher.main(args)

class PublisherTest(unittest.TestCase):
    def log(self, length: int):
        self.assertEqual(len(log), length)

    def action(self, index: int, type: int):
        self.assertEqual(log[index][0], type)

    def outcome(self, args: List[str], success: bool):
        args.insert(0, '')
        self.assertEqual(convert(args), 0 if success else 1)

    def printed(self, index: int, msg: str = None):
        self.assertEqual(log[index][0], PRINT)
        if msg:
            self.assertEqual(log[index][1], msg)

    def read(self, index: int, path: str = None):
        self.assertEqual(log[index][0], READ)
        if path:
            self.assertEqual(log[index][1], path)

    def wrote(self, index: int, path: str = None):
        self.assertEqual(log[index][0], WRITE)
        if path:
            self.assertEqual(log[index][1], path)

    def convert(self, index: int, src: str, dst: str):
        self.read(index, src)
        self.printed(index + 1, f'Converted {src} -> {dst}')
        self.wrote(index + 2, dst)

class TestArgs(PublisherTest):
    """
    Tests for provided tool arguments
    """

    def testZeroArgs(self):
        """
        Test for when none of the required arguments are provided
        """
        self.outcome([], False)
        self.log(1)
        self.action(0, PRINT_HELP)

    def testOneArg(self):
        """
        Test for when only one required argument is provided
        """
        self.outcome(['src'], False)
        self.log(1)
        self.action(0, PRINT_HELP)

    def testTwoArgs(self):
        """
        Test for when all required arguments are provided
        """
        self.outcome(['src', 'dst'], True)
        self.log(3)
        self.printed(0, 'Found 0 markdown files to convert')
        self.action(1, READ)
        self.action(2, READ)

# TestStyle
# Test builtin style
# Test provided style file
# Test error with nonexistent style file

# TestProject
class TestProject(PublisherTest):
    def testRecursiveFolder(self):
        self.outcome(['project1', 'output'], True)
        self.log(15)
        self.printed(0, 'Found 4 markdown files to convert')
        self.action(1, READ)
        self.action(2, READ)
        self.convert(3, 'project1/one.md', 'output/one.html')
        self.convert(6, 'project1/two.md', 'output/two.html')
        self.convert(9, 'project1/three.md', 'output/three.html')
        self.convert(12, 'project1/test/four.md', 'output/test/four.html')

    def testRepeatName(self):
        self.outcome(['project2', 'output'], True)
        self.log(6)
        self.printed(0, 'Found 1 markdown file to convert')
        self.action(1, READ)
        self.action(2, READ)
        self.convert(3, 'project2/project2.md', 'output/project2.html')

    def testDotToDot(self):
        self.outcome(['.', '.'], True)
        self.log(9)
        self.printed(0, 'Found 2 markdown files to convert')
        self.action(1, READ)
        self.action(2, READ)
        self.convert(3, './one.md', './one.html')
        self.convert(6, './test/two.md', './test/two.html')

if __name__ == '__main__':
    unittest.main()
