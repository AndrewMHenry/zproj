import unittest
import zproj.zproj

class TestToken(unittest.TestCase):

    def test_ctor_order(self):
        tok = zproj.zproj.Token(
            filename='yowza',
            kind='COMMENT',
            line=10,
            value='# yowza',
            column=20
            )

    def test_access(self):
        expected_attrs = {
            'kind': 'IDENTIFIER',
            'value': 'foo',
            'filename': 'Makefile',
            'line': 1,
            'column': 23
            }
        tok = zproj.zproj.Token(**expected_attrs)
        actual_attrs = {
            'kind': tok.kind,
            'value': tok.value,
            'filename': tok.filename,
            'line': tok.line,
            'column': tok.column
            }
        self.assertEqual(expected_attrs, actual_attrs)


class TestTokenizer(unittest.TestCase):

    def test_trivial(self):
        pass
