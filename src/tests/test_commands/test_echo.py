import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from commands.echo import Echo

class TestEcho:
    @pytest.fixture
    def echo_cmd(self):
        def _echo(args=None):
            return Echo(args or [], [], {}, None).run()
        return _echo

    def test_single_word(self, echo_cmd):
        assert echo_cmd(args=["hello"]) == "hello\n"

    def test_multiple_words(self, echo_cmd):
        assert echo_cmd(args=["heLlo", "worLd"]) == "heLlo worLd\n"

    def test_double_quoted(self, echo_cmd):
        assert echo_cmd(args=['"heLlo worLd"']) == '"heLlo worLd"\n'

    def test_single_quoted(self, echo_cmd):
        assert echo_cmd(args=["'heLlo worLd'"]) == "'heLlo worLd'\n"

    def test_numbers(self, echo_cmd):
        assert echo_cmd(args=["456"]) == "456\n"

    def test_empty_input(self, echo_cmd):
        assert echo_cmd() == "\n"

    @pytest.mark.parametrize("input_text,expected", [
        ("hello#world", "hello#world\n"),
        ("100%", "100%\n"),
        ("file*.txt", "file*.txt\n")
    ])
    def test_special_chars(self, echo_cmd, input_text, expected):
        assert echo_cmd(args=[input_text]) == expected