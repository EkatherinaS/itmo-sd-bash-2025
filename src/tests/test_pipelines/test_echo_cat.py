import pytest
from commands.echo import Echo
from commands.cat import Cat

class TestEchoCatInteraction:
    @pytest.fixture
    def config_py_content(self):
        try:
            with open("config.py", 'r') as f:
                return f.read()
        except FileNotFoundError:
            pytest.skip("config.py not found in project root")

    def test_echo_pipe_cat_empty(self):
        echo = Echo([], [], {}, None)
        cat = Cat([], [], {}, echo.run())
        assert cat.run() == "\n"

    def test_cat_pipe_echo_empty(self):
        cat = Cat([], [], {}, None)
        echo = Echo([], [], {}, cat.run())
        assert echo.run() == "\n"

    def test_echo_h_pipe_cat(self):
        echo = Echo(["h"], [], {}, None)
        cat = Cat([], [], {}, echo.run())
        assert cat.run() == "h\n"

    def test_cat_pipe_echo_h(self):
        cat = Cat([], [], {}, None)
        echo = Echo(["h"], [], {}, cat.run())
        assert echo.run() == "h\n"

    def test_echo_h_pipe_cat_config(self, config_py_content):
        echo = Echo(["h"], [], {}, None)
        cat = Cat(["config.py"], [], {}, echo.run())
        assert cat.run() == config_py_content

    def test_cat_config_pipe_echo_h(self):
        cat = Cat(["config.py"], [], {}, None)
        echo = Echo(["h"], [], {}, cat.run())
        assert echo.run() == "h\n"