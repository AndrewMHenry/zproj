#!/usr/bin/env python3
import argparse
import os
import sys

#from zproj.zproj import ZProjError
from .zproj import ZProjError, compile_zproj_file_wrapper

REQUIRED_KEYS = set('input-file output-file entry-point app-name'.split())
OPTIONAL_KEYS = set('library resource'.split())

ZABC_FILE_NAME = '.zabc'
ZABC_OUTPUT_FILE_NAME = 'main.asm'

ZPROJ_FILE_NAME = '.zproj'
TEMPLATE_FILE_NAME = os.path.join(os.path.dirname(__file__), 'template.asm')


def main():
    """Run zabc as from command line."""
    zproj = compile_zproj_file_wrapper()
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
        exit_calls=_format_exit_calls(zproj))


def _get_value(zproj, key):
    """Return the first value associated with key in zproj."""
    return list(zproj.lookup_key(key))[0]


def _format_includes(zproj, key):
    """Return source for #include directives mapped to values for key."""
    return '\n'.join(map('#include "{}"'.format, zproj.lookup_key(key)))


def _format_memory_equates(zproj):
    """Return source for equates to define memory areas."""
    library_bases = _get_library_bases(zproj)
    result = ''
    addends = ['saveSScreen']

    for library_base in library_bases:
        result += '#define {}Data {}\n'.format(
            library_base, ' + '.join(addends))
        addends.append('{}_DATA_SIZE'.format(library_base.upper()))

    return result[:-1]


def _format_init_calls(zproj):
    """Return source for calls to library init routines."""
    return _format_calls(
        '{}Init'.format(base) for base in _get_library_bases(zproj))


def _format_exit_calls(zproj):
    """Return source for calls to library exit routines."""
    return _format_calls(
        '{}Exit'.format(base) for base in reversed(_get_library_bases(zproj)))


def _get_library_bases(zproj):
    """Return bases (without extensions) of included library files."""
    return [os.path.splitext(lib)[0]
            for lib in zproj.lookup_key('library')]


def _format_calls(routines):
    """Return source for CALL instructions to routines."""
    return '\n'.join('{:8}{:8}{}'.format('', 'CALL', r) for r in routines)
