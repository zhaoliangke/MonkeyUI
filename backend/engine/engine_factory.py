from engine.playwright_engine import PlaywrightEngine
from engine.selenium_engine import SeleniumEngine


class EngineFactory:
    ENGINES = {
        'playwright': PlaywrightEngine,
        'selenium': SeleniumEngine,
    }

    @classmethod
    def get_engine(cls, engine_type: str):
        engine_class = cls.ENGINES.get(engine_type)
        if not engine_class:
            raise ValueError(f'不支持的引擎类型: {engine_type}')
        return engine_class()
