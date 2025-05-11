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

    def get(self, string):
        return self.values.get(string)

    def add(self, data):
        if '=' not in data:
            raise ValueError("Data must be in 'key=value' format")

        key, value = data.split('=', 1)
        self.values[key.strip()] = value.strip()
        return self