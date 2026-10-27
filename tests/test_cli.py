"""Tests for the Click command-line entry point."""

import sys
import runpy
from unittest.mock import patch

import pytest
from click.testing import CliRunner

from wpdetect import __main__ as cli
from wpdetect.cli_store import cli_options
from wpdetect.constants import VERSION


@pytest.fixture(autouse=True)
def isolate_cli_options():
    """Keep the module-level options store clean across invocations."""
    original_options = cli_options.copy()
    cli_options.clear()
    cli_options.update({
        'verbose': True,
        'show_signature': False,
        'scan_full': False,
    })

    yield

    cli_options.clear()
    cli_options.update(original_options)


def set_argv(monkeypatch, *args):
    """Set argv for the callback's explicit no-arguments check."""
    monkeypatch.setattr(sys, 'argv', ['wpdetect', *args])


def test_no_arguments_displays_help_and_runs_default_callback(monkeypatch):
    set_argv(monkeypatch)
    runner = CliRunner()

    with patch.object(cli, 'print_logo') as print_logo, \
            patch.object(cli, 'list_detected_domains') as list_domains, \
            patch.object(cli, 'handle_url') as handle_url, \
            patch.object(cli, 'handle_file') as handle_file:
        result = runner.invoke(cli.main, [])

    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert 'Detects if a website is running WordPress.' in result.output
    print_logo.assert_called_once_with(VERSION)
    list_domains.assert_called_once_with()
    handle_url.assert_not_called()
    handle_file.assert_not_called()


def test_help_option_displays_help_without_running_callback():
    runner = CliRunner()

    with patch.object(cli, 'print_logo') as print_logo, \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(cli.main, ['--help'])

    assert result.exit_code == 0
    assert 'Usage:' in result.output
    assert '-q, --quiet' in result.output
    assert '-sf, --scan-full' in result.output
    print_logo.assert_not_called()
    list_domains.assert_not_called()


def test_default_url_path_calls_handler_and_default_prints_logo(monkeypatch):
    set_argv(monkeypatch, 'https://example.com')
    runner = CliRunner()

    with patch.object(cli, 'print_logo') as print_logo, \
            patch.object(cli, 'handle_url') as handle_url, \
            patch.object(cli, 'full_scan') as full_scan, \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(cli.main, ['https://example.com'])

    assert result.exit_code == 0
    print_logo.assert_called_once_with(VERSION)
    handle_url.assert_called_once_with('https://example.com')
    full_scan.assert_not_called()
    list_domains.assert_called_once_with()
    assert cli_options == {
        'verbose': True,
        'show_signature': False,
        'scan_full': False,
    }


def test_quiet_and_show_signature_flags_update_options(monkeypatch):
    set_argv(monkeypatch, '--quiet', '--show-signature', 'example.com')
    runner = CliRunner()

    with patch.object(cli, 'print_logo'), \
            patch.object(cli, 'handle_url') as handle_url, \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(
            cli.main,
            ['--quiet', '--show-signature', 'example.com'],
        )

    assert result.exit_code == 0
    handle_url.assert_called_once_with('example.com')
    list_domains.assert_called_once_with()
    assert cli_options['verbose'] is False
    assert cli_options['show_signature'] is True
    assert cli_options['scan_full'] is False


def test_scan_full_flag_uses_full_scan_for_url(monkeypatch):
    set_argv(monkeypatch, '--scan-full', 'example.com')
    runner = CliRunner()

    with patch.object(cli, 'print_logo'), \
            patch.object(cli, 'full_scan') as full_scan, \
            patch.object(cli, 'handle_url') as handle_url, \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(cli.main, ['--scan-full', 'example.com'])

    assert result.exit_code == 0
    full_scan.assert_called_once_with('example.com')
    handle_url.assert_not_called()
    list_domains.assert_called_once_with()
    assert cli_options['scan_full'] is True


def test_file_option_calls_file_handler(monkeypatch, tmp_path):
    targets = tmp_path / 'targets.txt'
    targets.write_text('https://example.com\n', encoding='utf-8')
    set_argv(monkeypatch, '--file', str(targets))
    runner = CliRunner()

    with patch.object(cli, 'print_logo'), \
            patch.object(cli, 'handle_file') as handle_file, \
            patch.object(cli, 'handle_url') as handle_url, \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(cli.main, ['--file', str(targets)])

    assert result.exit_code == 0
    handle_file.assert_called_once_with(str(targets))
    handle_url.assert_not_called()
    list_domains.assert_called_once_with()


def test_version_flag_prints_version_without_logo(monkeypatch):
    set_argv(monkeypatch, '--version')
    runner = CliRunner()

    with patch.object(cli, 'print_logo') as print_logo, \
            patch.object(cli, 'print', create=True) as print_output, \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(cli.main, ['--version'])

    assert result.exit_code == 0
    print_output.assert_called_once_with(f'Version: {VERSION}')
    print_logo.assert_not_called()
    list_domains.assert_called_once_with()


def test_callback_skips_help_when_sys_argv_contains_arguments(monkeypatch):
    set_argv(monkeypatch, '--quiet')
    runner = CliRunner()

    with patch.object(cli, 'print_logo'), \
            patch.object(cli, 'list_detected_domains') as list_domains:
        result = runner.invoke(cli.main, ['--quiet'])

    assert result.exit_code == 0
    assert 'Usage:' not in result.output
    list_domains.assert_called_once_with()


def test_module_entry_point_invokes_click_command(monkeypatch, capsys):
    monkeypatch.setattr(sys, 'argv', ['wpdetect', '--help'])

    with pytest.raises(SystemExit) as exc_info:
        runpy.run_path(cli.__file__, run_name='__main__')

    assert exc_info.value.code == 0
    assert 'Usage:' in capsys.readouterr().out
