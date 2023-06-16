import click
import sys
import os
import helpers
import threading
import urllib.request
from urllib.parse import urlparse


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


UserAgent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/7046A194A"


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
            if len(target) > 0: ## if targets is not an empty string
                targets.append(target)
    
    if len(singleTarget) != 0:
        targets.append(singleTarget)

    if os.path.isfile(fileName):
        with open(fileName, "r") as targetsFile:
            for line in targetsFile:
                if line.strip() != "":
                    targets.append(line.strip())

    targets = list(filter(helpers.isUrl, targets))
    return targets


@click.command()
@click.option("--mode", default="fast",help="Mode of the scan [fast | slow]")
@click.option("--url", help="Url that you want to scan", default="")
@click.option("--file", help="File to import URLs from", default="")
@click.option("--targets", default=sys.stdin, type=click.File('r'))
@click.option("--threads", default=1, help="Number of threads")
@click.option("--timeout", default=5, help="HTTP Timeout in seconds")
def scan(url, mode, file, targets, threads, timeout):
    if sys.stdin.isatty() == False: # if targets are passed via the standard input
        with targets:
            stdinTargets = targets.read().split("\n")
            targets = import_targets(stdinTargets, url, file)
            targetsArray = helpers.splitArray(targets, threads)
            allThreads = []
            for t in targetsArray:
                thread = threading.Thread(target=isWordpress, args=[t, mode, timeout])
                thread.start()
            #isWordpress(targets, mode)
            
    else: # if standard input is empty
        targets = import_targets([], url, file)
        targetsArray = helpers.splitArray(targets, threads)
        allThreads = []
        for t in targetsArray:
            thread = threading.Thread(target=isWordpress, args=[t, mode, timeout])
            thread.start()
        #isWordpress(targets, mode)

if __name__ == "__main__":
    
    scan()