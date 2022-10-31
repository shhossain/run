import datetime

class Error:
    def __init__(self, file_path) -> None:
        self.file_path = file_path
        self.current_time = datetime.datetime.now().strftime("%H:%M:%S")

    def print(self, error_msg):
        raise Exception(
            f"[Time {self.current_time}] '{self.file_path}' : {error_msg}")
