from .zproj import compile_zproj_file, disassemble_zproj

def main():
    """Execute zmake as on command line."""
    print('Hello from zmake.py:main!')
    print(disassemble_zproj(compile_zproj_file('.zproj')))
    # import argparse
    # import sys

    # parser = argparse.ArgumentParser(sys.argv)
    # args = parser.parse_args()
