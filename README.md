# WP DETECT
A WordPress detection tool, detects if a website is running WordPress. wpdetect is a great tool when you just want to check WordPress' presence but do not want to scan the site for vulnerabilities or issues.  
### Installation

#### Installing from pip
You can install wpdetect using pip,
```sh
pip install wpdetect
```
wpdetect requires Python 3 or above to run. If you have Python 2 installed too, make sure to use the right pip.


### Usage
Syntax



```sh
wpdetect https://www.wordpress.com/
```


```sh
wpdetect --url https://www.wordpress.com/
```


```sh
cat URLs.txt | wpdetect
```

```sh
echo https://www.wordpress.com | wpdetect
```


```sh
wpdetect --file urls.txt
```


Where `urls.txt` will contain domains like this,
```sh
https://www.wordpress.com/
https://www.newyorker.com/
http://www.techcrunch.com/
```


Please note that, it is not always possible to detect the presence of WordPress, website admins can take extra measures to remove sign of WordPress.


## Options

| Option | Description | Default Value (Behavior) |
|--------|-------------|--------------|
| --file, -f | Path of the file containing URLs separated by new line characters    | Empty String |
|  --url, -u | URL of the target                                                    |              |
|--threads, -tr| Number of threads                                                   |1             |
|--timeout, -t| Timeout of the HTTP request in seconds                              |5            |
|--silent, -s| Only display URLs using wordpress, don't display banners and any other text | False|
|--preferhttp, -ph| If URL doesn't have http or https, only scan http | Scan both|
|--preferhttps, -phs| If URL doesn't have http or https, only scan https | Scan both |


## Upcoming features
1. **Asynchronous**: We're designing the tool to work in an asynchronous way, this means that there will be further improvements in speed.


### What's new in version 1.3.7
1. Improved performance
2. Multi-Threading
3. Silent Mode
4. Ability to feed targets from standard input
5. Ability to tune HTTP Request timeout