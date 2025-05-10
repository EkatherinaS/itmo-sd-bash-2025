from commands.echo import Echo


class CmdFactory:

    def __init__(self):
        self.commands = {
            #"cat": Cat,
            "echo": Echo,
            #"wc": Wc,
            #"pwd": Pwd,
            #"exit": Exit,
            #"grep": Grep
        }

    def get(self, cmd_name):
        if cmd_name is None: cmd_name = "echo"
        return self.commands[cmd_name]
