import re

from interpreter.bash_token import Token
from variables import Variables


class Lexer:
    def __init__(self, cmds):
        self.quoting_patterns = [
            ('SINGLE_QUOTING', r'\'([^\']+)\''),  # Одинарные кавычки
            ('DOUBLE_QUOTING', r'\"([^\"]+)\"'),  # Двойные кавычки
        ]
        self.token_patterns = [
            ('PIPE', r'\|'),                    # Шаблон для |
            ('FLAGS', r'-[^- \'"=]+'),          # Шаблон для флагов
            ('OPTIONS', r'--[^- \'"=]+'),       # Шаблон для опций
            ('WHITESPACE', r'\s+'),             # Игнорируем пробелы
            # Объявление var=value
            ('VAR_DECL', r'\b[a-zA-Z_][a-zA-Z0-9_]*=(?:\'[^\']*\'|"[^"]*"|[^\s;"\']+)')
        ]

        self.token_patterns.append(('CMD', '|'.join(cmds)))
        self.token_patterns.append(('ARGUMENT', r'[^ ]+'))   # Шаблон для аргументов

        self.vars_re = re.compile(r'(\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\$([a-zA-Z_][a-zA-Z0-9_]*))')
        self.quoting_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.quoting_patterns))
        self.token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns))

    def run(self, input_str):
        tokens = []
        pos = 0
        input_val = self.format_quotes(input_str)

        while pos < len(input_val):
            match = self.token_re.match(input_val, pos)
            if not match:
                raise SyntaxError(f"Unexpected character: {input_val[pos]}")
            name = match.lastgroup
            value = match.group(name)
            if name != 'WHITESPACE':
                tokens.append(Token(name, value))
            pos = match.end()
        return tokens

    def vars_replacer(self, match):
        var_name = match.group(2) if match.group(2) is not None else match.group(3)
        return Variables().get(var_name)

    # "..." - все раскрывается, '' - остаются как текст
    # '...' - все остается как текст
    # "" / '' - раскрываются лениво -> """""ex" будет раскрыто как "" "" "ex"
    def format_quotes(self, value):
        result = ""
        cur_quot = ""
        cur_val = ""
        for s in value:
            if (s == "\'" or s == "\"") and cur_quot == "":
                cur_quot = s
            elif s == "\'" and cur_quot == "\'":
                if cur_val != "": result += cur_val
                cur_quot = ""
                cur_val = ""
            elif s == "\"" and cur_quot == "\"":
                cur_val = self.vars_re.sub(self.vars_replacer, cur_val)
                if cur_val != "": result += cur_val
                cur_quot = ""
                cur_val = ""
            else:
                cur_val += s
        if cur_quot != "":
            cur_val = cur_quot + cur_val
        return result + cur_val