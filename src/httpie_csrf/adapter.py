from http.cookies import SimpleCookie
from typing import TYPE_CHECKING, Any, cast
from urllib.parse import urlparse

from requests.adapters import HTTPAdapter

if TYPE_CHECKING:
    from requests.models import PreparedRequest


class CsrfAdapter(HTTPAdapter):
    def __init__(
        self,
        *args: Any,
        csrf_cookie_name: str,
        csrf_header_name: str,
        **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.csrf_cookie_name = csrf_cookie_name
        self.csrf_header_name = csrf_header_name

    def add_headers(self, request: "PreparedRequest", **__: Any) -> None:
        self.set_csrf_header(request)
        self.set_referer_header(request)

    def set_csrf_header(self, request: "PreparedRequest") -> None:
        if (cookie_str := request.headers.get("Cookie")) is None:
            return
        cookies = SimpleCookie()
        cookies.load(cookie_str)

        if not (csrf_token := cookies.get(self.csrf_cookie_name)):
            return
        request.headers[self.csrf_header_name] = csrf_token.value

    def set_referer_header(self, request: "PreparedRequest") -> None:
        if "Referer" in request.headers or "Origin" in request.headers:
            return
        url = urlparse(request.url)
        hostname = f"{cast(str, url.scheme)}://{cast(str, url.netloc)}"
        request.headers["Referer"] = hostname
