import os
from commands.cmd import Cmd


class Cd(Cmd):
    def __init__(self, args, flags, options, stdin):
        super().__init__(args, flags, options, stdin)

    def run(self):
        if len(self.args) == 1:
            try:
                to_dir = self.args[0]
                os.chdir(to_dir)
            except (FileNotFoundError, NotADirectoryError):
                return f"cd: {to_dir}: No such directory\n"
        cur_dir = os.path.abspath(os.curdir)
        return cur_dir + '\n'
