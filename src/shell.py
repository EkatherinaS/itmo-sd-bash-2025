from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from colorama import Fore

from config import *

from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter

kb = KeyBindings()

@kb.add('c-d')
def _(event):
    event.app.current_buffer.reset()
    event.app.exit(exception=KeyboardInterrupt)

def main():
    lexer = Lexer(cmds)
    parser = Parser()
    interpreter = Interpreter()

    while True:
        try:
            user_input = prompt('BABASH> ', key_bindings=kb).strip()

            tokens = lexer.run(user_input)
            ast = parser.run(tokens)
            result = interpreter.run(ast)

            if result is None:
                print(user_input)
            else:
                print(result, end="")

        except KeyboardInterrupt:
            break

        except SyntaxError as e:
            print(Fore.RED + e.msg)


if __name__ == "__main__":
    main()