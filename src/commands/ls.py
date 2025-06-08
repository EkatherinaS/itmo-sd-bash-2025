import os
from datetime import datetime
from commands.cmd import Cmd


class Ls(Cmd):
    def __init__(self, args, flags, options, stdin):
        super().__init__(args, flags, options, stdin)

    def run(self):
        targets = []
        if not self.args:
            targets.append((os.path.abspath(os.curdir), True))
        else:
            for path in self.args:
                abs_path = os.path.abspath(path)
                if os.path.isdir(abs_path):
                    targets.append((abs_path, True))
                else:
                    targets.append((abs_path, False))
        
        output = ""
        for path, is_directory in targets:
            if not is_directory:
                try:
                    stat = os.stat(path)
                    output += "\n"
                    output += "| {:<7}| {:>16} | {:>10} | {:<}\n".format(
                        "Mode", "LastWriteTime", "Length", "Name"
                    )
                    output += "|{:-<8}|{:-<18}|{:-<12}|{:-<10}\n".format(
                        "", "", "", ""
                    )
                    
                    mode = "-a---"
                    last_write_time = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')
                    size = str(stat.st_size)
                    filename = os.path.basename(path)
                    
                    output += "| {:<7}| {:>16} | {:>10} | {:<}\n".format(
                        mode,
                        last_write_time,
                        size,
                        filename
                    )
                except (OSError, IOError) as e:
                    output += f"ls: {path}: {e.strerror.lower()}\n"
                continue
            
            header = f"\nКаталог: {path}\n\n"
            output += header
            
            output += "| {:<7}| {:>16} | {:>10} | {:<}\n".format(
                "Mode", "LastWriteTime", "Length", "Name"
            )
            output += "|{:-<8}|{:-<18}|{:-<12}|{:-<10}\n".format(
                "", "", "", ""
            )

            try:
                items = os.listdir(path)
                items = sorted(items)
                
                if not items:
                    output += "\n"
                    continue
                    
                for item in items:
                    if item.startswith('.'):
                        continue
                        
                    item_path = os.path.join(path, item)
                    try:
                        stat = os.stat(item_path)
                        
                        mode = "d---" if os.path.isdir(item_path) else "-a---"
                        last_write_time = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')
                        size = str(stat.st_size) if os.path.isfile(item_path) else ""

                        output += "| {:<7}| {:>16} | {:>10} | {:<}\n".format(
                            mode,
                            last_write_time,
                            size,
                            item
                        )
                    except (OSError, IOError):
                        continue
            except (FileNotFoundError, NotADirectoryError, PermissionError) as e:
                if isinstance(e, FileNotFoundError):
                    output += f"ls: {path}: No such file or directory\n"
                elif isinstance(e, NotADirectoryError):
                    output += f"ls: {path}: Not a directory\n"
                else:
                    output += f"ls: {path}: Permission denied\n"
        
        if output.endswith("\n\n"):
            output = output[:-1]
        
        return output + '\n'