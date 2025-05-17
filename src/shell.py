import re

from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
from colorama import Fore

from config import *

from interpreter.lexer import Lexer
from interpreter.parser import Parser
from interpreter.interpreter import Interpreter

import subprocess
import shlex

kb = KeyBindings()

@kb.add('c-d')
def _(event):
    event.app.current_buffer.reset()
    event.app.exit(exception=KeyboardInterrupt)

def execute_external_command(command):
    try:
        args = shlex.split(command)
        result = subprocess.run(
            args,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
    except FileNotFoundError:
        return f"Command not found: {args[0] if args else 'Unknown'}\n"
    except Exception as e:
        return f"Error executing command: {str(e)}\n"

def main():
    lexer = Lexer(cmds)
    parser = Parser()
    interpreter = Interpreter()

    while True:
        try:
            user_input = prompt('BABASH> ', key_bindings=kb).strip()

            commands = user_input.split(';')
            for cmd in commands:
                tokens = lexer.run(cmd)
                ast = parser.run(tokens)
                result = interpreter.run(ast)

                if result is None:
                    result = execute_external_command(cmd)
                    print(result)
                else:
                    print(result, end="")

        except KeyboardInterrupt:
            break

        except SyntaxError as e:
            print(Fore.RED + e.msg)


if __name__ == "__main__":
    main()