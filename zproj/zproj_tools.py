import argparse
import logging
import shutil
import os

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


def new_install_libraries(argument):
    """Install specified library files.

    The current implementation simply removes the previously-installed
    library directory tree and replaces it with the tree specified by
    `argument`.  Note that this gives the wrong result when installing
    a proper subset of the already-installed libraries.

    """
    logging.info('Installing into `{}` directory `{}` from `{}`'.format(
        'existing' if _ensure_directory_exists(LIB_DIR) else 'new',
        LIB_DIR,
        argument))

    for entry in os.scandir(argument):

        if entry.is_file():
            shutil.copy2(entry.path, LIB_DIR)
            logging.info('Installed generic file {}.'.format(entry.name))

        else:
            logging.info('Found subdirectory for assembler `{}`.'.format(
                entry.name))

            install_subdir = os.path.join(LIB_DIR, entry.name)
            _ensure_directory_exists(install_subdir)
            for subentry in os.scandir(entry.path):
                shutil.copy2(subentry.path, install_subdir)
                logging.info('Installed file `{}`.'.format(subentry.name))

    logging.info('Done.')


def _ensure_directory_exists(path):
    """If `path` does not exist, create a directory there.

    This function returns `True` if and only if the directory
    already existed.

    NOTE: The behavior of this function is not defined if `path`
    exists but specifies a file instead of a directory.

    """
    try:
        os.mkdir(path)
    except FileExistsError:
        return True
    else:
        return False


COMMAND_DISPATCH = {
    'install': new_install_libraries
}
