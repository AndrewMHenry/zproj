import subprocess
import os

from .zproj import ZProj, ZProjError, compile_zproj_file, disassemble_zproj
from . import data

ASSEMBLER = 'spasm'


def main():
    """Compile app based on .zproj file."""
    zproj = compile_zproj_file('.zproj')

    app_asm_filename = next(iter(zproj.lookup_key('app-file')))
    app_hex_filename = os.path.splitext(app_asm_filename)[0] + '.hex'

    subprocess.call('zabc')

    assemble_args = [ASSEMBLER,
                     '-I', data.get_include_dir(ASSEMBLER),
                     app_asm_filename, app_hex_filename]
    subprocess.call(assemble_args)

    subprocess.call(['rabbitsign', '-g', '-k', data.KEY_FILE, app_hex_filename])
