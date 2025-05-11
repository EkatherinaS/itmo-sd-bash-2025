import pytest
import os
from commands.cat import Cat
from commands.pwd import Pwd

class TestPwdCatInteraction:
    @pytest.fixture
    def expected_pwd(self):
        return os.getcwd() + "\n"

    @pytest.fixture
    def config_content(self):
        try:
            with open("config.py") as f:
                return f.read()
        except FileNotFoundError:
            pytest.skip("config.py not found")

    def test_pwd_pipe_cat(self, expected_pwd):
        pwd = Pwd([], [], {}, None)
        cat = Cat([], [], {}, pwd.run())
        assert cat.run() == expected_pwd

    def test_cat_pipe_pwd(self, expected_pwd):
        cat = Cat([], [], {}, None)
        pwd = Pwd([], [], {}, cat.run())
        assert pwd.run() == expected_pwd

    def test_pwd_pipe_cat_config(self, config_content):
        pwd = Pwd([], [], {}, None)
        cat = Cat(["config.py"], [], {}, pwd.run())
        assert cat.run() == config_content

    def test_cat_config_pipe_pwd(self, expected_pwd):
        cat = Cat(["config.py"], [], {}, None)
        pwd = Pwd([], [], {}, cat.run())
        assert pwd.run() == expected_pwd

    def test_pwd_with_stdin(self, expected_pwd):
        pwd = Pwd([], [], {}, "some stdin data")
        assert pwd.run() == expected_pwd

    def test_cat_with_pwd_stdin(self, expected_pwd):
        pwd = Pwd([], [], {}, None)
        cat = Cat([], [], {}, pwd.run())
        assert cat.run() == expected_pwd