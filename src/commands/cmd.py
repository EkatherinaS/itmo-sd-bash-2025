"""
Базовый класс команды:
[cmd] [options] [arguments]

arguments: *args
options: **kwargs
"""
from abc import abstractmethod


class Cmd:
    def __init__(self, args, flags, options, stdin):
        self.args = args
        self.flags = flags
        self.options = options
        self.stdin = stdin

    @abstractmethod
    def run(self):
        ...
