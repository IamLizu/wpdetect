# WP DETECT

A WordPress detection tool, detects if a website is running WordPress. wpdetect is a great tool when you just want to check WordPress' presence but do not want to scan the site for vulnerabilities or issues.

## Installation

You can install wpdetect using pip,

```sh
pip install wpdetect
```

wpdetect requires Python 3 or above to run. If you have Python 2 installed too, make sure to use the right pip.

## Usage

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

## Changelog

#### What's new in version 1.4.3

-   Fixed [#20](https://github.com/IamLizu/wpdetect/issues/20)

#### What's new in version 1.4.2

-   Fixed [#18](https://github.com/IamLizu/wpdetect/issues/18)

#### What's new in version 1.4.1

-   Fixed [#10](https://github.com/IamLizu/wpdetect/issues/10)
-   Added `-h` in `click` help options

#### What's new in version 1.4.0

-   Removed manual argument parsing.
-   Introduced [click](https://click.palletsprojects.com/en/8.1.x/) and parsing arguments with it.
-   Added a sample URL in the repo for ease of testing.

#### What's new in version 1.3.9

-   Minor bug fixes
-   Added workflow for linting on code push
-   Added workflow for publishing to PyPi on release

#### What's new in version 1.3.8

-   Fixed [#8](https://github.com/IamLizu/wpdetect/issues/8)

#### What's new in version 1.3.7

-   Migrated to Hatchling build system
-   Updated README

#### What's new in version 1.3.6

-   Fixed minor bugs
