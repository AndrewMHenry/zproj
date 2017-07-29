"""Definitions for paths to package data."""
import os

DIR = os.path.dirname(__file__)
LIB_BASE = 'lib'
LIB_DIR = os.path.join(DIR, LIB_BASE)

KEY_DIR = LIB_DIR
KEY_BASE = '0104.key'
KEY_FILE = os.path.join(KEY_DIR, KEY_BASE)
