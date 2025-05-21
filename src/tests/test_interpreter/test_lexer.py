import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from interpreter.lexer import Lexer
from interpreter.bash_token import Token

class TestLexer:
    @pytest.fixture
    def lexer(self):
        return Lexer(["echo", "ls", "grep"])

    def test_tokenize_simple_command(self, lexer):
        tokens = lexer.run("echo hello")
        assert len(tokens) == 2
        assert tokens[0].group == "CMD"
        assert tokens[0].value == "echo"
        assert tokens[1].group == "ARGUMENT"
        assert tokens[1].value == "hello"

    def test_tokenize_command_with_flags(self, lexer):
        tokens = lexer.run("ls -la")
        assert len(tokens) == 2
        assert tokens[0].group == "CMD"
        assert tokens[0].value == "ls"
        assert tokens[1].group == "FLAGS"
        assert tokens[1].value == "-la"

    def test_tokenize_command_with_options(self, lexer):
        tokens = lexer.run("grep --ignore-case pattern")
        assert len(tokens) == 3
        assert tokens[0].group == "CMD"
        assert tokens[0].value == "grep"
        assert tokens[1].group == "OPTIONS"
        assert tokens[1].value == "--ignore-case"
        assert tokens[2].group == "ARGUMENT"
        assert tokens[2].value == "pattern"

    def test_tokenize_pipe(self, lexer):
        tokens = lexer.run("echo hello | grep h")
        assert len(tokens) == 5
        assert tokens[0].group == "CMD"
        assert tokens[0].value == "echo"
        assert tokens[1].group == "ARGUMENT"
        assert tokens[1].value == "hello"
        assert tokens[2].group == "PIPE"
        assert tokens[2].value == "|"
        assert tokens[3].group == "CMD"
        assert tokens[3].value == "grep"
        assert tokens[4].group == "ARGUMENT"
        assert tokens[4].value == "h"

    def test_tokenize_var_declaration(self, lexer):
        tokens = lexer.run('VAR="value"')
        assert len(tokens) == 1
        assert tokens[0].group == "VAR_DECL"
        assert tokens[0].value == 'VAR=value'

    def test_double_quotes(self, lexer):
        result = lexer.format_quotes('echo "hello"')
        assert result == "echo hello"

    def test_single_quotes(self, lexer):
        result = lexer.format_quotes("echo 'hello'")
        assert result == "echo hello"

    def test_mixed_quotes(self, lexer):
        result = lexer.format_quotes('echo "hello" \'world\'')
        assert result == "echo hello world"

    def test_nested_quotes(self, lexer):
        result = lexer.format_quotes('echo "\'hello\'"')
        assert result == "echo 'hello'"

    def test_smoke_quotes(self, lexer):
        result = lexer.format_quotes('echo \"\'name\'\"')
        assert result == "echo \'name\'"
        result = lexer.format_quotes('echo \"\'name\"')
        assert result == "echo \'name"
        result = lexer.format_quotes('echo \'\"name\"\'')
        assert result == "echo \"name\""
        result = lexer.format_quotes('echo \'name\"\'')
        assert result == "echo name\""
        result = lexer.format_quotes('echo \"\"\"\"\"\"\"\"\"\"\"\"name\"\"')
        assert result == "echo name"
        result = lexer.format_quotes('echo \"\"\"\"\"\"\"\'\'\'\'\"name\"\"')
        assert result == "echo \'\'\'\'name"
        result = lexer.format_quotes('echo \'\'\'\'\'\"\"\'name\"\"')
        assert result == "echo \"\"name"

        result = lexer.format_quotes('echo \'\"$name\"\'')
        assert result == "echo \"$name\""
        result = lexer.format_quotes('echo \'$name\"\'')
        assert result == "echo $name\""

        result = lexer.format_quotes('echo \"\'\"\'\"')
        assert result == ""
        result = lexer.format_quotes('echo \'\"\'\"\'')
        assert result == ""

    def test_empty_input(self, lexer):
        tokens = lexer.run("")
        assert len(tokens) == 0