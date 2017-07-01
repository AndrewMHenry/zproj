import os
from .zproj import compile_zproj_file, ZProjError

DIR = os.path.dirname(__file__)
TEMPLATE_MAKEFILE = os.path.join(DIR, 'template-Makefile')
MAKEFILE = 'Makefile'

ASSEMBLER = 'spasm'
LIB_BASE = 'lib'
LIB_DIR = os.path.join(DIR, LIB_BASE)
INCLUDE_DIR = os.path.join(LIB_DIR, ASSEMBLER)

KEY_DIR = LIB_DIR
KEY_BASE = '0104.key'
KEY_FILE = os.path.join(KEY_DIR, KEY_BASE)


def generate_makefile_source(zproj):
    """Create source for Makefile based on zproj."""
    with open(TEMPLATE_MAKEFILE, 'r') as template_makefile:
        template = template_makefile.read()

    main_asm = next(iter(zproj.lookup_key('main-file')))
    app_asm = next(iter(zproj.lookup_key('app-file')))

    app_asm_base = os.path.splitext(app_asm)[0]
    app_hex = app_asm_base + '.hex'
    app_8xk = app_asm_base + '.8xk'

    key_file = KEY_FILE
    include_dir = INCLUDE_DIR

    return template.format(
        main_asm=main_asm,
        app_asm=app_asm,
        app_hex=app_hex,
        app_8xk=app_8xk,
        key_file=key_file,
        include_dir=include_dir)


def main():
    """Execute zmake as on command line."""
    error_list = []
    try:
        zproj = compile_zproj_file('.zproj', error_list)
    except ZProjError:
        print('\n'.join(error_list))
    else:
        with open(MAKEFILE, 'w') as makefile:
            makefile.write(generate_makefile_source(zproj))
