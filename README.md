# WP DETECT
A WordPress detection tool, detects if a website is running WordPress. wpdetect is a great tool when you just want to check WordPress' presence but do not want to scan the site for vulnerabilities or issues.  
### Installation
You can install wpdetect using pip,
```sh
git clone repository_url
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