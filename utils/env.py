import os

class Env:
    def __init__(self):
        self.file_name = ".env"
        self.env = self.load_env()

    def load_env(self):
        if not os.path.exists(self.file_name):
            return {}
        with open(self.file_name, "r") as f:
            lines = f.readlines()
            env = {}
            for line in lines:
                line = line.strip()
                if line.startswith("#"):
                    continue
                if "=" in line:
                    key, value = line.split("=")
                    env[key] = value
            return env

    def update(self):
        with open(self.file_name, "w") as f:
            for key, value in self.env.items():
                f.write(f"{key}={value}\n")

    def get(self, key):
        return self.env.get(key, None)

    def set(self, key, value):
        self.env[key] = value
        self.update()

    def __getitem__(self, key):
        return self.get(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __contains__(self, key):
        return key in self.env

    def __repr__(self):
        return str(self.env)

    def __str__(self):
        return str(self.env)

    def __len__(self):
        return len(self.env)
