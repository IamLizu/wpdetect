"""Tests for WordPress URL and target-file scanning helpers."""

# The descriptive test names serve as documentation for these cases.
# pylint: disable=missing-function-docstring

from io import StringIO
from urllib.error import HTTPError, URLError
from unittest.mock import MagicMock, Mock, call

import pytest

from wpdetect import cli_store
from wpdetect.constants import ERROR_UNABLE_TO_OPEN_FILE, ERROR_UNABLE_TO_OPEN_URL, HEADER
from wpdetect.utils import wp


@pytest.fixture(autouse=True)
def reset_wp_state():
    """Keep module-level scan state isolated between tests."""
    wp.detected_domains.clear()
    cli_store.cli_options.update({
        "verbose": True,
        "show_signature": False,
        "scan_full": False,
    })
    yield
    wp.detected_domains.clear()
    cli_store.cli_options.update({
        "verbose": True,
        "show_signature": False,
        "scan_full": False,
    })


def http_error(code):
    return HTTPError("https://example.test/", code, "error", {}, None)


def test_is_wp_builds_request_and_returns_true_for_open_response(monkeypatch):
    response = MagicMock()
    response.__enter__ = Mock(return_value=response)
    response.__exit__ = Mock(return_value=False)
    urlopen = Mock(return_value=response)
    monkeypatch.setattr(wp.urllib.request, "urlopen", urlopen)

    assert wp.is_wp("https://example.test/wp-login.php") is True

    request = urlopen.call_args.args[0]
    assert request.full_url == "https://example.test/wp-login.php"
    assert request.get_header("User-agent") == HEADER
    response.__enter__.assert_called_once_with()
    response.__exit__.assert_called_once_with(None, None, None)


def test_is_wp_returns_false_for_http_error(monkeypatch):
    urlopen = Mock(side_effect=http_error(404))
    monkeypatch.setattr(wp.urllib.request, "urlopen", urlopen)

    assert wp.is_wp("https://example.test/wp-login.php") is False
    urlopen.assert_called_once()


def test_handle_url_adds_http_and_stores_site_url_when_found(monkeypatch, capsys):
    add_http = Mock(side_effect=lambda url: "http://" + url)
    monkeypatch.setattr(wp, "add_http", add_http)
    monkeypatch.setattr(wp, "check_redirect", lambda url: url)
    is_wp = Mock(return_value=True)
    monkeypatch.setattr(wp, "is_wp", is_wp)

    wp.handle_url("example.test")

    add_http.assert_called_once_with("example.test")
    is_wp.assert_called_once_with("http://example.test/wp-login.php")
    assert wp.detected_domains == ["http://example.test"]
    output = capsys.readouterr().out
    assert "Checking: example.test" in output
    assert "No protocol specified." in output
    assert "WordPress found at: http://example.test" in output


def test_handle_url_displays_signature_when_configured(monkeypatch, capsys):
    cli_store.cli_options["show_signature"] = True
    monkeypatch.setattr(wp, "check_redirect", lambda url: url)
    monkeypatch.setattr(wp, "is_wp", lambda _: True)

    wp.handle_url("https://example.test")

    assert wp.detected_domains == ["https://example.test/wp-login.php"]
    assert "WordPress found at: https://example.test/wp-login.php" in capsys.readouterr().out


def test_handle_url_reports_not_found_and_stops_after_first_signature(monkeypatch, capsys):
    monkeypatch.setattr(wp, "check_redirect", lambda url: url)
    is_wp = Mock(return_value=False)
    monkeypatch.setattr(wp, "is_wp", is_wp)

    wp.handle_url("https://example.test")

    is_wp.assert_called_once_with("https://example.test/wp-login.php")
    assert not wp.detected_domains
    assert "WordPress not found at: https://example.test" in capsys.readouterr().out


@pytest.mark.parametrize("code, message", [
    (403, "Got 403! Website seems to be behind a WAF."),
    (500, None),
])
def test_handle_url_http_error(monkeypatch, capsys, code, message):
    monkeypatch.setattr(wp, "check_redirect", Mock(side_effect=http_error(code)))

    wp.handle_url("https://example.test")

    output = capsys.readouterr().out
    if message:
        assert message in output
    else:
        assert "Got 403!" not in output


def test_handle_url_https_url_error_falls_back_and_finds_site(monkeypatch, capsys):
    monkeypatch.setattr(wp, "add_http", lambda url: url.replace("https://", "http://"))
    check_redirect = Mock(side_effect=[URLError("TLS failure"), "http://example.test"])
    monkeypatch.setattr(wp, "check_redirect", check_redirect)
    is_wp = Mock(return_value=True)
    monkeypatch.setattr(wp, "is_wp", is_wp)

    wp.handle_url("https://example.test")

    assert check_redirect.call_args_list == [
        call("https://example.test"),
        call("http://example.test"),
    ]
    is_wp.assert_called_once_with("http://example.test/wp-login.php")
    assert wp.detected_domains == ["http://example.test"]
    output = capsys.readouterr().out
    assert "Couldn't connect over HTTPS." in output
    assert "WordPress found at: http://example.test" in output


def test_handle_url_https_url_error_reports_failed_http_fallback(monkeypatch, capsys):
    monkeypatch.setattr(wp, "add_http", lambda url: url.replace("https://", "http://"))
    monkeypatch.setattr(
        wp,
        "check_redirect",
        Mock(side_effect=[URLError("TLS failure"), URLError("HTTP failure")]),
    )

    wp.handle_url("https://example.test")

    output = capsys.readouterr().out
    assert "Couldn't connect over HTTPS." in output
    assert ERROR_UNABLE_TO_OPEN_URL.strip() in output


def test_handle_url_catches_url_error_raised_during_fallback(monkeypatch, capsys):
    original_handle_url = wp.handle_url
    monkeypatch.setattr(wp, "check_redirect", Mock(side_effect=URLError("TLS failure")))
    monkeypatch.setattr(wp, "add_http", lambda url: url.replace("https://", "http://"))
    monkeypatch.setattr(wp, "handle_url", Mock(side_effect=URLError("fallback failed")))

    original_handle_url("https://example.test")

    output = capsys.readouterr().out
    assert "Couldn't connect over HTTPS." in output
    assert ERROR_UNABLE_TO_OPEN_URL.strip() in output


def test_handle_url_non_https_url_error_reports_error(monkeypatch, capsys):
    monkeypatch.setattr(wp, "check_redirect", Mock(side_effect=URLError("failure")))

    wp.handle_url("http://example.test")

    output = capsys.readouterr().out
    assert ERROR_UNABLE_TO_OPEN_URL.strip() in output
    assert "Couldn't connect over HTTPS." not in output


def test_handle_url_value_error_reports_invalid_url(monkeypatch, capsys):
    monkeypatch.setattr(wp, "check_redirect", Mock(side_effect=ValueError("bad url")))

    wp.handle_url("https://example.test")

    assert "Invalid URL! Please type in the correct URL." in capsys.readouterr().out


@pytest.mark.parametrize("scan_full", [False, True])
def test_handle_file_routes_each_stripped_line(monkeypatch, capsys, scan_full):
    cli_store.cli_options["scan_full"] = scan_full
    contents = StringIO(" https://one.test/ \n\ntwo.test\n")
    open_mock = Mock(return_value=contents)
    monkeypatch.setattr(wp, "open", open_mock, raising=False)
    handler = Mock()
    monkeypatch.setattr(wp, "full_scan" if scan_full else "handle_url", handler)

    wp.handle_file("targets.txt")

    open_mock.assert_called_once_with("targets.txt", "r", encoding="utf-8")
    assert handler.call_args_list == [
        call("https://one.test/"),
        call(""),
        call("two.test"),
    ]
    output = capsys.readouterr().out
    assert "Targets," in output
    assert "https://one.test/" in output
    assert "two.test" in output


def test_handle_file_reports_file_not_found(monkeypatch, capsys):
    open_mock = Mock(side_effect=FileNotFoundError)
    monkeypatch.setattr(wp, "open", open_mock, raising=False)

    wp.handle_file("missing.txt")

    open_mock.assert_called_once_with("missing.txt", "r", encoding="utf-8")
    assert capsys.readouterr().out == ERROR_UNABLE_TO_OPEN_FILE + "\n"


def test_list_detected_domains_prints_only_when_not_verbose(capsys):
    wp.detected_domains.extend(["https://one.test", "https://two.test"])

    cli_store.cli_options["verbose"] = True
    wp.list_detected_domains()
    assert capsys.readouterr().out == ""

    cli_store.cli_options["verbose"] = False
    wp.list_detected_domains()
    assert capsys.readouterr().out.splitlines() == [
        "https://one.test",
        "https://two.test",
    ]


def test_full_scan_scans_http_then_https(monkeypatch, capsys):
    handle_url = Mock()
    monkeypatch.setattr(wp, "handle_url", handle_url)

    wp.full_scan("example.test/path")

    assert handle_url.call_args_list == [
        call("http://example.test/path"),
        call("https://example.test/path"),
    ]
    output = capsys.readouterr().out
    assert "Full scan initiated for example.test/path" in output
    assert "[1] Scanning HTTP..." in output
    assert "[2] Scanning HTTPS..." in output
