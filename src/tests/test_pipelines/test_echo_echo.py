import pytest
from commands.echo import Echo

class TestEchoPipeEcho:
    def test_echo_pipe_echo_empty(self):
        first_echo = Echo([], [], {}, None)
        second_echo = Echo([], [], {}, first_echo.run())
        assert second_echo.run() == "\n"

    def test_echo_h_pipe_echo_empty(self):
        first_echo = Echo(["h"], [], {}, None)
        second_echo = Echo([], [], {}, first_echo.run())
        assert second_echo.run() == "\n"

    def test_echo_empty_pipe_echo_h(self):
        first_echo = Echo([], [], {}, None)
        second_echo = Echo(["h"], [], {}, first_echo.run())
        assert second_echo.run() == "h\n"

    def test_echo_h_pipe_echo_g(self):
        first_echo = Echo(["h"], [], {}, None)
        second_echo = Echo(["g"], [], {}, first_echo.run())
        assert second_echo.run() == "g\n"

    def test_echo_with_n_flag_pipe_echo(self):
        first_echo = Echo([], ["-n"], {}, None)
        second_echo = Echo([], [], {}, first_echo.run())
        assert second_echo.run() == "\n"

    def test_echo_pipe_echo_with_n_flag(self):
        first_echo = Echo([], [], {}, None)
        second_echo = Echo([], ["-n"], {}, first_echo.run())
        assert second_echo.run() == ""