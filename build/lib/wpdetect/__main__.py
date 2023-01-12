import urllib.request
import sys
from pyfiglet import figlet_format

wp_domains = []
header = "'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A'"
def wp_check(url):
    url_wpl = url + "/wp-login.php" 
    url_wpa = url + "/wp-json/wp/v2/" 


    req_wpl = urllib.request.Request(url_wpl, headers={'User-Agent': header})
    req_wpa = urllib.request.Request(url_wpa, headers={'User-Agent': header})

    #print("Please wait.../")
    try:
        if urllib.request.urlopen(req_wpa):
            wp_domains.append(url)
            print(url)
    except urllib.error.HTTPError:
        try:
            if urllib.request.urlopen(req_wpl):
                wp_domains.append(url)
                print(url)
        except urllib.error.HTTPError:
            pass


def url_check(url):
    #print("Checking: " + str(url))
    try:
        if url[:4] != "http":
            #print("[!] No protocol specified.")
            url = "http://" + url
            #print("[+] Going with HTTP.\n")
            #print("Checking: " + str(url))
        req = urllib.request.Request(url, headers={'User-Agent': header})
        u = urllib.request.urlopen(req)
        if url != u.geturl():
            #print("[!] " + url + " redirected to "+u.geturl())
            url = u.geturl()
            #print("Checking: " + str(url))
        wp_check(url)
    except urllib.error.HTTPError as e:
        if e.code == 403:
            pass
    except urllib.error.URLError:
        if url[:5] == "https":
            #print("[!] Couldn't connect over HTTPS.")
            #print("[+] Trying with HTTP.\n")
            url = "http://" + url[8:]
            #print("Checking: " + str(url))
            try:
                url_check(url)
            except urllib.error.URLError:
                pass
        else:
            pass
    except ValueError:
        pass

def help():
    print("\nSyntax: wpdetect <website-url>")
    print("Example: wpdetect https://iamlizu.com/")
    print("or supply a list with '-f' flag")
    print("Example: wpdetect -f domainlist.txt\n")
    print("Example: cat urls.txt | wpdetect \n")

def main():
    try:
        if len(sys.argv) > 1:
            if sys.argv[1] == '-h' or sys.argv[1] == '--help':
                help()
                sys.exit()
            if sys.argv[1] == '-v' or sys.argv[1] == '--version':
                print("Version: 1.3.7")
                sys.exit()
        
        if not sys.stdin.isatty():
            for line in sys.stdin:
                url_check(line.strip())
        elif sys.argv[1] == '-f' or sys.argv[1] == '--file':
            try:
                if len(sys.argv) > 2:
                    file = open(sys.argv[2], 'r')
                    domains = file.readlines()
                    for domain in domains:
                        url = domain.strip()
                        url_check(url)
                    sys.exit()
                else:
                    print("No list supplied!")
                    help()
            except FileNotFoundError:
                    print("Please enter file name correctly, file not found!\n")
        else:
            url = sys.argv[1]
            url_check(url)

    except KeyboardInterrupt:
    	pass


if __name__ == '__main__':
	main()