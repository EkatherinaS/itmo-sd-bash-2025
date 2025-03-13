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

from src.commands.cmd import Cmd

class Echo(Cmd):
    def __init__(self, *args, **kwargs):
        Cmd.__init__(self, *args, **kwargs)
        self.n = self.options.get('n', False)
        self.e = self.options.get('e', False)
        self.E = self.options.get('E', False)

    def run(self):
        output = []
        for arg in self.args:
            if self.e and not self.E:
                for seq, char in self.escape_seq.items():
                    arg = arg.replace(seq, char)
            output.append(arg)
        result = ''.join(output)
        print(result, end="" if self.n else "\n")

    escape_seq = {
        '\\a': '\a',  # Alert (bell)
        '\\b': '\b',  # Backspace
        '\\e': '\x1b',  # Escape character
        '\\f': '\f',  # Form feed
        '\\n': '\n',  # New line
        '\\r': '\r',  # Carriage return
        '\\t': '\t',  # Horizontal tab
        '\\v': '\v',  # Vertical tab
        '\\\\': '\\', # Backslash
    }