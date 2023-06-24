import urllib.request
import requests
import sys
from pyfiglet import figlet_format

header = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"
version = "1.3.8"
wp_domains = []


def print_logo():
    print(figlet_format('     wpdetect     '))
    print("=================== version: " + version + " ===================\n")


def wp_check(url):
    wp_signature = urllib.request.Request(url, headers={'User-Agent': header})

    try:
        if urllib.request.urlopen(wp_signature):
            return True

    except urllib.error.HTTPError:
        pass


def check_protocol(url):
    print("[!] No protocol specified.")
    url = "http://" + url
    print("[+] Going with HTTP.\n")
    print("Checking: " + str(url))

    return url


def check_redirect(url):
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.head(url, allow_redirects=True, headers=headers)
    redirected_url = response.url

    if url != redirected_url:
        print("[!] {} redirected to {}".format(url, redirected_url))
        # Recursively follow the redirect
        return check_redirect(redirected_url)
    else:
        return redirected_url


def check_HTTP(url):
    print("[!] Couldn't connect over HTTPS.")
    print("[+] Trying with HTTP.\n")
    url = "http://" + url[8:]
    print("Checking: " + str(url))

    return url


def url_check(url, isBatch=False):
    print("Checking: " + str(url))
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
        for wp_signature in wp_signatures:
            result = wp_check(wp_signatures[wp_signature])

            if result:
                print("[✓] WordPress found at: " + url)
                wp_domains.append(url)
                break

        if len(wp_domains) == 0 and isBatch == False:
            print("[X] No WordPress installation found!")

    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("Got 403! Website seems to be behind a WAF.")

    except urllib.error.URLError:
        if url[:5] == "https":
            url = check_HTTP(url)

            try:
                url_check(url)
            except urllib.error.URLError:
                print(
                    "Couldn't open url, please make sure to type a valid and publicly accessible url.\n")
        else:
            print(
                "Couldn't open url, please make sure to type a valid and publicly accessible url.\n")
    except ValueError:
        print("Invalid url! Please type in correct url.\n")


def usage():
    print("\nSyntax: wpdetect <website-url>")
    print("Example: wpdetect https://wordpress.org/")
    print("or supply a list with '-f' flag")
    print("Example: wpdetect -f domainlist.txt\n")


def handle_file(filename):
    try:
        file = open(filename, 'r')
        domains = file.readlines()

        print("Targets,\n")

        for domain in domains:
            print(domain.strip())
        print("\n")

        for domain in domains:
            url = domain.strip()
            url_check(url, isBatch=True)

    except FileNotFoundError:
        print("Please enter the file name correctly, file not found!\n")


arguments = {
    '-h': usage,
    '--help': usage,
    '-v': lambda: print(version),
    '--version': lambda: print(version),
    '-f':  handle_file,
    '--file': handle_file
}


def main():
    print_logo()

    try:
        if len(sys.argv) > 1:
            argument = sys.argv[1]

            # Check if the argument exists in the dictionary
            if argument in arguments:
                # Execute the corresponding action
                arguments[argument](*sys.argv[2:])

            else:
                # Assume it's a URL and pass it to url_check
                url_check(argument)
        else:
            usage()

    except IndexError:
        print(
            "You didn't enter anything! Please try again, make sure to enter a valid url.")
        usage()

    except KeyboardInterrupt:
        print("\nAborted by user.")


if __name__ == '__main__':
    main()
