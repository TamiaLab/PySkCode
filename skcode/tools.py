"""
SkCode tools code.
"""

import re
import unicodedata

from html import escape as escape_html
from urllib.parse import urlsplit, urlunsplit


# URL charset regex for cleaning URL
URL_CHARSET_SUB = re.compile(r'[^a-z0-9-~+_.?#=!&;,/:%@$\|*\'()\x80-\xff]', re.I)


def escape_attrvalue(value):
    """
    Escape the given value and return it escaped and wrapped in simple or double quotes.
    Try to avoid escape sequence as much as possible to make the value more user-friendly.
    :param value: The input attribute value (unescaped).
    :return The attribute value escaped, with any surrounding quotes if required.
    """
    if "'" in value and '"' in value:
        # FIXME Maybe encode backslash too? (see parser.py for details)
        return '"%s"' % value.replace('"', '\\"')
    elif "'" in value:
        return '"%s"' % value
    elif '"' in value:
        return "'%s'" % value
    else:
        return '"%s"' % value


def sanitize_url(url, default_scheme='http',
                 allowed_schemes=('http', 'https', 'ftp', 'ftps', 'mailto'),
                 encode_html_entities=True):
    """
    Sanitize the given URL. Avoid XSS by filtering-out forbidden protocol.
    Allowed protocols by default are: http, https, ftp, ftps and mailto.
    If no protocol scheme is specified, all non-local URL will be tied to the default scheme.
    :param url: The user-supplied URL to be sanitized.
    :param default_scheme: Default scheme to use (default to http).
    :param allowed_schemes: List of allowed schemes (see default above).
    :param encode_html_entities: If set, the output URL is encoded to avoid raw HTML entities (default True).
    :return: The sanitized URL as string.
    """
    assert default_scheme, "A default scheme is mandatory to avoid XSS."
    assert len(allowed_schemes) > 0, "You need to allow at least one scheme to get a result!"

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

    # Check scheme with whitelist
    if scheme and scheme not in allowed_schemes:
        return ''

    # Add http scheme to non-local URL if required
    if not scheme and netloc:
        scheme = default_scheme

    # Build the final URL
    result = urlunsplit((scheme, netloc, path, query, fragment))

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
    value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
    value = re.sub('[^\w\s-]', '', value).strip().lower()
    return re.sub('[-\s]+', '-', value)


def unique_slugify(value, existing_slug, slug_namespace=''):
    """
    Convert the given value into an unique slug using the ``slugify`` function and the given dictionary of existing
    slug. A namespace can be specified to avoid recurrent slug conflict.
    :param value: The value to be feed into the ``slugify`` function.
    :param existing_slug: A dictionary of all existing slug (need to be updated **by caller**
    after this function return).
    :param slug_namespace: An optional namespace to avoid recurrent slug conflict (should be ending with an hyphen).
    :return: The slug, unique at the time of calling according to the given dictionary of existing slug.
    """

    # Compute the base slug
    slug = base_slug = slugify(slug_namespace + value)

    # Loop until we find an unique slug
    counter = 2
    while slug in existing_slug:

        # Generate a new slug with the counter appended
        slug = '%s-%d' % (base_slug, counter)
        counter += 1

    # Return the slug
    return slug
