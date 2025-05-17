from commands.cat import Cat
from commands.echo import Echo
from commands.wc import Wc
from commands.pwd import Pwd
from commands.exit import Exit
from commands.grep import Grep
from commands.ls import Ls


class CmdFactory:

    def __init__(self):
        self.commands = {
            "cat": Cat,
            "echo": Echo,
            "wc": Wc,
            "pwd": Pwd,
            "exit": Exit,
            "grep": Grep,
            "ls": Ls
        }

    def get(self, cmd_name):
        if cmd_name is None:
            return None
        return self.commands[cmd_name]
