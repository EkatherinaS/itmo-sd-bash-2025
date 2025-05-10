from commands.cmd import Cmd


class Cat(Cmd):
    def run(self):
        if not self.args:
            return ""

        content = []
        for file in self.args:
            try:
                with open(file, 'r') as f:
                    content.append(f.read())
            except FileNotFoundError:
                return f"cat: {file}: No such file or directory\n"

        return "\n".join(content) + "\n"