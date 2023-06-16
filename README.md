# WP DETECT
A WordPress detection tool, detects if a website is running WordPress. wpdetect is a great tool when you just want to check WordPress' presence but do not want to scan the site for vulnerabilities or issues.  
### Installation
You can install wpdetect using pip,
```sh
pip install wpdetect
```
wpdetect requires Python 3 or above to run. If you have Python 2 installed too, make sure to use the right pip.

### Usage
Syntax


```sh
wpdetect --url https://iamlizu.com/
```


```sh
cat URLs.txt | wpdetect
```

```sh
echo https://hackerone.com | wpdetect
```


```sh
wpdetect --file urls.txt
```


Where `urls.txt` will contain domains like this,
```sh
https://iamlizu.com/
https://www.newyorker.com/
http://www.techcrunch.com/
```


Please note that, it is not always possible to detect the presence of WordPress, website admins can take extra measures to remove sign of WordPress.

## Options

| Option | Description | Default Vaue |
|--------|-------------|--------------|
| --file | Path of the file containing URLs separated by new line characters    | Empty String |
|  --url | URL of the target         |              |
|--threads| Number of threads|1|
|--timeout| Timeout of the HTTP request in seconds | 5 |