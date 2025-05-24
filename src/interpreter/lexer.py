import re

from interpreter.bash_token import Token
from variables import Variables



class Lexer:
    def __init__(self, cmds):
        self.token_patterns = [
            ('PIPE', r'\|'),                    # Шаблон для |
            ('FLAGS', r'-[^- \'"=]+'),          # Шаблон для флагов
            ('OPTIONS', r'--[^ ]+'),       # Шаблон для опций
            ('WHITESPACE', r'\s+'),             # Игнорируем пробелы
            # Объявление var=value
            ('VAR_DECL', r'\b[a-zA-Z_][a-zA-Z0-9_]*=(?:\'[^\']*\'|"[^"]*"|[^\s;"\']+)')
        ]

        self.token_patterns.append(('CMD', '|'.join(cmds)))
        self.token_patterns.append(('ARGUMENT', r'[^ ]+'))   # Шаблон для аргументов

        self.vars_re = re.compile(r'(\$\{([a-zA-Z_][a-zA-Z0-9_]*)\}|\$([a-zA-Z_][a-zA-Z0-9_]*))')
        self.token_re = re.compile('|'.join(f'(?P<{name}>{pattern})' for name, pattern in self.token_patterns))

    def run(self, input_str):
        tokens = []
        pos = 0
        input_str = self.format_quotes(input_str)
        input_str = self.format_backslashes(input_str)

        while pos < len(input_str):
            match = self.token_re.match(input_str, pos)
            if not match:
                raise SyntaxError(f"Unexpected character: {input_str[pos]}")
            name = match.lastgroup
            value = match.group(name)
            if name != 'WHITESPACE':
                tokens.append(Token(name, value))
            pos = match.end()
        return tokens

    def format_backslashes(self, value):
        return re.sub(r'\\+', lambda m: '\\' * ((len(m.group())) // 2), value)

    def vars_replacer(self, match):
        var_name = match.group(2) if match.group(2) is not None else match.group(3)
        return Variables().get(var_name)

    # "..." - все раскрывается, '' - остаются как текст
    # '...' - все остается как текст
    # "" / '' - раскрываются лениво -> """""ex" будет раскрыто как "" "" "ex"
    def format_quotes(self, value):
        result = ""
        cur_val = ""
        unclosed_quote = ""
        for s in value:
            # Не кавычки в принципе -> добавляем в значение
            if s != "\'" and s != "\"":
                cur_val += s
            # Точно кавычка, но не совпадает с крайней -> добавляем в значение
            elif unclosed_quote == "":
                unclosed_quote = s
            # Точно кавычка, но крайней еще нет -> добавляем как открывающую
            elif s != unclosed_quote:
                cur_val += s
            # Одинарная кавычка -> не меняем переменные
            elif s == "\'":
                result += cur_val
                cur_val = ""
                unclosed_quote = ""
            # Двойная кавычка -> меняем переменные
            elif s == "\"":
                result += self.vars_re.sub(self.vars_replacer, cur_val)
                cur_val = ""
                unclosed_quote = ""
        # Есть незакрытая кавычка -> ошибка
        if unclosed_quote != "":
            return ""
        # Есть значение без кавычек в конце -> надо заменить переменные
        if cur_val != "":
            cur_val = self.vars_re.sub(self.vars_replacer, cur_val)
        return result + cur_val