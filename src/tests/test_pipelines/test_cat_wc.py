import pytest
import os
from commands.cat import Cat
from commands.wc import Wc


class TestCatWcInteraction:
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

    def test_empty_cat_pipe_wc(self):
        cat = Cat([], [], {}, None)
        wc = Wc([], [], {}, cat.run())
        assert wc.run() == ""

    def test_empty_wc_pipe_cat(self):
        wc = Wc([], [], {}, None)
        cat = Cat([], [], {}, wc.run())
        assert cat.run() == ""

    def test_cat_config_pipe_wc(self, config_content):
        cat = Cat(["config.py"], [], {}, None)
        wc = Wc([], [], {}, cat.run())

        lines = config_content.count('\n')
        words = len(config_content.split())
        chars = len(config_content)

        if config_content.endswith('\n'):
            lines -= 1
        else:
            chars += 1

        expected = f"{lines:7} {words:7} {chars:7}\n"
        assert wc.run() == expected

    def test_wc_pipe_cat_config(self, config_content):
        wc = Wc([], [], {}, None)
        cat = Cat(["config.py"], [], {}, wc.run())
        assert cat.run() == config_content

    def test_empty_cat_pipe_wc_shell(self, shell_content):
        cat = Cat([], [], {}, None)
        wc = Wc(["shell.py"], [], {}, cat.run())

        lines = shell_content.count('\n')
        words = len(shell_content.split())
        chars = len(shell_content)

        expected = f"{lines:7} {words:7} {chars:7} shell.py\n"
        assert wc.run() == expected

    def test_wc_shell_pipe_cat(self, shell_content):
        wc = Wc(["shell.py"], [], {}, None)
        cat = Cat([], [], {}, wc.run())

        lines = shell_content.count('\n')
        words = len(shell_content.split())
        chars = len(shell_content)

        expected = f"{lines:7} {words:7} {chars:7} shell.py\n"
        assert cat.run() == expected

    def test_cat_config_pipe_wc_shell(self, shell_content):
        cat = Cat(["config.py"], [], {}, None)
        wc = Wc(["shell.py"], [], {}, cat.run())

        lines = shell_content.count('\n')
        words = len(shell_content.split())
        chars = len(shell_content)

        expected = f"{lines:7} {words:7} {chars:7} shell.py\n"
        assert wc.run() == expected

    def test_wc_shell_pipe_cat_config(self, config_content):
        wc = Wc(["shell.py"], [], {}, None)
        cat = Cat(["config.py"], [], {}, wc.run())
        assert cat.run() == config_content