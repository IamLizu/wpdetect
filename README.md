# WP DETECT
A WordPress detection tool, detects if a website is running WordPress. wpdetect is a great tool when you just want to check WordPress' presence but do not want to scan the site for vulnerabilities or issues.  
### Installation
You can install wpdetect using pip,
```sh
git clone https://github.com/serialfuzzer/wpdetect.git
sudo python setup.py install
```
wpdetect requires Python 3 or above to run. If you have Python 2 installed too, make sure to use the right pip.

### Usage
Syntax

```sh
cat URLs.txt | wpdetect
```

```sh
echo https://hackerone.com | wpdetect
```


```sh
wpdetect <website_url>
```
Example
```sh
wpdetect https://iamlizu.com/
```
Or feed a text file with a list of domains, each domain should be separated with new lines.
```sh
wpdetect -f sites.txt
```
Where `sites.txt` will contain domains like this,
```sh
https://iamlizu.com/
https://www.newyorker.com/
http://www.techcrunch.com/
```

Please note that, it is not always possible to detect the presence of WordPress, website admins can take extra measures to remove sign of WordPress.

### What's new in version 1.3.6
* Fixed minor bugs


# DEV-Notes (Development mind map)

### To implement
1. Use 1000 requests per thread
2. Each request should be sent in an asynchronous way
3. Implement two methods: i. Fast (Some false positives but blazingly fast) ii. Slow (Highly accurate but slow) ✅
4. Combine URLs from standard input, CLI argument and file into a single array, also filter out the incorrect URLs (completed, will push later) ✅


Fast mode (default)
-------------

i. Will send 1 request and analyse it for wordpress patterns

Slow mode
------------

ii. Will send multiple requests and analyse it for wordpress patterns

User interface design 
-----------------------
-slow option should trigger the scans in slow mode
-t option should specift the number of threads

Input options
--------------

Three methods to supply input:
1. File
2. Standard input
3. Command line argument

If all of the input methods contains values then combine the targets from all the sources instead of priotizing one and ignoring other

Some additional optimisations
-------------------------------

Remove duplications from the targets container to avoid sending multiple requests to the same URL

Create test scripts
--------------------

