"""
SkCode tools code.
"""

import re
import unicodedata

from html import escape as escape_html
from urllib.parse import urlsplit, urlunsplit, urljoin


# URL charset regex for cleaning URL
URL_CHARSET_SUB = re.compile(r'[^a-zA-Z0-9-~+_.?#=!&;,/:%@$\|*\'()\[\]\x80-\xff]')


def escape_attrvalue(value):
    """
    Escape the given value and return it escaped and wrapped in simple or double quotes.
    Try to avoid escape sequence as much as possible to make the value more user-friendly.
    :param value: The input attribute value (unescaped).
    :return The attribute value escaped, with surrounding quotes if required.
    """
    if "'" in value and '"' in value:
        return '"%s"' % value.replace('\\', '\\\\').replace('"', '\\"')
    elif "'" in value:
        return '"%s"' % value
    elif '"' in value:
        return "'%s'" % value
    else:
        return '"%s"' % value


def sanitize_url(url, default_scheme='http',
                 allowed_schemes=('http', 'https', 'ftp', 'ftps', 'mailto'),
                 encode_html_entities=True, force_default_scheme=False,
                 force_remove_scheme=False, fix_non_local_urls=True,
                 convert_relative_to_absolute=False, absolute_base_url=''):
    """
    Sanitize the given URL. Avoid XSS by filtering-out forbidden protocol and characters.
    Allowed protocols by default are: ``http``, ``https``, ``ftp``, ``ftps`` and ``mailto``.
    If no protocol scheme is specified, all non-local URL will be tied to the default scheme.
    :param url: The user-supplied URL to be sanitized.
    :param default_scheme: The default scheme to use (default to ``http``).
    :param allowed_schemes: The list of allowed schemes (see defaults above).
    :param encode_html_entities: If set to ``True``, the output URL will be encoded to avoid raw HTML entities
    (default ``True``).
    :param force_default_scheme: Set to ``True`` to force the default scheme to be used in all case (default ``False``).
    :param force_remove_scheme: Set to ``True`` to remove the scheme if set (default ``False``).
    N.B. The ``force_default_scheme`` and ``force_remove_scheme`` are mutually exclusive.
    :param fix_non_local_urls: Set to ``True`` to fix non local URL with netloc in path (default ``True``).
    Example: ``google.com`` become ``http://google.com/``.
    :param convert_relative_to_absolute: Set to ``True`` to convert relative URLs into absolute ones
    (default ``False``). Example: ``/forum/`` become ``http://example.com/forum/``.
    :param absolute_base_url: The base URL for the relative-to-absolute conversion.
    :return: The sanitized URL as string, or an empty string if erroneous.
    """
    assert default_scheme, "A default scheme is mandatory to avoid XSS."
    assert len(allowed_schemes) > 0, "You need to allow at least one scheme to get a result."
    assert not (force_default_scheme and
                force_remove_scheme), "You cannot force the default scheme and also force-remove the scheme."
    if convert_relative_to_absolute:
        assert absolute_base_url, "The absolute base URL is required for the relative-to-absolute conversion."

    # Shortcut for empty string
    if not url:
        return ''

    # Remove dangerous stuff
    url = URL_CHARSET_SUB.sub('', url)

    # Split the URL
    try:
        scheme, netloc, path, query, fragment = urlsplit(url)
    except ValueError:

        # Handle malformed URL
        return ''

    # Check the scheme against the white list
    if scheme and scheme not in allowed_schemes:
        return ''

    # Detect and fix non local URL without // at beginning (not supported by  ``urlsplit``)
    if not netloc and path and not path.startswith('/') and fix_non_local_urls:
        parts = path.split('/', 1)
        if len(parts) == 2:
            netloc, path = parts
        else:
            netloc = parts[0]
            path = ''

    # Add scheme to any non-local URL if required
    if (not scheme and netloc) or force_default_scheme:
        scheme = default_scheme

    # Remove the scheme if requested
    if force_remove_scheme:
        scheme = ''

    # Build the final URL
    if netloc or not convert_relative_to_absolute:
        result = urlunsplit((scheme, netloc, path, query, fragment))
    else:
        result = urlunsplit(('', '', path, query, fragment))
        result = urljoin(absolute_base_url, result)

    # Escape HTML if requested
    if encode_html_entities:
        result = escape_html(result)

    # Return the sanitized URL
    return result


def slugify(value):
    """
    Convert the given value to a plain-text ASCII slug. Spaces are converted to hyphens.
    Characters that aren't alphanumerics, underscores, or hyphens are removed.
    The resulting string is then converted to lowercase. Leading and trailing whitespace are also stripped.
    :param value: The string to be turned into a slug.
    """
    value = value.strip()
    if not value:
        return ''
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub(r'[^\w\s-]', '', value).strip().lower()
    return re.sub(r'[-\s]+', '-', value).strip('-')
