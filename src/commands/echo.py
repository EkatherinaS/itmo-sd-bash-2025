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

ФЛАГИ НЕ ПОДДЕРЖИВАЮТСЯ!!!
"""
from commands.cmd import Cmd

class Echo(Cmd):
    def __init__(self, args, flags, options, stdin):
        super().__init__(args, flags, options, stdin)
        self.n = '-n' in self.flags
        self.e = False
        for flag in self.flags:
            self.e = ('-e' == flag)

    def run(self):
        result = ""
        if self.args:
            joiner = " " if not self.n else "\n"
            result = joiner.join(self.args)
        if self.stdin:
            result = self.stdin
        return result + ("" if self.n else "\n")