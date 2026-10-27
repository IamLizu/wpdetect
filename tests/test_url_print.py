"""Tests for URL and print utilities."""

# The descriptive test names serve as documentation for these cases.
# pylint: disable=missing-function-docstring

from types import SimpleNamespace
from unittest.mock import Mock, call

import pytest

from wpdetect import cli_store
from wpdetect.utils import print as print_utils
from wpdetect.utils import url


@pytest.fixture(autouse=True)
def reset_cli_options():
    """Give each test predictable CLI options and restore the shared state."""
    original_options = cli_store.cli_options.copy()
    cli_store.cli_options.clear()
    cli_store.cli_options.update(
        {'verbose': True, 'show_signature': False, 'scan_full': False}
    )

    yield

    cli_store.cli_options.clear()
    cli_store.cli_options.update(original_options)


@pytest.mark.parametrize(
    ('value', 'expected'),
    [
        ('https://example.com/path', 'https'),
        ('http://example.com', 'http'),
        ('example.com/path', None),
        ('/relative/path', None),
    ],
)
def test_get_protocol(value, expected):
    assert url.get_protocol(value) == expected


def test_add_scheme_to_url_replaces_existing_scheme():
    assert url.add_scheme_to_url('https://example.com/path', 'http') == (
        'http://example.com/path'
    )


def test_add_scheme_to_url_adds_scheme_when_missing():
    assert url.add_scheme_to_url('example.com/path', 'https') == (
        'https://example.com/path'
    )


def test_add_http_logs_and_applies_http_scheme(capsys):
    assert url.add_http('https://example.com/path') == 'http://example.com/path'
    assert capsys.readouterr().out == '[+] Going with HTTP.\n'


def test_get_redirected_url_uses_redirect_handler_without_network(monkeypatch):
    response = SimpleNamespace(url='https://example.com/final')
    opener = Mock()
    opener.open.return_value = response
    build_opener = Mock(return_value=opener)
    monkeypatch.setattr(url.urllib.request, 'build_opener', build_opener)

    result = url.get_redirected_url('http://example.com/start')

    assert result == 'https://example.com/final'
    build_opener.assert_called_once_with(url.urllib.request.HTTPRedirectHandler)
    opener.open.assert_called_once_with('http://example.com/start')


def test_check_redirect_returns_url_when_there_is_no_redirect(monkeypatch):
    get_redirected_url = Mock(return_value='https://example.com/same')
    print_verbose = Mock()
    print_checking_message = Mock()
    monkeypatch.setattr(url, 'get_redirected_url', get_redirected_url)
    monkeypatch.setattr(url, 'print_verbose', print_verbose)
    monkeypatch.setattr(url, 'print_checking_message', print_checking_message)

    result = url.check_redirect('https://example.com/same')

    assert result == 'https://example.com/same'
    get_redirected_url.assert_called_once_with('https://example.com/same')
    print_verbose.assert_not_called()
    print_checking_message.assert_not_called()


def test_check_redirect_recursively_follows_redirects(monkeypatch):
    urls = [
        'http://example.com/start',
        'https://example.com/middle',
        'https://www.example.com/final',
        'https://www.example.com/final',
    ]
    get_redirected_url = Mock(side_effect=urls[1:])
    print_verbose = Mock()
    print_checking_message = Mock()
    monkeypatch.setattr(url, 'get_redirected_url', get_redirected_url)
    monkeypatch.setattr(url, 'print_verbose', print_verbose)
    monkeypatch.setattr(url, 'print_checking_message', print_checking_message)

    result = url.check_redirect(urls[0])

    assert result == urls[-1]
    assert get_redirected_url.call_args_list == [call(value) for value in urls[:-1]]
    assert print_verbose.call_args_list == [
        call(f'[!] {urls[0]} redirected to {urls[1]}'),
        call(f'[!] {urls[1]} redirected to {urls[2]}'),
    ]
    assert print_checking_message.call_args_list == [call(urls[1]), call(urls[2])]


def test_print_verbose_prints_only_when_verbose(capsys):
    print_utils.print_verbose('visible')
    assert capsys.readouterr().out == 'visible\n'

    cli_store.cli_options['verbose'] = False
    print_utils.print_verbose('hidden')
    assert capsys.readouterr().out == ''


def test_print_checking_message_formats_url_and_respects_verbose(capsys):
    print_utils.print_checking_message(123)
    assert capsys.readouterr().out == '\nChecking: 123\n'

    cli_store.cli_options['verbose'] = False
    print_utils.print_checking_message('https://example.com')
    assert capsys.readouterr().out == ''


def test_print_logo_prints_figlet_and_version_only_when_verbose(monkeypatch, capsys):
    figlet_format = Mock(return_value='ASCII logo')
    monkeypatch.setattr(print_utils, 'figlet_format', figlet_format)

    print_utils.print_logo('1.2.3')

    assert figlet_format.call_args_list == [call('     wpdetect     ')]
    assert capsys.readouterr().out == (
        'ASCII logo\n=================== VERSION: 1.2.3 ===================\n\n'
    )

    cli_store.cli_options['verbose'] = False
    figlet_format.reset_mock()
    print_utils.print_logo('1.2.3')

    figlet_format.assert_called_once_with('     wpdetect     ')
    assert capsys.readouterr().out == ''
