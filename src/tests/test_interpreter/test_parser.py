import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from interpreter.bash_token import Token
from interpreter.parser import Parser

class TestParser:
    @pytest.fixture
    def parser(self):
        return Parser()

    def test_parse_simple_command(self, parser):
        tokens = [
            Token("CMD", "echo"),
            Token("ARGUMENT", "hello")
        ]
        result = parser.run(tokens)
        assert result == {
            "CMD": "echo",
            "ARGS": ["hello"]
        }

    def test_parse_command_with_flags(self, parser):
        tokens = [
            Token("CMD", "ls"),
            Token("FLAGS", "-l"),
            Token("FLAGS", "-a")
        ]
        result = parser.run(tokens)
        assert result == {
            "CMD": "ls",
            "FLAGS": ["-l", "-a"]
        }

    def test_parse_command_with_options(self, parser):
        tokens = [
            Token("CMD", "grep"),
            Token("OPTIONS", "--ignore-case"),
            Token("ARGUMENT", "pattern")
        ]
        result = parser.run(tokens)
        assert result == {
            "CMD": "grep",
            "OPTIONS": ["--ignore-case"],
            "ARGS": ["pattern"]
        }

    def test_parse_pipeline(self, parser):
        tokens = [
            Token("CMD", "echo"),
            Token("ARGUMENT", "hello"),
            Token("PIPE", "|"),
            Token("CMD", "grep"),
            Token("ARGUMENT", "h")
        ]
        result = parser.run(tokens)
        assert result == {
            "CMD": "grep",
            "STDIN": {
                "CMD": "echo",
                "ARGS": ["hello"]
            },
            "ARGS": ["h"]
        }

    def test_parse_complex_pipeline(self, parser):
        tokens = [
            Token("CMD", "cat"),
            Token("ARGUMENT", "file.txt"),
            Token("PIPE", "|"),
            Token("CMD", "grep"),
            Token("OPTIONS", "--color"),
            Token("ARGUMENT", "important"),
            Token("PIPE", "|"),
            Token("CMD", "wc"),
            Token("FLAGS", "-l")
        ]
        result = parser.run(tokens)
        assert result == {
            "CMD": "wc",
            "FLAGS": ["-l"],
            "STDIN": {
                "CMD": "grep",
                "OPTIONS": ["--color"],
                "ARGS": ["important"],
                "STDIN": {
                    "CMD": "cat",
                    "ARGS": ["file.txt"]
                }
            }
        }

    def test_parse_var_declaration(self, parser):
        tokens = [
            Token("VAR_DECL", "NAME=value"),
            Token("CMD", "echo"),
            Token("ARGUMENT", "$NAME")
        ]
        result = parser.run(tokens)
        assert result == {
            "VAR_DECL": "NAME=value",
            "CMD": "echo",
            "ARGS": ["$NAME"]
        }

    def test_empty_input(self, parser):
        tokens = []
        result = parser.run(tokens)
        assert result == {
            "CMD": None
        }

    def test_command_only(self, parser):
        tokens = [Token("CMD", "ls")]
        result = parser.run(tokens)
        assert result == {"CMD": "ls"}

    def test_parse_mixed_arguments(self, parser):
        tokens = [
            Token("CMD", "command"),
            Token("FLAGS", "-v"),
            Token("ARGUMENT", "file1"),
            Token("OPTIONS", "--debug"),
            Token("ARGUMENT", "file2")
        ]
        result = parser.run(tokens)
        assert result == {
            "CMD": "command",
            "FLAGS": ["-v"],
            "OPTIONS": ["--debug"],
            "ARGS": ["file1", "file2"]
        }