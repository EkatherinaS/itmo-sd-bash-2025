import pytest
import os
from commands.pwd import Pwd
from commands.wc import Wc


class TestPwdWcInteraction:
    @pytest.fixture
    def expected_pwd(self):
        return os.getcwd() + "\n"

    @pytest.fixture
    def config_content(self):
        try:
            with open("config.py") as f:
                content = f.read()
                return {
                    'content': content,
                    'lines': content.count('\n'),
                    'words': len(content.split()),
                    'chars': len(content)
                }
        except FileNotFoundError:
            pytest.skip("config.py not found")

    def test_pwd_pipe_wc(self, expected_pwd):
        pwd = Pwd([], [], {}, None)
        wc = Wc([], [], {}, pwd.run())

        lines = 1
        words = len(expected_pwd.strip().split())
        chars = len(expected_pwd)

        assert wc.run() == f"{lines:7} {words:7} {chars:7}\n"

    def test_wc_pipe_pwd(self, expected_pwd):
        wc = Wc([], [], {}, None)
        pwd = Pwd([], [], {}, wc.run())
        assert pwd.run() == expected_pwd

    def test_pwd_pipe_wc_config(self, config_content, expected_pwd):
        pwd = Pwd([], [], {}, None)
        wc = Wc(["config.py"], [], {}, pwd.run())

        expected = f"{config_content['lines']:7} {config_content['words']:7} {config_content['chars']:7} config.py\n"
        assert wc.run() == expected

    def test_wc_config_pipe_pwd(self, expected_pwd):
        wc = Wc(["config.py"], [], {}, None)
        pwd = Pwd([], [], {}, wc.run())
        assert pwd.run() == expected_pwd

    def test_pwd_always_ignores_stdin(self, expected_pwd):
        pwd = Pwd([], [], {}, "any stdin data")
        assert pwd.run() == expected_pwd

    def test_wc_with_pwd_stdin(self, expected_pwd):
        pwd = Pwd([], [], {}, None)
        wc = Wc([], [], {}, pwd.run())

        lines = 1
        words = len(expected_pwd.strip().split())
        chars = len(expected_pwd)

        assert wc.run() == f"{lines:7} {words:7} {chars:7}\n"