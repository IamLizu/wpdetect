"""
    Module for testing wpdetect/utils/print.py
"""

import sys
import unittest
from unittest.mock import patch
from io import StringIO
from pyfiglet import figlet_format
from wpdetect.utils.print import (
    print_logo, print_checking_message, print_verbose)


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

    def test_print_logo_without_version(self):
        """
        Test print_logo method without a version number, should raise ValueError
        """

        version = ""
        expected_output = "Invalid version number. Please provide a valid version."

        captured_output = StringIO()
        sys.stdout = captured_output

        with self.assertRaises(ValueError) as context:
            print_logo(version)

        sys.stdout = sys.__stdout__

        printed_output = captured_output.getvalue()

        self.assertEqual(str(context.exception), expected_output)
        self.assertEqual(printed_output, "")

    def test_print_checking_message_with_url(self):
        """
        Test print_checking_message method with a url
        """

        url = "https://www.example.com"
        expected_output = "\nChecking: " + str(url) + "\n"

        captured_output = StringIO()
        sys.stdout = captured_output

        print_checking_message(url)

        sys.stdout = sys.__stdout__

        printed_output = captured_output.getvalue()

        self.assertEqual(printed_output, expected_output)

    def test_print_checking_message_without_url(self):
        """
        Test print_checking_message method without a url, should raise ValueError
        """

        url = ""
        expected_output = "Invalid url. Please provide a valid url."

        captured_output = StringIO()
        sys.stdout = captured_output

        with self.assertRaises(ValueError) as context:
            print_checking_message(url)

        sys.stdout = sys.__stdout__

        printed_output = captured_output.getvalue()

        self.assertEqual(str(context.exception), expected_output)
        self.assertEqual(printed_output, "")

    def test_print_verbose_with_message_and_verbose_enabled(self):
        """
        Test print_verbose method with a message while verbose is enabled
        """
        with patch('wpdetect.utils.print.cli_options', {'verbose': True}):
            message = "Test message"
            expected_output = message + "\n"

            captured_output = StringIO()
            sys.stdout = captured_output

            print_verbose(message)

            sys.stdout = sys.__stdout__

            printed_output = captured_output.getvalue()
            self.assertEqual(printed_output, expected_output)

    def test_print_verbose_with_message_and_verbose_disabled(self):
        """
        Test print_verbose method with a message while verbose is disabled
        """
        with patch('wpdetect.utils.print.cli_options', {'verbose': False}):
            message = "Test message"
            expected_output = ""

            captured_output = StringIO()
            sys.stdout = captured_output

            print_verbose(message)

            sys.stdout = sys.__stdout__

            printed_output = captured_output.getvalue()
            self.assertEqual(printed_output, expected_output)

    def test_print_verbose_without_message(self):
        """
        Test print_verbose method without a message, should raise ValueError
        """

        message = ""
        expected_output = "Invalid message. Please provide a valid message."

        captured_output = StringIO()
        sys.stdout = captured_output

        with self.assertRaises(ValueError) as context:
            print_verbose(message)

        sys.stdout = sys.__stdout__

        printed_output = captured_output.getvalue()

        self.assertEqual(str(context.exception), expected_output)
        self.assertEqual(printed_output, "")


TestPrintMethods.__doc__ = "Test class for testing print methods"
print(TestPrintMethods.__doc__)

if __name__ == '__main__':
    unittest.main()
