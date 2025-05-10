import os
from commands.cmd import Cmd

class Pwd(Cmd):
    def run(self):
        return os.getcwd() + "\n"