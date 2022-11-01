# set current file folder in environment variable
import os
from classes.run import System, get_system

# get current file folder
current_file_folder = os.path.dirname(os.path.abspath(__file__))

if ":" in current_file_folder:
    current_file_folder = current_file_folder[:1].upper(
    ) + current_file_folder[1:]


path = os.environ.get("PATH", "")
if current_file_folder not in path:
    os.environ["PATH"] = current_file_folder + os.pathsep + path

win_cmd = "setx PATH " + f'"{os.environ["PATH"]}"'
linux_cmd = "export PATH=" + f'"{os.environ["PATH"]}"'

# set current file folder in environment variable
if get_system() == System.WINDOWS:
    os.system(win_cmd)
else:
    # save current file folder in .bashrc
    file_path = os.path.join(os.path.expanduser("~"), ".bashrc")
    with open(file_path, "a") as f:
        f.write(linux_cmd)
