import pytest
import sys
import os
from unittest.mock import patch

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from commands.exit import Exit


class TestExit:
    @pytest.fixture
    def exit_cmd(self):
        return Exit([], [], {}, None)

    @patch('sys.exit')
    def test_exit_calls_sys_exit_with_zero(self, mock_exit, exit_cmd):
        exit_cmd.run()

        mock_exit.assert_called_once_with(0)

    def test_exit_actually_exits(self, exit_cmd):
        with pytest.raises(SystemExit) as excinfo:
            exit_cmd.run()

        assert excinfo.value.code == 0