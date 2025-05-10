import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from commands.wc import Wc

class TestWc:
    @pytest.fixture
    def wc_cmd(self):
        def _wc(args=None):
            return Wc(args or [], [], {}, None).run()

        return _wc

    def test_nonexistent_file(self, wc_cmd):
        assert wc_cmd(args=["nonexistent_file.txt"]) == "wc: nonexistent_file.txt: No such file or directory\n"

    def test_single_file(self, wc_cmd):
        try:
            with open("shell.py", 'r') as f:
                content = f.read()
                lines = content.count('\n')
                words = len(content.split())
                chars = len(content)
                expected_output = f"{lines:7} {words:7} {chars:7} shell.py\n"
        except FileNotFoundError:
            pytest.skip("shell.py not found in project root")

        assert wc_cmd(args=["shell.py"]) == expected_output

    def test_multiple_files(self, wc_cmd):
        files_to_test = ["shell.py", "config.py"]
        results = []
        totals = [0, 0, 0]

        for file in files_to_test:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    lines = content.count('\n')
                    words = len(content.split())
                    chars = len(content)
                    results.append(f"{lines:7} {words:7} {chars:7} {file}")
                    totals[0] += lines
                    totals[1] += words
                    totals[2] += chars
            except FileNotFoundError:
                pytest.skip(f"{file} not found in project root")

        expected_output = "\n".join(results) + f"\n{totals[0]:7} {totals[1]:7} {totals[2]:7} total\n"
        assert wc_cmd(args=files_to_test) == expected_output

    def test_empty_input(self, wc_cmd):
        assert wc_cmd() == ""