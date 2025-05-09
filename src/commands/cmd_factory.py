from commands.cat import Cat
from commands.echo import Echo
from commands.wc import Wc
from commands.pwd import Pwd
from commands.exit import Exit
# from .grep import Grep


class CmdFactory:

    def __init__(self):
        self.commands = {
            "cat": Cat,
            "echo": Echo,
            "wc": Wc,
            "pwd": Pwd,
            "exit": Exit,
            # "grep": Grep
        }

    def get(self, cmd_name):
        if cmd_name is None:
            return None

        return self.commands[cmd_name]
