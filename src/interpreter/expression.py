from commands.cmd_factory import CmdFactory

class Expression:

    def __init__(self, cmd, flags, options, args, stdin):
        self.cmd = CmdFactory().get(cmd)
        self.flags = [] if flags is None else flags
        self.options = [] if options is None else options
        self.args = [] if args is None else args
        self.stdin = stdin

    def interpret(self):
        if self.cmd is None:
            return None

        stdin_res = None
        if not self.stdin is None:
            stdin_res = self.stdin.interpret()

        cmd = self.cmd(self.args, self.flags, self.options, stdin_res)
        return cmd.run()
