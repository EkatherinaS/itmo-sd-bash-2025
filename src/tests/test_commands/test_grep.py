import pytest
import tempfile
import os
from commands.grep import Grep

class TestGrep:
    @pytest.fixture
    def test_file(self):
        content = """first line
second line with pattern
third line
fourth line with PATTERN
fifth line
sixth line with pattern again
seventh line
eighth line"""
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            f.write(content)
            f.flush()
            yield f.name
        os.unlink(f.name)

    def test_grep_basic_pattern(self, test_file):
        grep = Grep(["pattern", test_file], [], {}, None)
        result = grep.run()
        assert "second line with pattern" in result
        assert "sixth line with pattern again" in result
        assert "PATTERN" not in result
        assert result.count('\n') == 3

    def test_grep_multiple_files(self, test_file):
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f2:
            f2.write("another pattern\nno match\n")
            f2.flush()
            grep = Grep(["pattern", test_file, f2.name], [], {}, None)
            result = grep.run()
            assert test_file in result
            assert f2.name in result
            assert "second line with pattern" in result
            assert "another pattern" in result
            assert "--" in result
            os.unlink(f2.name)

    def test_grep_count(self, test_file):
        grep = Grep(["pattern", test_file], ["-c"], {}, None)
        result = grep.run()
        assert result.strip() == f"{test_file}:2"

    def test_grep_files_with_matches(self, test_file):
        grep = Grep(["pattern", test_file], ["-l"], {}, None)
        result = grep.run()
        assert result.strip() == test_file

    def test_grep_no_pattern(self):
        grep = Grep([], [], {}, None)
        result = grep.run()
        assert "missing pattern" in result

    def test_grep_no_files(self):
        grep = Grep(["pattern"], [], {}, None)
        result = grep.run()
        assert "missing file operand" in result

    def test_grep_invalid_file(self):
        grep = Grep(["pattern", "nonexistent.txt"], [], {}, None)
        result = grep.run()
        assert "No such file or directory" in result

    def test_grep_invalid_pattern(self):
        grep = Grep(["*invalid["], [], {}, None)
        result = grep.run()
        assert "invalid pattern" in result

    def test_grep_stdin_with_flags(self):
        grep = Grep(["pattern"], ["-i"], {}, "input with PATTERN\n")
        result = grep.run()
        assert "input with PATTERN" in result

    def test_grep_after_context(self, test_file):
        grep = Grep(["pattern", test_file], [], ["-A2"], None)
        result = grep.run()
        assert "second line with pattern" in result
        assert "third line" in result
        assert "--" in result
        assert result.count('\n') == 7

    def test_grep_invalid_context(self, test_file):
        grep = Grep(["pattern", test_file], [], ["-A=abc"], None)
        result = grep.run()
        assert "second line with pattern" in result