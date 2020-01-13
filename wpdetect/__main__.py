import urllib.request
import sys
from pyfiglet import figlet_format


def inform():
	print("\nPlease keep an eye open for updated version.")
	sys.exit()


def wp_check(url):
    url_wpl = url + "/wp-login.php"
    url_wpac = url + "/wp-content/"
    url_wpad = url + "/wp-admin/"
    url_wpc = url + "/wp-cron.php"
    url_wpx = url + "/xmlrpc.php"
    url_wpa = url + "/wp-json/wp/v2/"

    req_wpl = urllib.request.Request(url_wpl, headers={'User-Agent': 'header'})
    req_wpac = urllib.request.Request(url_wpac, headers={'User-Agent': 'header'})
    req_wpad = urllib.request.Request(url_wpad, headers={'User-Agent': 'header'})
    req_wpc = urllib.request.Request(url_wpc, headers={'User-Agent': 'header'})
    req_wpx = urllib.request.Request(url_wpx, headers={'User-Agent': 'header'})
    req_wpa = urllib.request.Request(url_wpa, headers={'User-Agent': 'header'})

    try:
    	if urllib.request.urlopen(req_wpad):
    		print("Good news, website is using WordPress!")
    		inform()
    except urllib.error.HTTPError:
    	pass
    try:
    	if urllib.request.urlopen(req_wpac):
    		print("Good news, website is using WordPress!")
    		inform()
    except urllib.error.HTTPError:
    	pass
    try:
    	if urllib.request.urlopen(req_wpl):
    		print("Good news, website is using WordPress!")
    		inform()
    except urllib.error.HTTPError:
    	pass
    try:
    	if urllib.request.urlopen(req_wpc):
    		print("Good news, website is using WordPress!")
    		inform()
    except urllib.error.HTTPError:
    	pass
    try:
    	if urllib.request.urlopen(req_wpx):
    		print("Good news, website is using WordPress!")
    		inform()
    except urllib.error.HTTPError:
    	pass
    try:
    	if urllib.request.urlopen(req_wpa):
    		print("Good news, website is using WordPress!")
    		inform()
    except urllib.error.HTTPError:
    	print("Website may not be using WordPress.")
    	inform()


def url_check(url):
    try:
	    if url[:4] != "http":
	        print("No protocol specified.")
	        url = "http://" + url
	        print("Going with http.../")
	    print("Checking '" + url + "'.../")
	    req = urllib.request.Request(url, headers={'User-Agent': 'header'})
	    u = urllib.request.urlopen(req)
	    if url != u.geturl():
	        print("Redirecting to "+u.geturl())
	        url = u.geturl()
	    print("Checking '" + url + "'.../\n")
	    print("Please wait for the process to complete.")
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
        if sys.argv[1] == '-v' or sys.argv[1] == '--version':
        	print("Version: 1.3.1")
        	sys.exit()
        url = sys.argv[1]
        print(figlet_format('     wpdetect     '))
        print("=================== version: 1.3.1 ===================\n")
        url_check(url)
    except IndexError:
        print("You didn't enter anything! Please try agian, make sure to enter a valid url.")
        print("Syntax: wpdetect <website-url>")
        print("Example: wpdetect https://iamlizu.com/")
    except KeyboardInterrupt:
    	print("\nAborted by user.")


if __name__ == '__main__':
	header = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'
	main()