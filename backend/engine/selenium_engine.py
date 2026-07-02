from engine.engine_base import BaseEngine


class SeleniumEngine(BaseEngine):

    def execute(self, script_content: str, env_config: dict, credential: dict = None) -> dict:
        try:
            env_url = env_config.get('base_url', '')

            exec_globals = {
                'env_url': env_url,
                'env_config': env_config,
                'credential': credential,
            }
            self.logs.append('Selenium引擎已加载（需要安装selenium和webdriver）')
            exec(script_content, exec_globals)

            return {'success': True, 'message': 'Selenium脚本执行完成'}
        except Exception as e:
            self.logs.append(f'Selenium执行失败: {str(e)}')
            return {'success': False, 'message': str(e), 'screenshots': []}
