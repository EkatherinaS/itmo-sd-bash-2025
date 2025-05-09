class Parser:
    def __init__(self):
        self.position = 0
        self.tokens = []

    def run(self, tokens):
        self.tokens = tokens
        self.position = 0
        return self.parse_pipeline()

    def parse_pipeline(self):
        command = self.parse_command()
        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token.group == 'PIPE':
                self.position += 1
                next_command = self.parse_command()
                new_command = {
                    "CMD": next_command.get("CMD", ""),
                    "STDIN": command
                }
                if "FLAGS" in next_command:
                    new_command["FLAGS"] = next_command["FLAGS"]
                if "OPTIONS" in next_command:
                    new_command["OPTIONS"] = next_command["OPTIONS"]
                if "ARGS" in next_command:
                    new_command["ARGS"] = next_command["ARGS"]
                command = new_command
            else:
                break
        return command

    def parse_command(self):
        result = {
            "CMD": None,
            "FLAGS": [],
            "OPTIONS": [],
            "ARGS": []
        }

        while self.position < len(self.tokens):
            token = self.tokens[self.position]
            if token.group == 'VAR_DECL':
                result["VAR_DECL"] = token.value
            if token.group == "PIPE":
                break
            if token.group == "CMD":
                if result["CMD"] is None:
                    result["CMD"] = token.value
                else:
                    result["ARGS"].append(token.value)
            elif token.group == "FLAGS":
                result["FLAGS"].append(token.value)
            elif token.group == "OPTIONS":
                result["OPTIONS"].append(token.value)
            elif token.group == "ARGUMENT":
                result["ARGS"].append(token.value.strip('"'))
            self.position += 1

        if not result["FLAGS"]:
            del result["FLAGS"]
        if not result["OPTIONS"]:
            del result["OPTIONS"]
        if not result["ARGS"]:
            del result["ARGS"]

        return result