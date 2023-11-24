import sys
import subprocess


def open_file(filename):
    if sys.platform == "win32":
        # On Windows, standard commands such as 'call' are only recognised when spawning a Command Prompt shell
        subprocess.run(["cmd.exe", "/c", "call", filename])
    else:
        subprocess.run(["open", filename])
