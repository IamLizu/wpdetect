"""
    Print utility of wpdetect.
"""

from pyfiglet import figlet_format
from wpdetect.cli_store import cli_options


def print_verbose(message):
    """Prints the message if verbose is true."""

    if len(message) == 0:
        raise ValueError("Invalid message. Please provide a valid message.")

    if cli_options['verbose']:
        print(message)


def print_checking_message(url):
    """Prints the message before checking the url."""

    if len(url) == 0:
        raise ValueError("Invalid url. Please provide a valid url.")

    print_verbose("\nChecking: " + str(url))


def print_logo(version):
    """
        Prints the logo with version number.
    """

    if len(version) == 0:
        raise ValueError(
            "Invalid version number. Please provide a valid version.")

    print(figlet_format('     wpdetect     '))
    print("=================== VERSION: " +
          version + " ===================\n")
