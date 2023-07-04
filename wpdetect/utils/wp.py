"""
    WordPress scanning utility of wpdetect.
"""

import urllib.request
from wpdetect.constants import HEADER, ERROR_UNABLE_TO_OPEN_URL, ERROR_UNABLE_TO_OPEN_FILE
from wpdetect.cli_store import cli_options
from wpdetect.utils.print import print_verbose, print_checking_message
from wpdetect.utils.url import get_protocol, add_scheme_to_url, add_http, check_redirect


# List to store the found WordPress installations
detected_domains = []


def is_wp(url):
    """Checks if the given url is a WordPress installation."""

    wp_signature = urllib.request.Request(url, headers={'User-Agent': HEADER})

    try:
        with urllib.request.urlopen(wp_signature) as _:
            return True
    except urllib.error.HTTPError:
        pass

    return False


def handle_url(url):
    """
        Checks if the url is valid and publicly accessible.
        If so, it runs is_wp on it.
    """

    print_checking_message(url)

    try:
        if get_protocol(url) is None:
            print_verbose("[!] No protocol specified.")
            url = add_http(url)

        url = check_redirect(url)

        wp_signatures = {
            1: url + "/wp-login.php",
            2: url + "/wp-content/",
            3: url + "/wp-admin/",
            4: url + "/wp-cron.php",
            5: url + "/xmlrpc.php",
            6: url + "/wp-json/wp/v2/",
            7: url + "/wp-content/themes/",
        }

        # Run is_wp for each url in wp_signatures
        for wp_signature in wp_signatures.values():

            result = is_wp(wp_signature)

            if result:
                url_to_print = wp_signature if cli_options["show_signature"] else url

                print_verbose(f"[✓] WordPress found at: {url_to_print}")

                detected_domains.append(url_to_print)
            else:
                print_verbose(f"[✗] WordPress not found at: {url}")
            break

    except urllib.error.HTTPError as error:
        if error.code == 403:
            print_verbose("Got 403! Website seems to be behind a WAF.")

    except urllib.error.URLError:
        if get_protocol(url) == "https":
            print_verbose("[!] Couldn't connect over HTTPS.")

            url = add_http(url)

            try:
                handle_url(url)

            except urllib.error.URLError:
                print_verbose(ERROR_UNABLE_TO_OPEN_URL)

        else:
            print_verbose(ERROR_UNABLE_TO_OPEN_URL)

    except ValueError:
        print_verbose("Invalid URL! Please type in the correct URL.\n")


def handle_file(filename):
    """Opens the file and runs handle_url for each line."""

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            domains = file.readlines()

            print_verbose("Targets,\n")

            for domain in domains:
                print_verbose(domain.strip())

            for domain in domains:
                url = domain.strip()
                if cli_options['scan_full']:
                    full_scan(url)
                else:
                    handle_url(url)

    except FileNotFoundError:
        print(ERROR_UNABLE_TO_OPEN_FILE)


def list_detected_domains():
    """Prints the found WordPress installations."""

    if cli_options['verbose'] is False:
        for wp_domain in detected_domains:
            print(wp_domain)


def full_scan(url):
    """Scans the HTTP & HTTPS of the website for WordPress."""

    print_verbose(f"\nFull scan initiated for {url}\n")
    print_verbose("[1] Scanning HTTP...")

    url = add_scheme_to_url(url, "http")
    handle_url(url)

    print_verbose("\n[2] Scanning HTTPS...")

    url = add_scheme_to_url(url, "https")
    handle_url(url)
