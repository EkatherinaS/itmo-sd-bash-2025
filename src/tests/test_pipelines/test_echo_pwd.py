import pytest
import os
from commands.echo import Echo
from commands.pwd import Pwd

class TestEchoPwdInteraction:
    @pytest.fixture
    def expected_pwd(self):
        return os.getcwd() + "\n"

    def test_echo_pipe_pwd(self, expected_pwd):
        echo = Echo([], [], {}, None)
        pwd = Pwd([], [], {}, echo.run())
        assert pwd.run() == expected_pwd

    def test_pwd_pipe_echo_empty(self):
        pwd = Pwd([], [], {}, None)
        echo = Echo([], [], {}, pwd.run())
        assert echo.run() == "\n"

    def test_echo_h_pipe_pwd(self, expected_pwd):
        echo = Echo(["h"], [], {}, None)
        pwd = Pwd([], [], {}, echo.run())
        assert pwd.run() == expected_pwd

    def test_pwd_pipe_echo_h(self):
        pwd = Pwd([], [], {}, None)
        echo = Echo(["h"], [], {}, pwd.run())
        assert echo.run() == "h\n"

    def test_pwd_with_stdin(self, expected_pwd):
        pwd = Pwd([], [], {}, "some stdin data")
        assert pwd.run() == expected_pwd