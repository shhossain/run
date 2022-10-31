import requests
import os
import platform
import sys
import shutil
from utils.error import Error
from classes.run import get_system, System


class INSTALL:
    def __init__(self, language, version=None):
        self.language = language
        self.version = version
        self.current_os = get_system()
        self.error = Error("INSTALL")

    def install(self):
        if self.language == "python":
            self.install_python()
        elif self.language == "c" or self.language == "cpp" or self.language == "gcc" or self.language == "g++" or self.language == "c++" or self.language == "mingw":
            self.setup_mingw()
        elif self.language == "java":
            self.install_java()
        else:
            self.error.print(f"{self.language} is not supported.")

    def download_file(self, url, path):
        print("Downloading %s" % path)
        with open(path, "wb") as f:
            response = requests.get(url, stream=True)
            total_length = response.headers.get('content-length')

            if total_length is None:
                f.write(response.content)
            else:
                dl = 0
                total_length = int(total_length)
                for data in response.iter_content(chunk_size=4096):
                    dl += len(data)
                    f.write(data)
                    done = int(50 * dl / total_length)
                    sys.stdout.write("\r[%s%s]" %
                                     ('=' * done, ' ' * (50-done)))
                    # print total_length in mb and percentage
                    sys.stdout.write(" %s/%sMB %s%%" %
                                     (round(dl/1000000, 2), round(total_length/1000000, 2), round(dl/total_length*100, 2)))
                    sys.stdout.flush()

    def pc_arch(self):
        if platform.machine().endswith('64'):
            return "64"
        else:
            return "32"

    def install_python(self):
        if self.current_os == System.WINDOWS:
            # https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
            url = "https://www.python.org/ftp/python/{}/python-{}-{}.exe"
            arch = "amd64" if self.pc_arch() == "64" else "x86"
            if self.version is None:
                self.version = "3.11.0"

            url = url.format(self.version, self.version, arch)
            path = "python-{}-{}.exe".format(self.version, arch)
            self.download_file(url, path)
            sys.stdout.write(
                "\nBe sure to tick the 'Add Python to PATH' option.")
            os.startfile(path)
        elif self.current_os == System.LINUX:
            cmd = "sudo apt-get install python3"
            print("Install python3 with the following command:")
            print(cmd)

    def setup_mingw(self):
        if self.current_os == System.WINDOWS:
            url = "https://github.com/nishat48/minimalist/raw/main/mingw-get-setup_2.exe"
            path = "mingw-get-setup_2.exe"
            self.download_file(url, path)
            tutorial_url = "https://www.geeksforgeeks.org/installing-mingw-tools-for-c-c-and-changing-environment-variable/"
            print(f"\nFollow this tutorial to install mingw: {tutorial_url}")
            os.startfile(tutorial_url)
            os.startfile(path)

        elif self.current_os == System.LINUX:
            cmd = "sudo apt-get install mingw-w64"
            print("Install mingw-w64 with the following command:")
            print(cmd)
    
    def install_java(self):
        if self.current_os == System.WINDOWS:
            pass
