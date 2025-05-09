from interpreter.expression import Expression
from variables import Variables


class Interpreter:
    def __init__(self):
        self.root = None

    def run(self, ast):
        if "VAR_DECL" in ast:
            return self.var_decl_interpret(ast)
        else:
            self.root = self.create_expression(ast)
            return self.root.interpret()

    def var_decl_interpret(self, data):
        Variables().add(data["VAR_DECL"])
        return ""

    def create_expression(self, data):
        cmd = data["CMD"]
        flags = data.get("FLAGS", [])
        options = data.get("OPTIONS", [])
        args = data.get("ARGS", [])
        stdin = None

        if "STDIN" in data:
            stdin = self.create_expression(data["STDIN"])

        return Expression(cmd, flags, options, args, stdin)