import re

def singleton(class_):
    instances = {}

    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]

    return getinstance


@singleton
class Variables:
    def __init__(self):
        self.values = {}
        self.re_use = re.compile(r'\$([a-zA-Z_][a-zA-Z0-9_]*)|\$\{([^}]*)\}')

    def replace(self, string):

        def replacer(match):
            # group(1) - для $var, group(2) - для ${var}
            var_name = match.group(1) if match.group(1) is not None else match.group(2)
            return str(self.values.get(var_name, match.group(0)))

        return self.re_use.sub(replacer, string)

    def add(self, data):
        if '=' not in data:
            raise ValueError("Data must be in 'key=value' format")

        key, value = data.split('=', 1)
        self.values[key.strip()] = value.strip()
        return self