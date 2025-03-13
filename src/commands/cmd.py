"""
Базовый класс команды:
[cmd] [options] [arguments]

arguments: *args
options: **kwargs
"""

class Cmd:
    def __init__(self, *args, **kwargs):
        self.args = args
        self.options = kwargs