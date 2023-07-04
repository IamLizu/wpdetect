"""
    URL utility of wpdetect.
"""

import urllib.request
from urllib.parse import urlparse
from wpdetect.utils.print import print_verbose, print_checking_message


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

    print_verbose("[+] Going with HTTP.")

    url = add_scheme_to_url(url, "http")
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
