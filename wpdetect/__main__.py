'''
    Entry point for wpdetect.
'''

import sys
import click
from wpdetect.utils.wp import full_scan, handle_url, handle_file, list_detected_domains
from wpdetect.utils.print import print_logo
from wpdetect.cli_store import cli_options
from wpdetect.constants import VERSION


@click.command(context_settings={"help_option_names": ['-h', '--help']})
@click.argument('url', required=False)
@click.option('-f', '--file', type=click.Path(exists=True), help="File with list of URLs to check.")
@click.option('-v', '--version', is_flag=True, help="Print version.")
@click.option('-ss', '--show-signature', is_flag=True,
              help="Show by which signature WordPress is detected in a domain.")
@click.option('-q', '--quiet', is_flag=True, help="Only print the detected domains.")
@click.option('-sf', '--scan-full', is_flag=True,
              help="Scan HTTP & HTTPS of the website for WordPress.")
def main(*, url=None, file=None, version=None, show_signature=None, quiet=None, scan_full=None):
    """Detects if a website is running WordPress."""

    if quiet:
        cli_options['verbose'] = False

    if show_signature:
        cli_options['show_signature'] = True

    if scan_full:
        cli_options['scan_full'] = True

    if version is False:
        print_logo(VERSION)

    if url:
        if scan_full:
            full_scan(url)
        else:
            handle_url(url)

    if file:
        handle_file(file)

    if version:
        print(f"Version: {VERSION}")

    if len(sys.argv) == 1:
        click.echo(click.get_current_context().get_help())

    # Print detected_domains only when verbose is false
    list_detected_domains()


if __name__ == '__main__':
    main()
