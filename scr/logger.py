import os
from datetime import datetime

class Logger:
    def __init__(self, enabled):
        self.enabled = enabled
        self.file = None
        if self.enabled:
            logs_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
            os.makedirs(logs_dir, exist_ok=True)
            log_name = datetime.now().strftime('%Y-%m-%d_%H-%M-%S') + '.log'
            log_path = os.path.join(logs_dir, log_name)
            self.file = open(log_path, 'w')

    def log(self, message):
        if self.enabled and self.file:
            self.file.write(str(message) + '\n')

    def close(self):
        if self.enabled and self.file:
            self.file.close()
