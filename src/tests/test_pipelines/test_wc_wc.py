import pytest
from commands.wc import Wc


class TestWcPipeWc:
    @pytest.fixture
    def shell_content(self):
        try:
            with open("shell.py") as f:
                content = f.read()
                return {
                    'content': content,
                    'lines': content.count('\n'),
                    'words': len(content.split()),
                    'chars': len(content)
                }
        except FileNotFoundError:
            pytest.skip("shell.py not found")

    def test_empty_wc_pipe_wc(self):
        first_wc = Wc([], [], {}, None)
        second_wc = Wc([], [], {}, first_wc.run())
        assert second_wc.run() == ""

    def test_wc_shell_pipe_wc(self, shell_content):
        first_wc = Wc(["shell.py"], [], {}, None)
        second_wc = Wc([], [], {}, first_wc.run())

        output = f"{shell_content['lines']:7} {shell_content['words']:7} {shell_content['chars']:7} shell.py\n"
        lines = 1
        words = 4
        chars = len(output)

        assert second_wc.run() == f"{lines:7} {words:7} {chars:7}\n"

    def test_empty_wc_pipe_wc_shell(self, shell_content):
        first_wc = Wc([], [], {}, None)
        second_wc = Wc(["shell.py"], [], {}, first_wc.run())

        expected = f"{shell_content['lines']:7} {shell_content['words']:7} {shell_content['chars']:7} shell.py\n"
        assert second_wc.run() == expected

    def test_wc_shell_pipe_wc_shell(self, shell_content):
        first_wc = Wc(["shell.py"], [], {}, None)
        second_wc = Wc(["shell.py"], [], {}, first_wc.run())

        expected = f"{shell_content['lines']:7} {shell_content['words']:7} {shell_content['chars']:7} shell.py\n"
        assert second_wc.run() == expected

    def test_wc_ignores_stdin_when_args(self, shell_content):
        wc = Wc(["shell.py"], [], {}, "some stdin data")
        expected = f"{shell_content['lines']:7} {shell_content['words']:7} {shell_content['chars']:7} shell.py\n"
        assert wc.run() == expected