import re
import collections

from zproj.peeker import Peeker


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


def compile_zproj_file(filename):
    """Compile source in file named filename into a ZProj object."""
    return parse_zproj_tokens(tokenize_zproj_file(filename))


# Inspired by tokenizer example in Python re docs.

Token = collections.namedtuple('Token', 'kind value filename line column')

TOKEN_REGEX = r"""
    (?:^|(?<=\s)) (?:
        (?P<COMMENT>\#.*)|
        (?P<COLON>:)|
        (?P<IDENTIFIER>[a-zA-Z][a-zA-Z_0-9]*)|
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


def parse_zproj_tokens(tokens):
    zp = ZProj()
    tokens = list(tokens)
    index = 0

    while index < len(tokens):

        if tokens[index].kind != 'COLON':
            raise ZProjError('Expected colon.')
        index += 1

        if tokens[index].kind != 'IDENTIFIER':
            raise ZProjError('Expected identifier.')
        index += 1

        



def prime_tokens(head, tail):
    if head is not None:
        return (head, tail)
    else:
        return 
def more_tokens(peeker):
    try:
        peeker.peek(0)
    except StopIteration:
        return False
    else:
        return True


def peek_token(peeker):
    return peeker.peek(0)


def get_token(peeker):
    token = peek_token(peeker)
    peeker.advance()
    return token


def match_token(peeker, kind):
    """Check whether next token exists and has given kind."""
    return more_tokens(peeker) and peek_token(peeker).kind == kind


def expect_token(peeker, kind):
    """Error if no token of given kind; get and return otherwise."""
    if match_token_kind(peeker, kind):
        raise ZProjError('Expected token of kind `{}`.'.format(kind))
    return peeker.get()


def generate_token_kind(peeker, kind):
    """Get and generate tokens while of given kind."""
    while match_token_kind(peeker, kind):
        yield peeker.get()


# def parse_zproj_tokens(tokens):
#     zp = ZProj()
#     itr = iter(tokens)
#     head, tail = next(itr, None), itr

#     while head is not None:
#         require_token_kind(head, 'COLON')
#         head, tail = advance_tokens(head, tail)
#         require_token_kind(head, 'IDENTIFIER')
#         key = head
        
#         zp.map_key(expect_token_kind(peeker, 'IDENTIFIER'),
#                    generate_token_kind(peeker, 'IDENTIFIER'))

#     return zp


# def require_token_kind(tok, kind):
#     if tok.kind != kind:
#         raise ZProjError('Expected token of kind `{}`.'.format(kind))
    

# def read_token(head, tail):
#     return head, next(tail, None), tail


# def expect_token(head, tail, kind):
#     if head.kind != kind:
#         raise ZProjError('Expected token of kind `{}`.'.format(kind))
#     return read_token(head, tail)

# def parse_zproj_tokens(tokens):
#     """Parse iterable tokens into ZProj object.

#     'COLON'       -->  {'IDENTIFIER'}
#     'IDENTIFIER'  -->  {'COLON', 'IDENTIFIER'}

#     """
#     zp = ZProj()
#     peeker = Peeker(tokens)

#     while not peeker.done:
#         if peeker.peek.kind != 'COLON':
#             raise ZProjError('Expected colon.')
#         peeker.advance()

#         if peeker.peek.kind != 'IDENTIFIER':
#             raise ZProjError('Expected identifier.')
#         key = peeker.peek
#         peeker.advance()

#         values = [
#     current = next(itr, None)
#     allowed = {'COLON', 'IDENTIFIER'}

#     while current is not None:

#         current = peek
#         peek = next(itr, None)

#         expect_token_kind(itr, 'COLON')
#         key = expect_token_kind(itr, 'IDENTIFIER')
        
#         tok = next(itr, None)

#         if tok is None:
#             break
# #        elif tok.kind != '
#     return zp


# def parse_zproj_tokens(tokens):
#     state = 'colon'
#     for token in tokens:
#         if state == 'colon':
#             if token.kind != 'COLON':
#                 raise ZProjError('Expected colon.')
#             state = 'key'
#         elif state == 'key':
#             if token.kind != 'IDENTIFIER':
#                 raise ZProjError('Expected key.')
#             key = token.value
#             values = []
#             state = 'value'
#         elif token.kind == 'IDENTIFIER':
#             pass
