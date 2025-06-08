import os
from commands.cmd import Cmd


class Cd(Cmd):
    def __init__(self, args, flags, options, stdin):
        super().__init__(args, flags, options, stdin)

    def run(self):
        if len(self.args) > 1:
            return "cd: There are too many arguments\n"
        
        try:
            to_dir = self.args[0] if self.args else os.path.expanduser("~")
            os.chdir(to_dir)
            cur_dir = os.path.abspath(os.curdir)
            return f"{cur_dir}\n"
        except FileNotFoundError:
            return f"cd: {to_dir}: No such directory\n"
        except NotADirectoryError:
            return f"cd: {to_dir}: Not a directory\n"
        except PermissionError:
            return f"cd: {to_dir}: Permission denied\n"
        except Exception as e:
            return f"cd: {to_dir}: {str(e)}\n"