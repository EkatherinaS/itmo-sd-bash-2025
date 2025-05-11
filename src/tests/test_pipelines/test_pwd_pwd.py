import pytest
import os
from commands.pwd import Pwd


class TestPwdPipePwd:
    @pytest.fixture
    def expected_pwd(self):
        return os.getcwd() + "\n"

    def test_pwd_pipe_pwd(self, expected_pwd):
        first_pwd = Pwd([], [], {}, None)
        second_pwd = Pwd([], [], {}, first_pwd.run())

        assert second_pwd.run() == expected_pwd

        assert second_pwd.run() == Pwd([], [], {}, None).run()