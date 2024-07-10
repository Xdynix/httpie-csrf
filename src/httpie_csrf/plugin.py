from pathlib import Path

from decouple import AutoConfig
from httpie.plugins import TransportPlugin

from httpie_csrf.adapter import CsrfAdapter

config = AutoConfig(search_path=Path.cwd())

HTTPIE_CSRF_PREFIX: str = config(
    "HTTPIE_CSRF_PREFIX",
    default="https://example.com",
)

CSRF_COOKIE_NAME: str = config("CSRF_COOKIE_NAME", default="csrftoken")

CSRF_HEADER_NAME: str = config("CSRF_HEADER_NAME", default="HTTP_X_CSRFTOKEN")
# Normalize Django style header name.
if CSRF_HEADER_NAME.isupper() and CSRF_HEADER_NAME.startswith("HTTP_"):
    CSRF_HEADER_NAME = CSRF_HEADER_NAME.removeprefix("HTTP_").replace("_", "-")


class HttpieCsrfPlugin(TransportPlugin):  # type: ignore[misc]
    name = "CSRF header transport"

    description = (
        "Get the CSRF token from Cookies before sending the request and "
        "add it to the request header."
    )

    prefix = HTTPIE_CSRF_PREFIX

    @classmethod
    def get_adapter(cls) -> CsrfAdapter:
        return CsrfAdapter(
            csrf_cookie_name=CSRF_COOKIE_NAME,
            csrf_header_name=CSRF_HEADER_NAME,
        )
