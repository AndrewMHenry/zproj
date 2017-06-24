#!/usr/bin/env python3
import argparse
import os
import sys

#from zproj.zproj import ZProjError
from .zproj import ZProjError, compile_zproj_file

REQUIRED_KEYS = set('input-file output-file entry-point app-name'.split())
OPTIONAL_KEYS = set('library resource'.split())

ZABC_FILE_NAME = '.zabc'
ZABC_OUTPUT_FILE_NAME = 'main.asm'

ZPROJ_FILE_NAME = '.zproj'
TEMPLATE_FILE_NAME = os.path.join(os.path.dirname(__file__), 'template.asm')


def main():
    """Run zabc as from command line."""
    print('Hello from zabc.py:main!')

    error_list = []
    try:
        zproj = compile_zproj_file(ZPROJ_FILE_NAME, error_list)
    except ZProjError:
        print('\n'.join(error_list))
        sys.exit(1)

    with open(_get_value(zproj, 'app-file'), 'w') as file:
        file.write(_generate_output(zproj))


def _generate_output(zproj):
    """Return boilerplated source from ZProj object."""
    with open(TEMPLATE_FILE_NAME, 'r') as template_file:
        template_source = template_file.read()

    return template_source.format(
        app_name=_get_value(zproj, 'app-name'),
        main_file=_get_value(zproj, 'main-file'),
        library_includes=_format_includes(zproj, 'library'),
        resource_includes=_format_includes(zproj, 'resource'),
        memory_equates=_format_memory_equates(zproj),
        init_calls=_format_init_calls(zproj),
        entry_point=_get_value(zproj, 'entry-point'),
        exit_calls=_format_exit_calls(zproj)
       )


def _get_value(zproj, key):
    return list(zproj.lookup_key(key))[0]


def _format_includes(zproj, key):
    return '\n'.join(map('#include "{}"'.format, zproj.lookup_key(key)))


def _format_memory_equates(zproj):
    library_bases = _get_library_bases(zproj)
    result = ''
    addends = ['saveSScreen']

    for library_base in library_bases:
        result += '#define {}Data {}\n'.format(
            library_base, ' + '.join(addends))
        addends.append('{}_DATA_SIZE'.format(library_base.upper()))

    return result[:-1]


def _format_init_calls(zproj):
    return _format_calls(
        '{}Init'.format(base) for base in _get_library_bases(zproj))


def _format_exit_calls(zproj):
    return _format_calls(
        '{}Exit'.format(base) for base in reversed(_get_library_bases(zproj)))


def _get_library_bases(zproj):
    return [os.path.splitext(lib)[0]
            for lib in zproj.lookup_key('library')]


def _format_calls(routines):
    return '\n'.join('{:8}{:8}{}'.format('', 'CALL', r) for r in routines)


# def _error(message):
#     """Display error message and exit."""
#     print(message)
#     sys.exit(1)


# def _list_keys(message, keys):
#     if keys:
#         print('{}\n{}\n'.format(message, '\n'.join('  `{}`'.format(key)
#                                                    for key in keys)))


# if __name__ == '__main__':
#     try:
#         with open(ZABC_FILE_NAME, 'r') as zabc_file:
#             source = zabc_file.read()
#     except FileNotFoundError:
#         _error('File `{}` not found.'.format(ZABC_FILE_NAME))

#     syntax_errors = []
#     keydict = parse_source(source, syntax_errors)
#     if syntax_errors:
#         _error('There were syntax errors in the `{}` file:\n{}'.format(
#             ZABC_FILE_NAME, '\n'.join(syntax_errors)))

#     keys = set(keydict.keys())
#     missing_keys = list(sorted(REQUIRED_KEYS - keys))
#     bad_keys = list(sorted(keys - (REQUIRED_KEYS | OPTIONAL_KEYS)))

#     _list_keys(ZABC_FILE_NAME + ' is missing one or more required keys:',
#                missing_keys)
#     _list_keys(ZABC_FILE_NAME + ' contains one or more invalid keys:',
#                bad_keys)

#     if missing_keys or bad_keys:
#         _error('The program failed due to incorrect keys in {}.'.format(
#             ZABC_FILE_NAME))

#     with open(TEMPLATE_FILE_NAME, 'r') as template_file:
#         template_source = template_file.read()

#     output_source = generate_output(keydict)

#     with open(keydict['output-file'][0], 'w') as output_file:
#         output_file.write(output_source)

#     # parser = argparse.ArgumentParser()
#     # parser.add_argument('filename')
#     # args = parser.parse_args()

#     # print('filename: {}'.format(args.filename))

#     # errors = []
#     # try:
#     #     process_keys(parse_source(read_file(errors), errors), errors)
#     # except RuntimeError:
#     #     print('There were errors:\n{}'.format('\n'.join(errors)))
#     #     sys.exit(1)

#     # print(generate_app_boilerplate('Hello'))
#     # print(generate_library_includes(keydict))
#     # print(generate_resource_includes(keydict))

#     # key_errors = []
#     # process_keys(keydict, key_errors)
#     # if key_errors:
#     #     _error('There were problems with the keys in the `{}` file:\n{}'.format(
#     #         ZABC_FILE_NAME, '\n'.join(key_errors)))



# # def generate_app_boilerplate(app_name):
# #     return '\n'.join([
# #         ';;; APP BOILERPLATE',
# #         '',
# #         '#define APP_NAME "{:8}"'.format(keydict['app-name'][0]),
# #         '#include "app.asm"',
# #         ''])


# # def generate_library_includes(keydict):
# #     return _format_includes(keydict, 'library')


# # def generate_resource_includes(keydict):
# #     return _format_includes(keydict, 'resource')


# # def generate_memory_equates(keydict):
# #     pass


# # def _format_includes(keydict, key):
# #     return '\n'.join([
# #         ';;; {} INCLUSIONS'.format(key.upper()),
# #         '',
# #         '\n'.join('#include "{}"'.format(key)
# #                   for key in _get_values(keydict, key)),
# #         ''])

# # def process_keys(keydict, key_errors):
# #     keys = set(keydict.keys())
# #     key_errors.extend('Missing required key: `{}`'.format(key)
# #                   for key in sorted(REQUIRED_KEYS - keys))
# #     key_errors.extend('Unrecognized key: `{}`'.format(key)
# #                   for key in sorted(keys - (REQUIRED_KEYS | OPTIONAL_KEYS)))

# class ZABCCompiler(object):

#     def __init__(self):
#         self._errors = []

#     @property
#     def errors(self):
#         return self._errors

#     def read_file(self):
#         try:
#             with open(ZABC_FILE_NAME, 'r') as file:
#                 source = file.read()
#         except FileNotFoundError:
#             errors.append('File `{}` not found.'.format(ZABC_FILE_NAME))
#             raise RuntimeError()
#         else:
#             return source
