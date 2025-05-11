import unittest
from io import StringIO
from unittest.mock import patch
from src.commands.echo import Echo


class EchoTestCase(unittest.TestCase):
    def test_simple(self):
        with patch('sys.stdout', new=StringIO()) as test_out:
            Echo("Test echo").run()
            self.assertEqual(test_out.getvalue(), "Test echo\n")

    def test_n_option(self):
        with patch('sys.stdout', new=StringIO()) as test_out:
            Echo("Test echo", n=True).run()
            self.assertEqual(test_out.getvalue(), "Test echo")

    def test_e_option(self):
        with patch('sys.stdout', new=StringIO()) as test_out:
            Echo("Test echo", "\\nNew line", e=True).run()
            self.assertEqual(test_out.getvalue(), "Test echo\nNew line\n")

    def test_E_option(self):
        with patch('sys.stdout', new=StringIO()) as test_out:
            Echo("Test echo", "\\nNot a new line", E=True).run()
            self.assertEqual(test_out.getvalue(), "Test echo\\nNot a new line\n")

    def test_n_e_option(self):
        with patch('sys.stdout', new=StringIO()) as test_out:
            Echo("Test echo", "\\nNew line", n=True, e=True).run()
            self.assertEqual(test_out.getvalue(), "Test echo\nNew line")


if __name__ == '__main__':
    unittest.main()