"""
    Module for testing wpdetect/utils/print.py
"""

import sys
import unittest
from io import StringIO
from pyfiglet import figlet_format
from wpdetect.utils.print import print_logo


class TestPrintMethods(unittest.TestCase):
    """
    Test class for testing print methods
    """

    def test_print_logo_with_version(self):
        """
        Test print_logo method with a version number
        """

        version = "1.4.10"
        expected_output = figlet_format('     wpdetect     ') + \
            "\n=================== VERSION: " + \
            version + " ===================\n\n"

        captured_output = StringIO()
        sys.stdout = captured_output

        print_logo(version)

        sys.stdout = sys.__stdout__

        printed_output = captured_output.getvalue()

        self.assertEqual(printed_output, expected_output)


if __name__ == '__main__':
    unittest.main()
