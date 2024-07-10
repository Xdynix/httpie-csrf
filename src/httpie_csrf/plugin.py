from httpie.plugins import TransportPlugin

from httpie_csrf.adapter import CsrfAdapter


class HttpieCsrfPlugin(TransportPlugin):  # type: ignore[misc]
    name = "CSRF header transport"

    description = (
        "Get the CSRF token from Cookies before sending the request and "
        "add it to the request header."
    )

    @classmethod
    def get_request_headers(cls) -> CsrfAdapter:
        return CsrfAdapter()
