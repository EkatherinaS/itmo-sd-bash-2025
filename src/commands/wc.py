from commands.cmd import Cmd


class Wc(Cmd):
    def run(self):
        if not self.args and not self.stdin:
            return ""

        text = self.stdin if not self.args else ""

        if self.args:
            text = ""
            for file in self.args:
                try:
                    with open(file, 'r') as f:
                        text += f.read()
                except FileNotFoundError:
                    return f"wc: {file}: No such file or directory\n"

        lines = text.count('\n')
        words = len(text.split())
        chars = len(text)

        return f"{lines} {words} {chars}\n"