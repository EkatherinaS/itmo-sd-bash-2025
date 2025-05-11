import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from commands.wc import Wc
from commands.echo import Echo

class TestEchoWcInteraction:
    @pytest.fixture
    def shell_py_stats(self):
        try:
            with open("shell.py", 'r') as f:
                content = f.read()
                return {
                    'lines': content.count('\n'),
                    'words': len(content.split()),
                    'chars': len(content)
                }
        except FileNotFoundError:
            pytest.skip("shell.py not found in project root")

    def test_echo_pipe_wc(self):
        echo = Echo([], [], {}, None)
        wc = Wc([], [], {}, echo.run())
        assert wc.run() == "      1       0       1\n"

    def test_wc_pipe_echo(self):
        wc = Wc([], [], {}, None)
        echo = Echo([], [], {}, wc.run())
        assert echo.run() == "\n"

    def test_echo_h_pipe_wc(self):
        echo = Echo(["h"], [], {}, None)
        wc = Wc([], [], {}, echo.run())
        assert wc.run() == "      1       1       2\n"

    def test_wc_pipe_echo_h(self):
        wc = Wc([], [], {}, None)
        echo = Echo(["h"], [], {}, wc.run())
        assert echo.run() == "h\n"

    def test_echo_pipe_wc_shell_py(self, shell_py_stats):
        echo = Echo([], [], {}, None)
        wc = Wc(["shell.py"], [], {}, echo.run())
        expected = f"{shell_py_stats['lines']:7} {shell_py_stats['words']:7} {shell_py_stats['chars']:7} shell.py\n"
        assert wc.run() == expected

    def test_wc_shell_py_pipe_echo(self):
        wc = Wc(["shell.py"], [], {}, None)
        echo = Echo([], [], {}, wc.run())
        assert echo.run() == "\n"

    def test_echo_h_pipe_wc_shell_py(self, shell_py_stats):
        echo = Echo(["h"], [], {}, None)
        wc = Wc(["shell.py"], [], {}, echo.run())
        expected = f"{shell_py_stats['lines']:7} {shell_py_stats['words']:7} {shell_py_stats['chars']:7} shell.py\n"
        assert wc.run() == expected

    def test_wc_shell_py_pipe_echo_h(self):
        wc = Wc(["shell.py"], [], {}, None)
        echo = Echo(["h"], [], {}, wc.run())
        assert echo.run() == "h\n"