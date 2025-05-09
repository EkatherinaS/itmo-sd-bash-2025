import sys
from commands.cmd import Cmd

class Exit(Cmd):
    def run(self):
        sys.exit(0)