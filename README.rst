WP Detect
=========

A WordPress detection tool, detects if a website is running
WordPress. wpdetect is a great tool when you just want to check
WordPress' presence but do not want to scan the site for vulnerabilities
or issues.

Installation
~~~~~~~~~~~~

You can install wpdetect using pip,

.. code:: sh

    pip install wpdetect

wpdetect requires Python 3 or above to run. If you have Python 2
installed too, make sure to use the right pip.

Usage
~~~~~

Syntax

.. code:: sh

	wpdetect <website_url>

Example

.. code:: sh

        wpdetect https://iamlizu.com/

Please note that, it is not always possible to detect the presence of WordPress, website admins can take extra measures to remove sign of WordPress.