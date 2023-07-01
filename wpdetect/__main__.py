'''
name: wpdetect
description: A simple script to detect if a website is running WordPress.
'''

import sys
import urllib.request
import requests
import click
from pyfiglet import figlet_format

HEADER = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14" + \
    " (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"
VERSION = "1.4.1"

# Error messages
ERROR_UNABLE_TO_OPEN_URL = "Couldn't open url," + \
    " please make sure to type a valid and publicly accessible url.\n"

# List to store the found WordPress installations
wp_domains = []


def print_logo(version):
    """
        print_logo(version)
        Prints the logo with version number.
    """

    print(figlet_format('     wpdetect     '))
    print("=================== VERSION: " + version + " ===================\n")


def wp_check(url):
    """Checks if the given url is a WordPress installation."""

    wp_signature = urllib.request.Request(url, headers={'User-Agent': HEADER})

    try:
        with urllib.request.urlopen(wp_signature) as _:
            return True

    except urllib.error.HTTPError:
        pass

    return False


def check_protocol(url):
    """Checks if the url has a protocol specified, if not, it adds HTTP."""

    print("[!] No protocol specified.")
    url = "http://" + url
    print("[+] Going with HTTP.\n")
    print("Checking: " + str(url))

    return url


def check_redirect(url):
    """Checks if the url redirects to another url, if so, it follows the redirect."""

    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.head(url, allow_redirects=True,
                             headers=headers, timeout=5)
    redirected_url = response.url

    if url != redirected_url:
        print(f"[!] {url} redirected to {redirected_url}")
        # Recursively follow the redirect
        return check_redirect(redirected_url)

    return redirected_url


def check_http(url):
    """Instead of HTTPS, it tries to connect over HTTP."""

    print("[!] Couldn't connect over HTTPS.")
    print("[+] Trying with HTTP.\n")
    url = "http://" + url[8:]
    print("Checking: " + str(url))

    return url


def url_check(url, show_signature=False):
    """
        Checks if the url is valid and publicly accessible.
        If so, it runs wp_check on it.
    """

    print("\nChecking: " + str(url))
    try:
        if url[:4] != "http":
            url = check_protocol(url)

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
                url_to_print = wp_signature if show_signature else url

                print(f"[✓] WordPress found at: {url_to_print}")

                wp_domains.append(url)
            else:
                print(f"[✗] WordPress not found at: {url}")
            break

    except urllib.error.HTTPError as error:
        if error.code == 403:
            print("Got 403! Website seems to be behind a WAF.")

    except urllib.error.URLError:
        if url[:5] == "https":
            url = check_http(url)

            try:
                url_check(url)
            except urllib.error.URLError:
                print(ERROR_UNABLE_TO_OPEN_URL)
        else:
            print(ERROR_UNABLE_TO_OPEN_URL)
    except ValueError:
        print("Invalid url! Please type in correct url.\n")


def handle_file(filename, show_signature=False):
    """Opens the file and runs url_check for each line."""

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            domains = file.readlines()

            print("Targets,\n")

            for domain in domains:
                print(domain.strip())

            for domain in domains:
                url = domain.strip()
                url_check(url, show_signature)

    except FileNotFoundError:
        print("Please enter the file name correctly, file not found!\n")


@click.command(context_settings={"help_option_names": ['-h', '--help']})
@click.argument('url', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), help="File with list of URLs to check.")
@click.option('-v', '--version', is_flag=True, help="Print version.")
@click.option('-ss', '--show-signature', is_flag=True,
              help="Show by which signature WordPress is detected in a domain.")
def main(url, file, version, show_signature):
    """Detects if a website is running WordPress."""

    if version is False:
        print_logo(VERSION)

    if url:
        url_check(url, show_signature)

    if file:
        handle_file(file, show_signature)

    if version:
        print(f"Version: {VERSION}")

    if len(sys.argv) == 1:
        click.echo(click.get_current_context().get_help())


if __name__ == '__main__':
    main(None, None, None, None)
