import re
import collections

from peeker import Peeker


class ZProjError(Exception):
    """Custom exception for zproj."""
    pass


class ZProj(object):
    """Object to represent a zproj project.

    Currently, the keys are not necessarily stored in any particular
    order.  Therefore, client code should not assume any order, so that
    it will not break even if the keys are stored in order in the
    future.

    """

    def __init__(self):
        """Initialize an empty project."""
        self._key_dict = {}

    @property
    def keys(self):
        """Return iterable over keys in project."""
        yield from self._key_dict.keys()

    def map_key(self, key, values):
        """Map key to iterable values."""
        if key not in self._key_dict:
            self._key_dict[key] = []
        self._key_dict[key].extend(values)

    def lookup_key(self, key):
        """Return iterable over values for key, else KeyError."""
        if key not in self._key_dict:
            raise ZProjError('ZProj does not define key `{}`.'.format(key))
        return list(self._key_dict[key])


Token = collections.namedtuple('Token', 'kind value filename line column')


# MODULE INTERFACE: file compiler

def compile_zproj_file(filename, error_list=None):
    """Compile source in file named filename into a ZProj object.

    If the optional argument error_list is supplied, any error
    messages generated are appended to it.

    """
    tokens = tokenize_zproj_file(filename, error_list)
    zproj = parse_zproj_tokens(tokens, error_list)
    return zproj


# Tokenization phase (inspired by tokenizer example in Python re docs)

TOKEN_REGEX = r"""
    (?:^|(?<=\s)) (?:
        (?P<COMMENT>\#.*)|
        (?P<COLON>:)|
        (?P<ATOM>[a-zA-Z0-9\.\-]+)|
        (?P<IDENTIFIER>[a-zA-Z][a-zA-Z_0-9\-]*)|
        (?P<ERROR>\S+?)
    ) (?:(?=\s)|$)"""


def tokenize_zproj_file(filename, error_list=None):
    """Generate Tokens from ZProj source in file name filename."""
    with open(filename, 'r') as file:
        lines = list(file)

    bad_tokens = []

    for line_number, line_string in enumerate(lines):
        for mo in re.finditer(TOKEN_REGEX, line_string, flags=re.VERBOSE):
            tok = Token(
                kind=mo.lastgroup,
                value=mo.group(mo.lastgroup),
                filename=filename,
                line=line_number,
                column=mo.start(mo.lastgroup))

            if mo.lastgroup == 'ERROR':
                bad_tokens.append(tok)
            elif mo.lastgroup != 'COMMENT':
                yield tok

    if error_list is not None:
        error_list.extend(
            _error_message('Unexpected token {token.value}', bad_token)
            for bad_token in bad_tokens)

    if bad_tokens:
        raise ZProjError(
            'ERROR: File `{}` could not be tokenized.'.format(filename))


# Parsing phase

def parse_zproj_tokens(tokens, error_list=None):
    """Create ZProj object from iterable tokens.
    
    Currently, this function stops parsing tokens upon the first syntax
    error, because it would be difficult to diagnose the remainder.
    Therefore, it will generate a maximum of one error message.  However,
    in case this behavior changes in the future, and for uniformity with
    tokenize_zproj_file above, this function meets the error_list
    interface.

    """
    zp = ZProj()
    peeker = Peeker(tokens)

    try:
        while peeker:
            expect_token(peeker, 'COLON')
            key = expect_token(peeker, 'ATOM').value
            values = [token.value
                      for token in generate_tokens(peeker, 'ATOM')]
            zp.map_key(key, values)

    except ZProjError as e:
        if error_list is not None:
            error_list.append(str(e))
        raise e

    return zp


def peek_token(peeker):
    """Return current token from peeker."""
    return peeker.peek(0)


def get_token(peeker):
    """Return and consume current token from peeker."""
    token = peek_token(peeker)
    peeker.advance(1)
    return token


def match_token(peeker, kind):
    """Check whether next token exists and has given kind."""
    return peeker and peek_token(peeker).kind == kind


def expect_token(peeker, kind):
    """Error if no token of given kind; get and return otherwise."""
    if not peeker:
        raise ZProjError('Unexpected end of input.')

    token = get_token(peeker)

    if token.kind != kind:
        raise ZProjError(
            _error_message(
                ('Expected token of kind `{}`; '
                 'found `{{token.value}}` '
                 'of kind {{token.kind}}.').format(kind), token))

    return token


def generate_tokens(peeker, kind):
    """Get and generate tokens while of given kind."""
    while match_token(peeker, kind):
        yield get_token(peeker)


def _syntax_error(message, token):
    pass

def _error_message(message, token):
    return (('ERROR ('
             'file {token.filename}, '
             'line {token.line}, '
             'column {token.column}'
             '): ') + message).format(token=token)

# ZProj object rendering

def disassemble_zproj(zproj):
    """Return a source representation of zproj."""
    return '\n'.join(disassemble_zproj_key(zproj, key)
                     for key in sorted(zproj.keys))


def disassemble_zproj_key(zproj, key):
    """Return a source representation of key in zproj."""
    return ': {} {}'.format(key, ' '.join(zproj.lookup_key(key)))
