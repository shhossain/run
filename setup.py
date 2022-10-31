# set current file folder in environment variable
import os

# get current file folder
current_file_folder = os.path.dirname(os.path.abspath(__file__))

if ":" in current_file_folder:
    current_file_folder = current_file_folder[:1].upper(
    ) + current_file_folder[1:]


cmd = f'''setx PATH "{current_file_folder};%PATH%"'''
os.system(cmd)
