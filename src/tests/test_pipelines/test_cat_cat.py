import pytest
from commands.cat import Cat


class TestCatPipeCat:
    @pytest.fixture
    def config_content(self):
        try:
            with open("config.py") as f:
                return f.read()
        except FileNotFoundError:
            pytest.skip("config.py not found")

    @pytest.fixture
    def shell_content(self):
        try:
            with open("shell.py") as f:
                return f.read()
        except FileNotFoundError:
            pytest.skip("shell.py not found")

    def test_empty_cat_pipe_cat(self):
        first_cat = Cat([], [], {}, None)
        second_cat = Cat([], [], {}, first_cat.run())
        assert second_cat.run() == ""

    def test_empty_cat_pipe_cat_config(self, config_content):
        first_cat = Cat([], [], {}, None)
        second_cat = Cat(["config.py"], [], {}, first_cat.run())
        assert second_cat.run() == config_content

    def test_cat_config_pipe_cat(self, config_content):
        first_cat = Cat(["config.py"], [], {}, None)
        second_cat = Cat([], [], {}, first_cat.run())
        assert second_cat.run() == config_content

    def test_cat_config_pipe_cat_shell(self, shell_content):
        first_cat = Cat(["config.py"], [], {}, None)
        second_cat = Cat(["shell.py"], [], {}, first_cat.run())
        assert second_cat.run() == shell_content

    def test_cat_with_stdin_and_args(self, config_content, shell_content):
        cat = Cat(["shell.py"], [], {}, config_content)
        assert cat.run() == shell_content

        cat = Cat([], [], {}, config_content)
        assert cat.run() == config_content

        cat = Cat(["shell.py"], [], {}, None)
        assert cat.run() == shell_content

        cat = Cat([], [], {}, None)
        assert cat.run() == ""