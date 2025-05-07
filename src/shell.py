from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings

from interpreter.lexer import Lexer
from interpreter.parser import Parser
from config import *

kb = KeyBindings()

@kb.add('c-d')
def _(event):
    event.app.current_buffer.reset()
    event.app.exit(exception=KeyboardInterrupt)

def main():
    lexer = Lexer(cmds)
    parser = Parser()

    while True:
        try:
            user_input = prompt('BABASH> ', key_bindings=kb).strip()
            if user_input.lower() in ('exit', 'quit'):
                break

            tokens = lexer.run(user_input)
            for res in tokens:
                print(res.group + ": " + res.value )

            #TODO: parse lexer result
            ast = parser.run(tokens)

            #TODO: interpret AST

        except KeyboardInterrupt:
            break

        except SyntaxError as e:
            print(e)


if __name__ == "__main__":
    main()