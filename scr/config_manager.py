class ConfigManager:
    def __init__(self):
        self.config = {
            'count_of_cities': None,
            'size_of_map': None,
            'count_of_generation': None,
            'count_of_nested_generation': None,
            'logging_enabled': None
        }

    def load_config(self, file_path):
        with open(file_path, 'r') as file:
            for line in file:
                if ':' not in line:
                    continue
                key, value = line.strip().split(':', 1)
                key = key.strip()
                value = value.strip()
                if key == 'count_of_cities':
                    self.config['count_of_cities'] = int(value)
                elif key == 'size_of_map':
                    self.config['size_of_map'] = eval(value)
                elif key == 'count_of_generation':
                    self.config['count_of_generation'] = int(value)
                elif key == 'count_of_nested_generation':
                    self.config['count_of_nested_generation'] = int(value)
                elif key == 'logging':
                    self.config['logging_enabled'] = value.lower() == 'true'

    def get(self, key, default=None):
        return self.config.get(key, default)
