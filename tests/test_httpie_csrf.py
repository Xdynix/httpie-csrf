import importlib
import os
from typing import cast
from urllib.parse import urljoin

import pytest
from pytest_mock import MockerFixture
from requests import Session

import httpie_csrf.plugin

HTTPBIN = "https://httpbin.org"


def mount_adapter(session: Session) -> None:
    importlib.reload(httpie_csrf.plugin)  # Ensure setting values are re-evaluated.
    plugin = httpie_csrf.plugin.HttpieCsrfPlugin()
    session.mount(plugin.prefix, plugin.get_adapter())


def get_headers(session: Session) -> dict[str, str]:
    response = session.get(urljoin(HTTPBIN, "/headers"))
    response.raise_for_status()
    return cast(dict[str, str], response.json()["headers"])


def set_cookies(session: Session, name: str, value: str) -> None:
    url = f"/cookies/set/{name}/{value}"
    response = session.get(urljoin(HTTPBIN, url))
    response.raise_for_status()


@pytest.mark.parametrize("csrf_header_name", ["HTTP_X_FOOBAR", "X-Foobar"])
def test_smoke(mocker: MockerFixture, csrf_header_name: str) -> None:
    csrf_token = "42"  # noqa: S105
    csrf_cookie_name = "answer"

    mocker.patch.dict(
        os.environ,
        {
            "HTTPIE_CSRF_PREFIX": HTTPBIN,
            "CSRF_COOKIE_NAME": csrf_cookie_name,
            "CSRF_HEADER_NAME": csrf_header_name,
        },
    )

    session = Session()
    mount_adapter(session)

    set_cookies(session, "foo", "bar")
    assert "X-Foobar" not in get_headers(session)

    set_cookies(session, csrf_cookie_name, csrf_token)
    assert session.cookies[csrf_cookie_name] == csrf_token
    assert get_headers(session)["X-Foobar"] == csrf_token
