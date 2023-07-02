# WP DETECT

[![Pylint](https://github.com/IamLizu/wpdetect/actions/workflows/pylint.yml/badge.svg?event=push)](https://github.com/IamLizu/wpdetect/actions/workflows/pylint.yml)
[![Upload Python Package](https://github.com/IamLizu/wpdetect/actions/workflows/pypi-publish.yml/badge.svg?event=release)](https://github.com/IamLizu/wpdetect/actions/workflows/pypi-publish.yml)

A WordPress detection tool, detects if a website is running WordPress. wpdetect is a great tool when you just want to check WordPress' presence but do not want to scan the site for vulnerabilities or issues.

## Installation

You can install wpdetect using pip,

```sh
pip install wpdetect
```

wpdetect requires Python 3 or above to run. If you have Python 2 installed too, make sure to use the right pip.

## Usage

| Option                  | Description                                                                           |
| ----------------------- | ------------------------------------------------------------------------------------- |
| `url`                   | The URL to check. No need to pass the `url` flag, just pass the actual domain or url. |
| `-f, --file`            | File with a list of URLs to check.                                                    |
| `-v, --version`         | Print the version.                                                                    |
| `-ss, --show-signature` | Show by which signature WordPress is detected in a domain.                            |
| `-q, --quiet`           | Only print the detected domains.                                                      |
| `-sf, --scan-full`      | Scan HTTP & HTTPS of the website for WordPress.                                       |

Here's a few basic examples,

```sh
wpdetect <website_url>
```

Example

```sh
wpdetect https://wordpress.org
```

Or feed a text file with a list of domains, each domain should be separated with new lines.

```sh
wpdetect -f sites.txt
```

Where `sites.txt` will contain domains like this,

```sh
https://wordpress.org
https://www.newyorker.com/
http://www.techcrunch.com/
```

Please note that, it is not always possible to detect the presence of WordPress, website admins can take extra measures to remove sign of WordPress.
