from zproj.zproj import ZProjError


def parse_file(filename, syntax_errors):
    """Parse contents of file named filename into keys and values"""
    with open(filename, 'r') as file:
        source = file.read()
    return parse_source(source, syntax_errors)


def parse_source(source):
    """Extract keys and values from zabc source string."""
    ret = {}
    key = None
    syntax_errors = []

    for words in source.split(':')[1:]:
        word_list = words.split()

        try:
            key = word_list[0]
        except IndexError:
            syntax_errors.append('Expected key (last key: {})'.format(key))
        else:
            values = word_list[1:]

            if key not in ret:
                ret[key] = []
            ret[key].extend(values)

    if syntax_errors:
        raise ZProjError(SYNTAX_ERROR_HEADER + '\n\n' + '\n'.join(syntax_errors))

    return ret


def tokenize_lines(lines):
    pass
