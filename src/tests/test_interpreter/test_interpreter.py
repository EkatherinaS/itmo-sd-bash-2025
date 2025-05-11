import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import pytest
from interpreter.interpreter import Interpreter
from unittest.mock import patch, MagicMock

class TestInterpreter:
    @pytest.fixture
    def interpreter(self):
        return Interpreter()

    def test_simple_command_interpretation(self, interpreter):
        ast = {
            "CMD": "echo",
            "ARGS": ["hello"]
        }
        with patch('interpreter.expression.Expression.interpret') as mock_interpret:
            mock_interpret.return_value = "hello\n"
            result = interpreter.run(ast)
            mock_interpret.assert_called_once()
            assert result == "hello\n"

    def test_pipeline_interpretation(self, interpreter):
        ast = {
            "CMD": "grep",
            "ARGS": ["pattern"],
            "STDIN": {
                "CMD": "cat",
                "ARGS": ["file.txt"]
            }
        }
        with patch('interpreter.expression.Expression.interpret') as mock_interpret:
            mock_interpret.return_value = "matched line\n"
            result = interpreter.run(ast)
            assert result == "matched line\n"

    def test_complex_pipeline(self, interpreter):
        ast = {
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
        with patch('interpreter.expression.Expression.interpret') as mock_interpret:
            mock_interpret.return_value = "42\n"
            result = interpreter.run(ast)
            assert result == "42\n"
