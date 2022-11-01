import json
import enum
import sys
import os
import time
import shutil
import subprocess
from subprocess import PIPE, Popen
from utils.error import Error
from utils.env import Env
import psutil


current_file_path = os.path.dirname(os.path.realpath(__file__))

languages_path = os.path.join(current_file_path, "languages.json")
with open(languages_path, "r") as f:
    languages = json.load(f)


def detect_language(file_name):
    if file_name[-1] == '"':
        file_name = file_name[:-1]

    for language in languages:
        if file_name.endswith(languages[language]["extention"]):
            return language
    return None


def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss

class System(enum.Enum):
    WINDOWS = 1
    LINUX = 2
    MAC = 3


def get_system():
    if sys.platform.startswith("win"):
        return System.WINDOWS
    elif sys.platform.startswith("linux"):
        return System.LINUX
    elif sys.platform.startswith("darwin"):
        return System.MAC
    else:
        return None


class RUN:
    def __init__(self, file_path, **kw):
        if " " in file_path:
            file_path = f'"{file_path}"'





        self.path = file_path
        self.language = detect_language(file_path)
        self.base_name = os.path.basename(file_path).split(".")[0]

        self.current_os = get_system()
        self.error = Error(file_path)
        self.env = Env()

        self.execution_time = -1
        self.memory_usage = -1
        self.compiler_error_message = None
        self.runtime_error_message = None
        self.output = None

        self.input_file = kw.get("input_file", None)
        self.output_file = kw.get("output_file", None)
        self.expected_output_file = kw.get("expected_output", None)
        self.compiler_options = kw.get("compiler_options", None)
        self.timeout = kw.get("timeout", None)

        if self.timeout is not None:
            self.timeout = float(self.timeout)

        self.input = None
        self.output = None
        self.expected_output = None
        self.return_code = None
        self.exit_code = None

        self.read_expected_output()

    def read_input(self):
        if self.input_file is not None:
            with open(self.input_file, "r") as f:
                self.input = f.read()
                return True
        return None

    def read_expected_output(self):
        if self.expected_output_file is not None:
            with open(self.expected_output_file, "r") as f:
                self.expected_output = f.read()
                return True
        return None

    def write_output(self):
        if self.output_file is not None:
            with open(self.output_file, "w") as f:
                f.write(self.output.replace("\r", ""))
                return True
        return None

    def run(self):
        if self.language == "python":
            self.run_python()
        elif self.language == "c++":
            self.run_cpp()
        elif self.language == "c":
            self.run_c()
        elif self.language == "java":
            self.run_java()

    def run_python(self):
        # rading input
        self.read_input()
        iinput = self.input.encode("utf-8") if self.input else None

        # setting python path
        cmd = ""
        if self.current_os == System.WINDOWS:
            cmd = f"python"
        else:
            cmd = f"python3"

        self.executable_exists(cmd)

        cmd += f" {self.path}"

        # running python code
        proc = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        # checking for timeout
        try:
            mstart = process_memory()
            start = time.time()
            self.output, self.runtime_error_message = proc.communicate(
                iinput, timeout=self.timeout)
            self.execution_time = time.time() - start
            self.memory_usage = process_memory() - mstart
            self.output = self.output.decode("utf-8").strip()
        except subprocess.TimeoutExpired as e:
            proc.kill()
            self.runtime_error_message = f"Time Limit Exceeded. Given time limit is {self.timeout} seconds."
            self.execution_time = self.timeout
            self.error.print(self.runtime_error_message)

        # checking for runtime error
        self.return_code = proc.returncode
        if self.return_code != 0:
            self.error.print(self.runtime_error_message.decode("utf-8"))

        # writing output
        self.write_output()



    def run_cpp(self):
        # setting compiler options
        cmd = "g++"
        self.executable_exists("g++")
        if self.compiler_options is not None:
            cmd += " " + self.compiler_options
        cmd += f" {self.path} -o {self.base_name}"
        _, e = Popen(
            cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        # checking for compiler error
        if e:
            self.compiler_error_message = e.decode()
            self.error.print(self.compiler_error_message)

        # setting execution command
        cmd = ""
        if self.current_os == System.WINDOWS:
            cmd = f"{self.base_name}.exe"
        else:
            cmd = f"./{self.base_name}"

        # reading input
        self.read_input()
        iinput = self.input.encode("utf-8") if self.input else None

        # print("cmd", cmd)
        # running executable
        p = Popen(cmd, shell=True, stdout=PIPE,
                  stderr=PIPE, stdin=PIPE)
        # checking for timeout
        try:
            mstart = process_memory()
            start = time.time()
            self.output, self.runtime_error_message = p.communicate(
                iinput, timeout=self.timeout)
            self.execution_time = time.time() - start
            self.memory_usage = process_memory() - mstart
            self.output = self.output.decode("utf-8").strip()
        except subprocess.TimeoutExpired as e:
            p.kill()
            self.runtime_error_message = f"Time Limit Exceeded. Given time limit is {self.timeout} seconds."
            self.execution_time = self.timeout
            self.error.print(self.runtime_error_message)

        # checking for runtime error
        self.return_code = p.returncode
        if self.return_code != 0:
            self.error.print(self.runtime_error_message.decode("utf-8"))

        # writing output
        self.write_output()

    def run_c(self):
        # setting compiler options
        cmd = "gcc"
        self.executable_exists(cmd)
        if self.compiler_options is not None:
            cmd += " " + self.compiler_options
        cmd += f" {self.path} -o {self.base_name}"
        _, e = Popen(
            cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        # checking for compiler error
        if e:
            self.compiler_error_message = e.decode()
            self.error.print(self.compiler_error_message)

        # setting execution command
        cmd = ""
        if self.current_os == System.WINDOWS:
            cmd = f"{self.base_name}.exe"
        else:
            cmd = f"./{self.base_name}"

        # reading input
        self.read_input()
        iinput = self.input.encode("utf-8") if self.input else None

        # running executable
        p = Popen(cmd, shell=True, stdout=PIPE,
                  stderr=PIPE, stdin=PIPE)
        # checking for timeout
        try:
            mstart = process_memory()
            start = time.time()
            self.output, self.runtime_error_message = p.communicate(
                iinput, timeout=self.timeout)
            self.execution_time = time.time() - start
            self.memory_usage = process_memory() - mstart
            self.output = self.output.decode("utf-8").strip()
        except subprocess.TimeoutExpired as e:
            p.kill()
            self.runtime_error_message = f"Time Limit Exceeded. Given time limit is {self.timeout} seconds."
            self.execution_time = self.timeout
            self.error.print(self.runtime_error_message)

        # checking for runtime error
        self.return_code = p.returncode
        if self.return_code != 0:
            self.error.print(self.runtime_error_message.decode("utf-8"))

        # writing output
        self.write_output()

    def run_java(self):
        # setting compiler options
        cmd = "javac"
        self.executable_exists(cmd)
        if self.compiler_options is not None:
            cmd += " " + self.compiler_options
        cmd += f" {self.path}"
        _, e = Popen(
            cmd, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        # checking for compiler error
        if e:
            self.compiler_error_message = e.decode()
            self.error.print(self.compiler_error_message)

        # setting execution command
        cmd = ""
        if self.current_os == System.WINDOWS:
            cmd = f"java {self.base_name}"
        else:
            cmd = f"java {self.base_name}"

        # reading input
        self.read_input()
        iinput = self.input.encode("utf-8") if self.input else None

        # running executable
        p = Popen(cmd, shell=True, stdout=PIPE,
                  stderr=PIPE, stdin=PIPE)
        # checking for timeout
        try:
            mstart = process_memory()
            start = time.time()
            self.output, self.runtime_error_message = p.communicate(
                iinput, timeout=self.timeout)
            self.execution_time = time.time() - start
            self.memory_usage = process_memory() - mstart
            self.output = self.output.decode("utf-8").strip()
        except subprocess.TimeoutExpired as e:
            p.kill()
            self.runtime_error_message = f"Time Limit Exceeded. Given time limit is {self.timeout} seconds."
            self.execution_time = self.timeout
            self.error.print(self.runtime_error_message)

        # checking for runtime error
        self.return_code = p.returncode
        if self.return_code != 0:
            self.error.print(self.runtime_error_message)

        # writing output
        self.write_output()

    def executable_exists(self, cmd):
        env_cmd = self.env.get(cmd)
        if env_cmd is None:
            if shutil.which(cmd) is None:
                self.compiler_error_message = f"{cmd} is not installed. or not in path."
                self.error.print(self.compiler_error_message)
            else:
                self.env[cmd] = cmd

    def cleanup(self):
        if self.current_os == System.WINDOWS:
            os.system(f"del {self.base_name}.exe")
        else:
            os.system(f"rm {self.base_name}")
