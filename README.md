# httpie-csrf

A plugin that helps [HTTPie](https://httpie.io/) easily access CSRF-protected
(especially Django-style) endpoints.

It will try to read the CSRF token from the cookie and add it to the corresponding
header; and set the `Referer` header for the request - these are checked by Django's
CSRF protection.

## Usage

Installation:

```shell
httpie cli plugins install git+https://github.com/Xdynix/httpie-csrf.git
```

Configure the settings by creating a `.env` in your working directory,
or setting environment variables.

Example:

```dotenv
# Django project default

# Required. Set to the hostname you're querying.
HTTPIE_CSRF_PREFIX=http://localhost:8000

# Optional, if it's the same as Django's default.
CSRF_COOKIE_NAME=csrftoken

# Optional, if it's the same as Django's default.
CSRF_HEADER_NAME=HTTP_X_CSRFTOKEN
```

Now you can use `http` to query your endpoint directly without being bothered by CSRF
protection or sacrificing the security it brings.

```shell
http --session=dev POST http://localhost:8000/api/login username=john password=secret
```

Caveat: You still need an HTTPie session for this to work. Make it as a default option
in the HTTPie [config](https://httpie.io/docs/cli/config) to omit the argument.

You may also need to first make a request to an endpoint that ensures the CSRF cookie is
provided (such as one decorated with `ensure_csrf()`) to obtain the CSRF token.

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

Test: `pdm test`
