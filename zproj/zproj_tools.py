import argparse
import logging
import shutil

from .data import LIB_DIR


def main():
    logging.basicConfig(level=logging.INFO)
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=['install'])
    parser.add_argument('argument')
    args = parser.parse_args()

    COMMAND_DISPATCH[args.command](args.argument)


def install_libraries(argument):
    """Install specified library files.

    The current implementation simply removes the previously-installed
    library directory tree and replaces it with the tree specified by
    `argument`.  Note that this gives the wrong result when installing
    a proper subset of the already-installed libraries.

    """
    logging.info('Installing libraries from directory `{}`'.format(argument))
    shutil.rmtree(LIB_DIR, ignore_errors=True)
    shutil.copytree(argument, LIB_DIR)
    logging.info('Done.')


COMMAND_DISPATCH = {
    'install': install_libraries
}
