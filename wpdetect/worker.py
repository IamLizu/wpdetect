import urllib.request
import sys
from pyfiglet import figlet_format


def wp_check(url):
    url_wpl = url + "/wp-login.php"
    url_wpac = url + "/wp-content/"
    url_wpad = url + "/wp-admin/"
    url_wpc = url + "/wp-cron.php"
    url_wpx = url + "/xmlrpc.php"
    url_wpa = url + "/wp-json/wp/v2/"

    req_wpl = urllib.request.Request(url_wpl, headers={'User-Agent': header})
    req_wpac = urllib.request.Request(url_wpac, headers={'User-Agent': header})
    req_wpad = urllib.request.Request(url_wpad, headers={'User-Agent': header})
    req_wpc = urllib.request.Request(url_wpc, headers={'User-Agent': header})
    req_wpx = urllib.request.Request(url_wpx, headers={'User-Agent': header})
    req_wpa = urllib.request.Request(url_wpa, headers={'User-Agent': header})

    try:
        print("\n[+] Checking ./")
        print(req_wpad.full_url)
        if urllib.request.urlopen(req_wpad):
            print("\nGood news, website is using WordPress!")
            sys.exit()
    except urllib.error.HTTPError:
        pass
    try:
        print("[+] Checking ../")
        print(req_wpac.full_url)
        if urllib.request.urlopen(req_wpac):
            print("\nGood news, website is using WordPress!")
            sys.exit()
    except urllib.error.HTTPError:
        pass
    try:
        print("[+] Checking .../")
        print(req_wpl.full_url)
        if urllib.request.urlopen(req_wpl):
            print("\nGood news, website is using WordPress!")
            sys.exit()
    except urllib.error.HTTPError:
        pass
    try:
        print("[+] Checking ..../")
        print(req_wpc.full_url)
        if urllib.request.urlopen(req_wpc):
            print("\nGood news, website is using WordPress!")
            sys.exit()
    except urllib.error.HTTPError:
        pass
    try:
        print("[+] Checking ...../")
        print(req_wpx.full_url)
        if urllib.request.urlopen(req_wpx):
            print("\nGood news, website is using WordPress!")
            sys.exit()
    except urllib.error.HTTPError:
        pass
    try:
        print("[+] Checking ....../")
        print(req_wpa.full_url)
        if urllib.request.urlopen(req_wpa):
            print("\nGood news, website is using WordPress!")
            sys.exit()
    except urllib.error.HTTPError:
        print("\nWebsite may not be using WordPress.")
        sys.exit()


def url_check(url):
    try:
        if url[:4] != "http":
            print("[!] No protocol specified.")
            url = "http://" + url
            print("[+] Going with HTTP.\n")
        print("Target: " + url + "\n")
        req = urllib.request.Request(url, headers={'User-Agent': header})
        u = urllib.request.urlopen(req)
        if url != u.geturl():
            print("[!] " + url + " redirected to "+u.geturl())
            url = u.geturl()
            print("Target: " + url + "\n")
        print("Please wait for the process to complete.")
        wp_check(url)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print("Got 403! Website seems to be behind a WAF.")
    except urllib.error.URLError:
        if url[:5] == "https":
            print("[!] Couldn't connect over HTTPS.")
            print("[+] Trying with HTTP.\n")
            url = "http://" + url[8:]
            try:
                url_check(url)
            except urllib.error.URLError:
                print("Couldn't open url, please make sure to type a valid and publicly accessible url.")
        else:
            print("Couldn't open url, please make sure to type a valid and publicly accessible url.")
    except ValueError:
        print("Invalid url! Please type in correct url. ")



def main():
    try:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Syntax: wpdetect <website-url>")
            print("Example: wpdetect https://iamlizu.com/")
            sys.exit()
        if sys.argv[1] == '-v' or sys.argv[1] == '--version':
        	print("Version: 1.3.2")
        	sys.exit()
        url = sys.argv[1]
        print(figlet_format('     wpdetect     '))
        print("=================== version: 1.3.2 ===================\n")
        url_check(url)
    except IndexError:
        print("You didn't enter anything! Please try agian, make sure to enter a valid url.")
        print("Syntax: wpdetect <website-url>")
        print("Example: wpdetect https://iamlizu.com/")
    except KeyboardInterrupt:
    	print("\nAborted by user.")


if __name__ == '__main__':
	header = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"
	main()