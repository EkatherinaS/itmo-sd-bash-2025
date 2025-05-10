import re

from interpreter.bash_token import Token
from variables import Variables


class Lexer:
    def __init__(self, cmds):
        self.token_patterns = [
            ('PIPE', r'\|'),                # Шаблон для |
            ('FLAGS', r'-[^- \'"=]+'),      # Шаблон для флагов
            ('OPTIONS', r'--[^- \'"=]+'),   # Шаблон для опций
            ('WHITESPACE', r'\s+'),         # Игнорируем пробелы
            # Строка без изменений
            ('SINGLE_QUOTING', r'\'([^- \=]*?)\''),
            # Объявление var=value
            ('VAR_DECL', r'\b[a-zA-Z_][a-zA-Z0-9_]*=(?:\'[^\']*\'|"[^"]*"|[^\s;"\']+)')
        ]
        self.token_patterns.append(('CMD', '|'.join(cmds)))
        self.token_patterns.append(('ARGUMENT', r'[^- =]+'))   # Шаблон для аргументов

        self.quoting_re = re.compile(r'\"([^- \=]*?)\"')
        self.vars_re = re.compile(r'(\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\$([a-zA-Z_][a-zA-Z0-9_]*))')
        self.unquoted_vars_re = re.compile(r'(?<!\')(\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\$([a-zA-Z_][a-zA-Z0-9_]*))(?!\')')
        self.token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns))

    def run(self, input_str):
        pos = 0
        tokens = []

        input_str = self.quoting_re.sub(self.quoting_replacer, input_str)
        input_str = self.unquoted_vars_re.sub(self.vars_replacer, input_str)

        while pos < len(input_str):
            match = self.token_re.match(input_str, pos)
            if not match:
                raise SyntaxError(f"Unexpected character at position {pos}: {input_str[pos]}")
            name = match.lastgroup
            value = match.group(name)
            if name == 'SINGLE_QUOTING' and len(value) > 2:
                tokens.append(Token('ARGUMENT', value[1:-1]))
            if name != 'WHITESPACE':
                tokens.append(Token(name, value))
            pos = match.end()
        return tokens

    def quoting_replacer(self, match):
        value = match.group(1)
        value = re.sub(r'\\([\\"$])', lambda m: m.group(1), value)
        value = self.vars_re.sub(self.vars_replacer, value)
        return value

    def vars_replacer(self, match):
        var_name = match.group(2) if match.group(2) is not None else match.group(3)
        return Variables().get(var_name)