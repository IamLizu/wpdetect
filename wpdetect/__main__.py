import click
import sys
import os
import validators
import threading
import urllib.request
from urllib.parse import urlparse
from pyfiglet import figlet_format

banner=figlet_format('     wpdetect     ')
UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"


cliOptions = {
    "silent": False,
    "preferHttps": False,
    "preferHttp": False
}


def notSilentMode():
    return cliOptions["silent"] == False

def output(str):
    if notSilentMode():
        print(str)


def isUrl(string):
    return validators.url(string)

def splitArray(array, n):
    if n != 1:
        final = [array[i * n:(i + 1) * n] for i in range((len(array) + n - 1) // n )]
        return final
    else:
        return [array]

def checkProtocol(url):
    if url[:6] == 'https:':
        return True
    elif url[:5] == 'http:':
        return True
    else:
        return False

def wp_check(url): # this function is defined to support the implementation of previous version of the tool
    try:
        isWp = False
        checks = ['wp-content', 'wp-includes', 'wp-json']
        hostname = urlparse(url).netloc
        request = urllib.request.Request(url, headers={'User-Agent': UserAgent})
        response = urllib.request.urlopen(request).read().decode()
        for check in checks:
            checkStr = hostname + "/" + check
            if checkStr in response:
                isWp=True
        return isWp
    except:
        return False




def isWordpress(urls, mode, timeOut):
    try:
        if mode == "fast":
            checks = ['wp-content', 'wp-includes', 'wp-json']
            for url in urls:
                try:
                    isWp = False
                    hostname = urlparse(url).netloc
                    request = urllib.request.Request(url, headers={'User-Agent': UserAgent})
                    response = urllib.request.urlopen(request, timeout=timeOut).read().decode()
                    for check in checks:
                        checkStr = hostname + "/" + check
                        if checkStr in response:
                            if notSilentMode():
                                print("Good news, " + str(url) + " is using WordPress!")
                            else:
                                print(url)
                            isWp=True
                            break
                        if isWp == True:
                            continue
                except Exception as err:
                    pass
        else:
            pass
    except Exception as e:
        pass

def import_targets(arrayOfTargets, singleTarget, fileName):
    targets = []
    if len(arrayOfTargets) > 0:
        for target in arrayOfTargets:
            if len(target) > 0: ## if target is not an empty string
                targets.append(target)
    
    if len(singleTarget) != 0:
        targets.append(singleTarget)

    if fileName != "":
        if os.path.isfile(fileName):
            with open(fileName, "r") as targetsFile:
                for line in targetsFile:
                    if line.strip() != "":
                        targets.append(line.strip())

    for target in targets:
        mutatedTarget = []
        if checkProtocol(target) == False:
            if cliOptions['preferHttp']:
                mutatedTarget.append("http://" + target)
            elif cliOptions['preferHttps']:
                mutatedTarget.append("https://" + target)
            else:
                mutatedTarget.append("http://" + target)
                mutatedTarget.append("https://" + target)
        else:
            pass
        for tgt in mutatedTarget:
            targets.append(tgt)

    targets = list(filter(isUrl, targets))
    return targets


@click.command()
@click.argument("domain", default="")
@click.option("--mode", default="fast",help="Mode of the scan [fast | slow] Experimental: Dont use this now")
@click.option("-m", "mode", default="fast",help="Mode of the scan [fast | slow] Experimental: Dont use this now")
@click.option("--url", help="Url that you want to scan", default="")
@click.option("-u", "url", help="Url that you want to scan", default="")
@click.option("--file", help="File to import URLs from", default="")
@click.option("-f", "file", default="")
@click.option("--preferhttp/--not-preferhttp", default=False)
@click.option("-ph/-np", "preferhttp", default=False)
@click.option("--preferhttps/--not-preferhttps", default=False)
@click.option("-phs/-nphs", "preferhttps", default=False)
@click.option("--targets", default=sys.stdin, type=click.File('r'))
@click.option("--threads", default=1, help="Number of threads")
@click.option("-tr", "threads", default=1, help="Number of threads")
@click.option("--silent/--not-silent", default=False, help="Do not display banner, just return URLs in the output")
@click.option("-s/--ns", "silent", default=False, help="Do not display banner, just return URLs in the output")
@click.option("--timeout", default=5, help="HTTP Timeout in seconds")
@click.option("-t", "timeout", default=5, help="HTTP Timeout in seconds")
@click.help_option('-h', '--help')
def main(url, mode, file, targets, threads, timeout, silent, preferhttp, preferhttps, domain):
    if domain != "":
        url=domain

    cliOptions["silent"] = silent
    cliOptions["url"] = url
    cliOptions["file"] = file
    cliOptions["threads"] = threads
    cliOptions["timeout"] = timeout
    cliOptions["preferHttp"] = preferhttp
    cliOptions["preferHttps"] = preferhttps
    output(banner)
    if sys.stdin.isatty() == False: # if targets are passed via the standard input
        with targets:
            stdinTargets = targets.read().split("\n")
            targets = import_targets(stdinTargets, url, file)
            targetsArray = splitArray(targets, threads)
            output("Please wait.../")
            for t in targetsArray:
                thread = threading.Thread(target=isWordpress, args=[t, mode, timeout])
                thread.start()
            #isWordpress(targets, mode)
            
    else: # if standard input is empty
        targets = import_targets([], url, file)
        targetsArray = splitArray(targets, threads)
        output("Please wait.../")
        for t in targetsArray:
            thread = threading.Thread(target=isWordpress, args=[t, mode, timeout])
            thread.start()
        #isWordpress(targets, mode)

if __name__ == "__main__":
    main()