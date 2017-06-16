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


class ZProjTokenizer(object):    
    """Class to generate tokens from ZProj source file."""

    def __init__(self):
        """Initialize "empty" ZProjTokenizer object."""
        self._errors = []

    # PUBLIC INTERFACE

    def tokenize_file(self, filename):
        """Generate tokens from source in file named filename."""
        with open(filename, 'r') as file:
            lines = list(file)

        for line_number, line_string in enumerate(lines):
            for mo in re.finditer(TOKEN_REGEX, line_string, flags=re.VERBOSE):
                tok = Token(
                    kind=mo.lastgroup,
                    value=mo.group(mo.lastgroup),
                    filename=filename,
                    line=line_number,
                    column=mo.start(mo.lastgroup))

                if mo.lastgroup == 'ERROR':
                    self._log_error(self._get_error_message(tok))

                elif mo.lastgroup != 'COMMENT':
                    yield tok

    @property
    def error_list(self):
        """Return list of errors encountered."""
        return self._errors

    # PRIVATE HELPERS

    def _get_error_message(self, token):
        """Return error message reflecting that token was encountered."""
        return '(Line {}, Column {}) Unexpected token {}.'.format(
            tok.line, tok.column, tok.value)

    def _log_error(self, message):
        """Record error with message."""
        self._errors.append(message)



class ZProjParser(object):

    def __init__(self):
        pass

    def parse_tokens(self, tokens):
        """Return ZProj object from iterable tokens."""
        
class ZProjCompiler(object):
    """Class to generate tokens from ZProj source file."""

    def __init__(self):
        """Initialize "empty" ZProjCompiler object."""
        self._errors = []

    # PUBLIC INTERFACE

    @property
    def error_list(self):
        """Return list of errors encountered."""
        return self._errors

    def compile_file(self, filename):
        """Create ZProj object from source in file named filename.

        If the source contains errors and thus cannot be compiled,
        ZProjError is raised.

        """
        tokens = list(self.tokenize_file(filename))
        

    # PRIVATE HELPERS

    def tokenize_file(self, filename):
        """Generate tokens from source in file named filename."""
        with open(filename, 'r') as file:
            lines = list(file)

        for line_number, line_string in enumerate(lines):
            for mo in re.finditer(TOKEN_REGEX, line_string, flags=re.VERBOSE):
                tok = Token(
                    kind=mo.lastgroup,
                    value=mo.group(mo.lastgroup),
                    filename=filename,
                    line=line_number,
                    column=mo.start(mo.lastgroup))

                if mo.lastgroup == 'ERROR':
                    self._log_error(self._get_error_message(tok))

                elif mo.lastgroup != 'COMMENT':
                    yield tok

    def _get_error_message(self, token):
        """Return error message reflecting that token was encountered."""
        return '(Line {}, Column {}) Unexpected token {}.'.format(
            tok.line, tok.column, tok.value)

    def _log_error(self, message):
        """Record error with message."""
        self._errors.append(message)

    def _parse_zproj_tokens(self, tokens):
        """Create ZProj object from iterable tokens."""
        zp = ZProj()
        peeker = Peeker(tokens)

        while peeker:
            self._expect_token(peeker, 'COLON')
            zp.map_key(self._expect_token(peeker, 'IDENTIFIER'),
                       self._generate_tokens(peeker, 'IDENTIFIER'))

        return zp

    def _peek_token(self, peeker):
        """Return current token from peeker."""
        return peeker.peek(0)

    def _get_token(self, peeker):
        """Return and consume current token from peeker."""
        token = self._peek_token(peeker)
        peeker.advance(1)
        return token

    def _match_token(self, peeker, kind):
        """Check whether next token exists and has given kind."""
        return peeker and peek_token(peeker).kind == kind


def expect_token(peeker, kind):
    """Error if no token of given kind; get and return otherwise."""
    if match_token(peeker, kind):
        return get_token(peeker)
    raise ZProjError('Expected token of kind `{}`.'.format(kind))


def generate_tokens(peeker, kind):
    """Get and generate tokens while of given kind."""
    while match_token(peeker, kind):
        yield get_token(peeker)






def compile_zproj_file(filename):
    """Compile source in file named filename into a ZProj object."""
    return parse_zproj_tokens(tokenize_zproj_file(filename))


# Inspired by tokenizer example in Python re docs.

Token = collections.namedtuple('Token', 'kind value filename line column')

TOKEN_REGEX = r"""
    (?:^|(?<=\s)) (?:
        (?P<COMMENT>\#.*)|
        (?P<COLON>:)|
        (?P<IDENTIFIER>[a-zA-Z][a-zA-Z_0-9\-]*)|
        (?P<ERROR>\S+?)
    ) (?:(?=\s)|$)"""


def tokenize_zproj_file(filename):
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

    if bad_tokens:
        raise ZProjError(
            'File `{}` contained one or more unexpected tokens:\n'
            '\n'
            '\n'.join('  Line {}, Column {}: {}'.format(
                tok.line, tok.column, tok.value) for tok in bad_tokens))


def parse_zproj_tokens(tokens):
    """Create ZProj object from iterable tokens."""
    zp = ZProj()
    peeker = Peeker(tokens)

    while peeker:
        expect_token(peeker, 'COLON')
        zp.map_key(expect_token(peeker, 'IDENTIFIER'),
                   generate_tokens(peeker, 'IDENTIFIER'))

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
    if match_token(peeker, kind):
        return get_token(peeker)
    raise ZProjError('Expected token of kind `{}`.'.format(kind))


def generate_tokens(peeker, kind):
    """Get and generate tokens while of given kind."""
    while match_token(peeker, kind):
        yield get_token(peeker)



def disassemble_zproj(zproj):
    """Return a source representation of zproj."""
    return '\n'.join(disassemble_zproj_key(zproj, key)
                     for key in sorted(zproj.keys))


def disassemble_zproj_key(zproj, key):
    """Return a source representation of key in zproj."""
    return ': {} {}'.format(key, zproj.lookup_key(key))
