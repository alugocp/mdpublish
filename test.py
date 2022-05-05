"""
This file contains test coverage for the tool
"""
from typing import List
import publisher
import unittest
log = []
publisher.log = log.append

def convert(args: List[str]) -> int:
    """
    This function mocks the tool being run from the terminal
    """
    log.clear()
    return publisher.main(args)

class TestArgs(unittest.TestCase):
    """
    Tests for provided tool arguments
    """

    def testZeroArgs(self):
        """
        Test for when none of the required arguments are provided
        """
        self.assertEqual(convert(['python']), 1)
        self.assertEqual(len(log), 2)
        self.assertEqual(log[0], 'Usage: tool <src> <dst> [stylesheet]')
        self.assertEqual(log[1], '  src and dst should be project paths')

    def testOneArg(self):
        """
        Test for when only one required argument is provided
        """
        self.assertEqual(convert(['python', 'src']), 1)
        self.assertEqual(len(log), 2)
        self.assertEqual(log[0], 'Usage: tool <src> <dst> [stylesheet]')
        self.assertEqual(log[1], '  src and dst should be project paths')

    def testTwoArgs(self):
        """
        Test for when all required arguments are provided
        """
        self.assertEqual(convert(['python', 'src', 'dst']), 0)
        self.assertEqual(len(log), 1)
        self.assertEqual(log[0], 'Found 0 markdown files to convert')

# TestStyle
# Test builtin style
# Test provided style file
# Test error with nonexistent style file

# TestProject
# Test recursive folders
# Test tool where src is same name as a file (make sure the file name is unchanged)
# Test tool from . to .

if __name__ == '__main__':
    unittest.main()
