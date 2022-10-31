# set current file folder in environment variable
import os

# get current file folder
current_file_folder = os.path.dirname(os.path.abspath(__file__))
# set current file folder in path environment variable

cmd = "setx path \"%path%;{}\"".format(current_file_folder)
os.system(cmd)
