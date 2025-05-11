import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from commands.cat import Cat


class TestCat:
    @pytest.fixture
    def cat_cmd(self):
        def _cat(args=None):
            return Cat(args or [], [], {}, None).run()

        return _cat

    def test_nonexistent_file(self, cat_cmd):
        assert cat_cmd(args=["nonexistent_file.txt"]) == "cat: nonexistent_file.txt: No such file or directory\n"

    def test_single_file(self, cat_cmd):
        expected_content = ""
        try:
            with open("config.py", 'r') as f:
                expected_content = f.read()
        except FileNotFoundError:
            pytest.skip("config.py not found in project root")

        assert cat_cmd(args=["config.py"]) == expected_content + "\n"

    def test_multiple_files(self, cat_cmd):
        expected_content = []
        files_to_test = ["config.py", "shell.py"]

        for file in files_to_test:
            try:
                with open(file, 'r') as f:
                    expected_content.append(f.read())
            except FileNotFoundError:
                pytest.skip(f"{file} not found in project root")

        expected_output = "\n".join(expected_content) + "\n"
        assert cat_cmd(args=files_to_test) == expected_output

    def test_empty_input(self, cat_cmd):
        assert cat_cmd() == ""