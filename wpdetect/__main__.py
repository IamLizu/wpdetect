import urllib.request
import sys
from pyfiglet import figlet_format

header = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"
version = "1.3.7"
wp_domains = []


def printLogo():
    print(figlet_format('     wpdetect     '))
    print("=================== version: " + version + " ===================\n")


def wp_check_v2(url):
    wpSignature = urllib.request.Request(url, headers={'User-Agent': header})

    try:
        if urllib.request.urlopen(wpSignature):
            return True

    except urllib.error.HTTPError:
        pass


def checkProtocol(url):
    if url[:4] != "http":
        print("[!] No protocol specified.")
        url = "http://" + url
        print("[+] Going with HTTP.\n")
        print("Checking: " + str(url))

    req = urllib.request.Request(url, headers={'User-Agent': header})
    u = urllib.request.urlopen(req)

    if url != u.geturl():
        print("[!] " + url + " redirected to "+u.geturl())
        url = u.geturl()
        print("Checking: " + str(url))

    return url


def checkHTTP(url):
    print("[!] Couldn't connect over HTTPS.")
    print("[+] Trying with HTTP.\n")
    url = "http://" + url[8:]
    print("Checking: " + str(url))

    return url


def url_check(url, isBatch=False):
    print("Checking: " + str(url))
    try:
        url = checkProtocol(url)

        wpSignatures = {
            1: url + "/wp-login.php",
            2: url + "/wp-content/",
            3: url + "/wp-admin/",
            4: url + "/wp-cron.php",
            5: url + "/xmlrpc.php",
            6: url + "/wp-json/wp/v2/",
            7: url + "/wp-content/themes/",
        }

        # run wp_check for each url in wpSignatures
        for wpSignature in wpSignatures:
            result = wp_check_v2(wpSignatures[wpSignature])

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
            url = checkHTTP(url)

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
    print("Example: wpdetect https://iamlizu.com/")
    print("or supply a list with '-f' flag")
    print("Example: wpdetect -f domainlist.txt\n")


def main():
    try:
        printLogo()

        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            usage()
            sys.exit()

        if sys.argv[1] == '-v' or sys.argv[1] == '--version':
            print("Version: 1.3.7")
            sys.exit()

        if sys.argv[1] == '-f' or sys.argv[1] == '--file':
            try:
                if len(sys.argv) > 2:
                    file = open(sys.argv[2], 'r')
                    domains = file.readlines()

                    print("Targets.../\n")

                    for domain in domains:
                        print(domain.strip())
                    print("\n")

                    for domain in domains:
                        url = domain.strip()
                        url_check(url, isBatch=True)

                else:
                    print("No list supplied!")
                    usage()
            except FileNotFoundError:
                print("Please enter file name correctly, file not found!\n")
        else:
            url = sys.argv[1]
            url_check(url)

    except IndexError:
        print(
            "You didn't enter anything! Please try agian, make sure to enter a valid url.")
        usage()

    except KeyboardInterrupt:
        print("\nAborted by user.")


if __name__ == '__main__':
    main()
