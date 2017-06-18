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
    else:
        with open(TEMPLATE_FILE_NAME, 'r') as file:
            source = file.read()

# def parse_source(source, syntax_errors):
#     """Extract keys and values from zabc source string."""
#     ret = {}
#     key = None

#     for words in source.split(':')[1:]:
#         word_list = words.split()

#         try:
#             key = word_list[0]
#         except IndexError:
#             syntax_errors.append('Expected key (last key: {})'.format(key))
#         else:
#             values = word_list[1:]

#             if key not in ret:
#                 ret[key] = []
#             ret[key].extend(values)

#     return ret


# def generate_output(keydict):
#     """Return boilerplated source from keys."""
#     with open(TEMPLATE_FILE_NAME, 'r') as template_file:
#         template_source = template_file.read()

#     return template_source.format(
#         app_name=keydict['app-name'][0],
#         main_file=keydict['input-file'][0],
#         library_includes=_format_includes(keydict, 'library'),
#         resource_includes=_format_includes(keydict, 'resource'),
#         memory_equates=_format_memory_equates(keydict),
#         init_calls=_format_init_calls(keydict),
#         entry_point=keydict['entry-point'][0],
#         exit_calls=_format_exit_calls(keydict)
#        )


# def _format_includes(keydict, key):
#     return '\n'.join(map('#include "{}"'.format, _get_values(keydict, key)))


# def _format_memory_equates(keydict):
#     library_bases = _get_library_bases(keydict)
#     result = ''
#     addends = ['saveSScreen']

#     for library_base in library_bases:
#         result += '#define {}Data {}\n'.format(
#             library_base, ' + '.join(addends))
#         addends.append('{}_DATA_SIZE'.format(library_base.upper()))

#     return result[:-1]


# def _format_init_calls(keydict):
#     return _format_calls(
#         '{}Init'.format(base) for base in _get_library_bases(keydict))


# def _format_exit_calls(keydict):
#     return _format_calls(
#         '{}Exit'.format(base) for base in reversed(_get_library_bases(keydict)))


# def _get_library_bases(keydict):
#     return [os.path.splitext(lib)[0]
#             for lib in _get_values(keydict, 'library')]


# def _format_calls(routines):
#     return '\n'.join('{:8}{:8}{}'.format('', 'CALL', r) for r in routines)


# def _get_values(keydict, key):
#     return keydict[key] if key in keydict else []


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
