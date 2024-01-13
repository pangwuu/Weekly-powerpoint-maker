import sys
import subprocess
import os


def open_file(filename):
    if sys.platform == "win32":
        # On Windows, opening a file is a blocking command, so the program won't continue until the file
        # is closed. Instead, call a batch script that opens the file in a separate process using 'start'.
        subprocess.run([f"{os.path.dirname(__file__)}/open.bat", filename])
    else:
        subprocess.run(["open", filename])
