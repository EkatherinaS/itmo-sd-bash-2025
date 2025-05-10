import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from commands.pwd import Pwd


class TestPwd:
    @pytest.fixture
    def pwd_cmd(self):
        def _pwd():
            return Pwd([], [], {}, None).run()

        return _pwd

    def test_pwd_returns_current_directory(self, pwd_cmd):
        expected_output = os.getcwd() + "\n"
        assert pwd_cmd() == expected_output

    @patch('os.getcwd')
    def test_pwd_with_mock_directory(self, mock_getcwd, pwd_cmd):
        test_dir = "/path/to/test/directory"
        mock_getcwd.return_value = test_dir

        expected_output = test_dir + "\n"
        assert pwd_cmd() == expected_output
        mock_getcwd.assert_called_once()

    def test_pwd_always_ends_with_newline(self, pwd_cmd):
        output = pwd_cmd()
        assert output.endswith("\n")
        assert len(output) > 1