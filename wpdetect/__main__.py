'''
name: wpdetect
description: A simple script to detect if a website is running WordPress.
'''

import sys
import urllib.request
from urllib.parse import urlparse
import click
from pyfiglet import figlet_format

HEADER = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14" + \
    " (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"
VERSION = "1.4.3"

# Error messages
ERROR_UNABLE_TO_OPEN_URL = "Couldn't open url," + \
    " please make sure to type a valid and publicly accessible url.\n"

# List to store the found WordPress installations
wp_domains = []


# cli options store
cli_options = {
    'verbose': True,  # default value
    'show_signature': False,  # default value
}


def print_verbose(message):
    """Prints the message if verbose is true."""

    if cli_options['verbose']:
        print(message)


def print_logo(version):
    """
        print_logo(version)
        Prints the logo with version number.
    """

    print_verbose(figlet_format('     wpdetect     '))
    print_verbose("=================== VERSION: " +
                  version + " ===================\n")


def print_checking_message(url):
    """Prints the message before checking the url."""

    print_verbose("\nChecking: " + str(url))


def wp_check(url):
    """Checks if the given url is a WordPress installation."""

    wp_signature = urllib.request.Request(url, headers={'User-Agent': HEADER})

    try:
        with urllib.request.urlopen(wp_signature) as _:
            return True

    except urllib.error.HTTPError:
        pass

    return False


def get_protocol(url):
    """Returns the protocol of the url."""

    parsed_url = urlparse(url)
    return parsed_url.scheme if parsed_url.scheme else None


def add_scheme_to_url(url, scheme):
    """Adds the scheme to the url."""

    parsed_url = urlparse(url)
    updated_url = parsed_url._replace(scheme=scheme)

    return updated_url.scheme + "://" + updated_url.netloc + updated_url.path


def add_http(url):
    """Checks if the url has a protocol specified, if not, it adds HTTP."""

    print_verbose("[!] No protocol specified.")
    print_verbose("[+] Going with HTTP.")

    url = add_scheme_to_url(url, "http")

    print_checking_message(url)

    return url


def get_redirected_url(url):
    """Returns the redirected url."""

    opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
    response = opener.open(url)
    redirected_url = response.url

    return redirected_url


def check_redirect(url):
    """Checks if the url redirects to another url, if so, it follows the redirect."""

    redirected_url = get_redirected_url(url)

    if url != redirected_url:
        print_verbose(f"[!] {url} redirected to {redirected_url}")
        # Recursively follow the redirect
        print_checking_message(redirected_url)

        return check_redirect(redirected_url)

    return redirected_url


def check_http(url):
    """Instead of HTTPS, it tries to connect over HTTP."""

    print_verbose("[!] Couldn't connect over HTTPS.")
    print_verbose("[+] Trying with HTTP.")

    url = add_scheme_to_url(url, "http")

    return url


def url_check(url):
    """
        Checks if the url is valid and publicly accessible.
        If so, it runs wp_check on it.
    """

    print_checking_message(url)

    try:
        if get_protocol(url) is None:
            url = add_http(url)  # add http if no protocol specified

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

        # run wp_check for each url in wp_signatures
        for wp_signature in wp_signatures.values():
            result = wp_check(wp_signature)

            if result:
                url_to_print = wp_signature if cli_options["show_signature"] else url

                print_verbose(f"[✓] WordPress found at: {url_to_print}")

                wp_domains.append(url_to_print)
            else:
                print_verbose(f"[✗] WordPress not found at: {url}")
            break

    except urllib.error.HTTPError as error:
        if error.code == 403:
            print_verbose("Got 403! Website seems to be behind a WAF.")

    except urllib.error.URLError:
        if get_protocol(url) == "https":
            url = check_http(url)

            try:
                url_check(url)
            except urllib.error.URLError:
                print_verbose(ERROR_UNABLE_TO_OPEN_URL)
        else:
            print_verbose(ERROR_UNABLE_TO_OPEN_URL)
    except ValueError:
        print_verbose("Invalid url! Please type in correct url.\n")


def handle_file(filename):
    """Opens the file and runs url_check for each line."""

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            domains = file.readlines()

            print_verbose("Targets,\n")

            for domain in domains:
                print_verbose(domain.strip())

            for domain in domains:
                url = domain.strip()
                url_check(url)

    except FileNotFoundError:
        print("Please enter the file name correctly, file not found!\n")


def print_domains():
    """Prints the found WordPress installations."""

    if cli_options['verbose'] is False:
        for wp_domain in wp_domains:
            print(wp_domain)


def full_scan(url):
    """Scans the HTTP & HTTPS of the website for WordPress."""

    print_verbose("Full scan initiated.\n")

    print_verbose("[1] Scanning HTTP...")
    url = add_scheme_to_url(url, "http")
    url_check(url)

    print_verbose("\n[2] Scanning HTTPS...")
    url = add_scheme_to_url(url, "https")
    url_check(url)


@click.command(context_settings={"help_option_names": ['-h', '--help']})
@click.argument('url', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), help="File with list of URLs to check.")
@click.option('-v', '--version', is_flag=True, help="Print version.")
@click.option('-ss', '--show-signature', is_flag=True,
              help="Show by which signature WordPress is detected in a domain.")
@click.option('-q', '--quiet', is_flag=True, help="Only print the detected domains.")
@click.option('-sf', '--scan-full', is_flag=True,
              help="Scan HTTP & HTTPS of the website for WordPress.")
def main(url=None, file=None, version=None, show_signature=None, quiet=None, scan_full=None):
    """Detects if a website is running WordPress."""

    if quiet:
        cli_options['verbose'] = False

    if show_signature:
        cli_options['show_signature'] = True

    if version is False:
        print_logo(VERSION)

    if url:
        if scan_full:
            full_scan(url)
        else:
            url_check(url)

    if file:
        handle_file(file)

    if version:
        print(f"Version: {VERSION}")

    if len(sys.argv) == 1:
        click.echo(click.get_current_context().get_help())

    # print wp_domains if verbose is true
    print_domains()


if __name__ == '__main__':
    main()
