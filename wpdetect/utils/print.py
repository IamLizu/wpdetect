"""
    Print utility of wpdetect.
"""

from pyfiglet import figlet_format
from wpdetect.cli_store import cli_options


def print_verbose(message):
    """Prints the message if verbose is true."""

    if cli_options['verbose']:
        print(message)


def print_checking_message(url):
    """Prints the message before checking the url."""

    print_verbose("\nChecking: " + str(url))


def print_logo(version):
    """
        Prints the logo with version number.
    """

    print_verbose(figlet_format('     wpdetect     '))
    print_verbose("=================== VERSION: " +
                  version + " ===================\n")
