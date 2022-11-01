from classes import INSTALL, RUN
from utils import Error
import os
import sys
import re

# examples
# main.py <file> -i <input> -o <output> -t <timeout> -e <expected> -o <compiler_options>

# run install <python|c|cpp|java> -v <version>

# -i, --input, -o, --output, -t, --timeout, -v, --version (optional)


def get_version():
    # current folder path
    current_folder_path = os.path.dirname(os.path.abspath(__file__))
    return open(os.path.join(current_folder_path, "VERSION"), "r").read()


class Parser:
    def __init__(self, *args, **kw) -> None:
        self.args: list = args
        self.kw = kw
        self.language = None
        self.error = Error("Parser")
        self.language = None
        self.version = None

        if len(self.args) == 0:
            self.error.print("No arguments given")

        if self.args[0] == "-v" or self.args[0] == "--version":
            txt = f"Run {get_version()}"
            print(txt)
            return
        elif self.args[0] == "-h" or self.args[0] == "--help":
            self.run_help()
            return

        elif self.args[0] == "install":
            # next arg is language
            idx = args.index("install")
            self.language = args[idx+1]
            args_len = len(args) - 1

            # check if version is specified
            if (idx+1) != args_len:
                v = args[idx+2]
                if "-v" in v or "--version" in v:
                    self.version = args[idx+3]
                else:
                    self.version = v

                if "help" in self.version or "-h" in self.version:
                    self.install_help()

            # install
            self.install()
        else:
            self.run()

    def install(self):
        install = INSTALL(self.language, self.version)
        install.install()

    def fix_file_path(self):
        path = ""
        if not os.path.isfile(self.args[0]):
            for i in range(len(self.args)):
                if self.args[i].startswith("-"):
                    break
                path += self.args[i] + " "
        else:
            path = self.args[0]

        if path[-1] == " ":
            path = path[:-1]

        return path

    def run(self):
        file_path = self.fix_file_path()
        input_file = None
        output_file = None
        expeted_output_file = None
        timeout = None
        compiler_options = None

        keys = ["-i", "--input", "-o", "--output", "-t",
                "--timeout", "-e", "--expected", "-c", "--options"]
        op = {i: None for i in keys}
        for i in range(1, len(self.args)-1):
            if "help" in self.args[i] or "-h" in self.args[i]:
                self.run_help()
                return
            op[self.args[i]] = self.args[i+1]
            i += 1

        if op["-i"] is not None:
            input_file = op["-i"]
        elif op["--input"] is not None:
            input_file = op["--input"]

        if op["-o"] is not None:
            output_file = op["-o"]
        elif op["--output"] is not None:
            output_file = op["--output"]

        if op["-t"] is not None:
            timeout = op["-t"]
        elif op["--timeout"] is not None:
            timeout = op["--timeout"]

        if op["-e"] is not None:
            expeted_output_file = op["-e"]
        elif op["--expected"] is not None:
            expeted_output_file = op["--expected"]

        if op["-c"] is not None:
            compiler_options = op["-c"]
        elif op["--options"] is not None:
            compiler_options = op["--options"]

        run = RUN(file_path, input_file=input_file, output_file=output_file, timeout=timeout,
                  compiler_options=compiler_options, expected_output=expeted_output_file)
        run.run()

        if output_file is None:
            print(run.output)
            print()

        if expeted_output_file is not None:
            self.match_output(run.expected_output, run.output)

        print(f"[Finished in {round(run.execution_time, 2)} seconds]")
        print(f"[Memory used: {round(run.memory_usage/1024/1024, 2)} MB]")

    def match_output(self, expected_output_file, output):
        elines = expected_output_file.splitlines()
        olines = output.splitlines()

        if len(elines) != len(olines):
            self.error.print("Output does not match expected output")

        for i in range(len(elines)):
            if elines[i] != olines[i]:
                self.error.print("Output does not match expected output")

        print("Output matches expected output")

    def install_help(self):
        print("install <language> -v <version>")

    def run_help(self):
        print("run <file> -i <input> -o <output> -t <timeout> -e <expected> -o <compiler_options>")


if __name__ == "__main__":
    args = sys.argv[1:]
    Parser(*args)
