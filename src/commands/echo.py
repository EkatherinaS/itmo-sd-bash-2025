"""
https://bash-linux.ru/command/211/komanda-echo-v-linux-s-primerami/
Вывод на экран текста или строки символов
echo [options] [string]

options: необязательный параметр - как отображать выводимый текст
string (строка): текст или сообщение, которое необходимо вывести на экран
может быть простая фраза, значение переменной или сложный вывод сценария.

-n: отключает завершающую новую строку (командная строка будет отображаться сразу после сообщения)
-e: позволяет интерпретировать обратные косые черты (например \n \t и т.д.)
-E: отключает интерпретацию обратных косых черточек (поведение по умолчанию)
"""
from argparse import ArgumentError

from commands.cmd import Cmd

class Echo(Cmd):
    def __init__(self, args, flags, options, stdin):
        Cmd.__init__(self, args, flags, options, stdin)
        self.n = '-n' in self.flags
        self.e = '-e' in self.flags
        self.E = '-E' in self.flags

    def run(self):
        output = []
        if not self.stdin is None and len(self.args) > 0:
            raise ArgumentError("echo : The input object cannot be bound to any parameters for the command either because the command does not take pipeline input or the input and its properties do not match any of the parameters that take pipeline input.")

        for arg in self.args:
            if self.e and not self.E:
                for seq, char in self.escape_seq.items():
                    arg = arg.replace(seq, char)
            output.append(arg)

        joiner = "" if self.n else "\n"
        result = joiner.join(output) + joiner
        return result

    escape_seq = {
        '\\a': '\a',  # Alert (bell)
        '\\b': '\b',  # Backspace
        '\\e': '\x1b',# Escape character
        '\\f': '\f',  # Form feed
        '\\n': '\n',  # New line
        '\\r': '\r',  # Carriage return
        '\\t': '\t',  # Horizontal tab
        '\\v': '\v',  # Vertical tab
        '\\\\': '\\', # Backslash
    }