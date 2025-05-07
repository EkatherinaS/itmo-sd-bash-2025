import re

from interpreter.bash_token import Token

class Lexer:
    def __init__(self, cmds):
        self.token_patterns = [
            ('PIPE', r'\|'),          # Шаблон для |
            ('ARGUMENT', r'".*?"'),   # Шаблон для строк
            ('REDIRECT', r'[><]'),    # Шаблон для перенаправлений
            ('WHITESPACE', r'\s+')    # Игнорируем пробелы
        ]
        self.token_patterns.append(('CMD', '|'.join(cmds)))
        self.token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns))

    def run(self, input_str):
        pos = 0
        tokens = []
        while pos < len(input_str):
            match = self.token_re.match(input_str, pos)

            if not match:
                raise SyntaxError(f"Unexpected character at position {pos}: {input_str[pos]}")

            name = match.lastgroup
            value = match.group(name)

            if name != 'WHITESPACE':
                tokens.append(Token(name, value))

            pos = match.end()
        return tokens