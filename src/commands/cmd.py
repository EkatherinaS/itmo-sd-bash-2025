"""
Базовый класс команды:
[cmd] [options] [arguments]

arguments: *args
options: **kwargs
"""
from abc import abstractmethod


class Cmd:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.options = kwargs

    @abstractmethod
    def run(self):
        ...
