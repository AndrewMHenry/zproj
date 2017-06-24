import os
from .zproj import compile_zproj_file, disassemble_zproj, ZProjError

TEMPLATE_MAKEFILE = os.path.join(os.path.dirname(__file__), 'template-Makefile')
MAKEFILE = 'Makefile'

ASSEMBLER = 'spasm'

LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')
INCLUDE_DIR = os.path.join(LIB_DIR, 'spasm')

KEY_DIR = LIB_DIR
KEY_BASE = '0104.key'
KEY_FILE = os.path.join(KEY_DIR, KEY_BASE)


def generate_makefile_source(zproj):
    with open(TEMPLATE_MAKEFILE, 'r') as template_makefile:
        template = template_makefile.read()

    main_asm = next(iter(zproj.lookup_key('main-file')))
    app_base = '{}-app'.format(os.path.splitext(main_asm)[0])

    app_asm = app_base + '.asm'
    app_hex = app_base + '.hex'
    app_8xk = app_base + '.8xk'

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
    print('Hello from zmake.py:main!')

    error_list = []
    try:
        zproj = compile_zproj_file('.zproj', error_list)
    except ZProjError:
        print('\n'.join(error_list))
    else:
        with open(MAKEFILE, 'w') as makefile:
            makefile.write(generate_makefile_source(zproj))
