import urllib.request
import sys

def wp_check(url):
    url_wpl = url + "/wp-login.php"
    url_wpc = url + "/wp-cron.php"
    url_wpx = url + "/xmlrpc.php"
    url_wpr = url + "/readme.html"
    url_wpa = url + "/wp-json/wp/v2/"
    try:
        if urllib.request.urlopen(url_wpr) or urllib.request.urlopen(url_wpl) or urllib.request.urlopen(url_wpc) or urllib.request.urlopen(url_wpx) or urllib.request.urlopen(url_wpa):
            print("Good news, website is using WordPress!")
    except urllib.error.URLError:
            print(sys.argv[1] + " is not using WordPress!")
    print("\nPlease be informed we can not always guarantee the result.")
    print("If you have any suggestions, please email thegeek@iamlizu.com.")


def url_check(url):
    try:
        if url[:4] != "http":
            print("No protocol specified.")
            url = "http://" + url
            print("Going with http.../")
        print("Checking '" + url + "'.../")
        u = urllib.request.urlopen(url)
        if url != u.geturl():
            print("Redirecting to "+u.geturl())
            url = u.geturl()
        print("Checking '" + url + "'.../")
        wp_check(url)
    except urllib.error.URLError:
        print(url + " is not accessible, please make sure the url is valid and publicly accessible.")
    except ValueError:
        print("Invalid url! Please type in correct url, don't forget to add the right protocol.")



def main():
    try:
        if sys.argv[1] == '-h' or sys.argv[1] == '--help':
            print("Syntax: wpdetect <website-url>")
            print("Example: wpdetect https://iamlizu.com/")
            sys.exit()
        url = sys.argv[1]
        url_check(url)
    except IndexError:
        print("You didn't enter anything! Please try agian, make sure to enter a valid url.")
        print("Syntax: wpdetect <website-url>")
        print("Example: wpdetect https://iamlizu.com/")


if __name__ == '__main__':
    main()