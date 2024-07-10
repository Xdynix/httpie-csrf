# httpie-csrf

[HTTPie](https://httpie.io/) plugin to append CSRF token to request header.

## Installation

(TODO)

## Setting

This plugin use [`python-decouple`](https://github.com/HBNetwork/python-decouple) to
read setting values.

It will try to read values from the following locations in order:

1. `settings.ini`.
2. `.env`.
3. Environment variables.

The following settings can be configured:

- **HTTPIE_CSRF_PREFIX**: Default: `https://example.com`. The plugin will try to add the
  CSRF token to the request header only if the prefix of the requested URL matches this
  value. Note that if you set this to `http://` or `https://` it will override HTTPie's
  built-in adapters.
- **CSRF_COOKIE_NAME**: Default: `csrftoken`. The name of cookie that holds the CSRF
  token.
- **CSRF_HEADER_NAME**: Default: `HTTP_X_CSRFTOKEN`. The name of the header that will be
  used to send the CSRF token. This can be a Django-style header name (e.g.
  `HTTP_X_FOOBAR`) or a standard header name (e.g. `X-Foobar`).

## Development

Prerequisite: [PDM](https://pdm-project.org/latest/)

Environment setup: `pdm sync`

Run linters: `pdm lint`
