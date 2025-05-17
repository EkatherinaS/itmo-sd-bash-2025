import os
from datetime import datetime
from commands.cmd import Cmd


class Ls(Cmd):
    def run(self):
        list = ""
        dir = os.path.abspath(os.curdir)
        list += f"\n Каталог: {dir}\n\n"

        list += "| {:<7}| {:>16} | {:>10} | {:<}\n".format(
            "Mode", "LastWriteTime", "Length", "Name"
            )
        list += "|{:-<8}|{:-<18}|{:-<12}|{:-<10}\n".format(
                "", "", "", ""
            )
        
        for item in os.listdir(dir):
            item_path = os.path.join(dir, item)
            stat = os.stat(item_path)
            
            mode = "d---" if os.path.isdir(item_path) else "-a---"
            last_write_time = datetime.fromtimestamp(stat.st_mtime).strftime('%d.%m.%Y %H:%M')
            size = str(stat.st_size) if os.path.isfile(item_path) else ""

            list += "| {:<7}| {:>16} | {:>10} | {:<}\n".format(
                    mode,
                    last_write_time,
                    size,
                    item
                )
        return list + '\n'
