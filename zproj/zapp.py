import subprocess
import os

from .zproj import ZProj, ZProjError, compile_zproj_file, disassemble_zproj

ASSEMBLER = 'spasm'

LIB_DIR = os.path.join(os.path.dirname(__file__), 'lib')
INCLUDE_DIR = os.path.join(LIB_DIR, 'spasm')

KEY_DIR = LIB_DIR
KEY_BASE = '0104.key'
KEY_FILE = os.path.join(KEY_DIR, KEY_BASE)


def main():
    """Compile app based on .zproj file."""
    zproj = compile_zproj_file('.zproj')

    app_asm_filename = next(iter(zproj.lookup_key('app-file')))
    app_hex_filename = os.path.splitext(app_asm_filename)[0] + '.hex'

    assemble_args = [ASSEMBLER,
                     '-I', INCLUDE_DIR,
                     app_asm_filename, app_hex_filename]
    subprocess.call(assemble_args)

    subprocess.call(['rabbitsign', '-g', '-k', KEY_PATH, app_hex_filename])
