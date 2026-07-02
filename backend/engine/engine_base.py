from abc import ABC, abstractmethod


class BaseEngine(ABC):

    def __init__(self):
        self.screenshots = []
        self.logs = []
        self.video_path = ''

    @abstractmethod
    def execute(self, script_content: str, env_config: dict, credential: dict = None) -> dict:
        pass

    def setup(self, env_config: dict):
        pass

    def teardown(self):
        pass

    def collect_results(self) -> dict:
        return {
            'screenshots': self.screenshots,
            'logs': '\n'.join(self.logs),
            'video_path': self.video_path,
        }
