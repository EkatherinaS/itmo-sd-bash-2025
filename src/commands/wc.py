from commands.cmd import Cmd


class Wc(Cmd):
    def run(self):
        if not self.args:
            return ""

        total_lines = 0
        total_words = 0
        total_chars = 0
        results = []

        for file in self.args:
            try:
                with open(file, 'r') as f:
                    content = f.read()
                    lines = content.count('\n')
                    words = len(content.split())
                    chars = len(content)

                    results.append(f"{lines:7} {words:7} {chars:7} {file}")

                    total_lines += lines
                    total_words += words
                    total_chars += chars
            except FileNotFoundError:
                return f"wc: {file}: No such file or directory\n"

        if len(self.args) > 1:
            results.append(f"{total_lines:7} {total_words:7} {total_chars:7} total")

        return "\n".join(results) + "\n"