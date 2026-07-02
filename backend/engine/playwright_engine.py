from engine.engine_base import BaseEngine


class PlaywrightEngine(BaseEngine):

    def execute(self, script_content: str, env_config: dict, credential: dict = None) -> dict:
        try:
            from playwright.sync_api import sync_playwright
            env_url = env_config.get('base_url', '')

            with sync_playwright() as p:
                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                page = context.new_page()

                if env_url:
                    page.goto(env_url, wait_until='networkidle')

                exec_globals = {
                    'page': page,
                    'browser': browser,
                    'context': context,
                }
                exec(script_content, exec_globals)

                screenshot_path = f'/tmp/screenshot_{__import__("uuid").uuid4().hex[:8]}.png'
                page.screenshot(path=screenshot_path)
                self.screenshots.append(screenshot_path)
                self.logs.append('Playwright脚本执行完成')

                browser.close()
                return {'success': True, 'message': '执行成功', 'screenshots': [screenshot_path]}
        except Exception as e:
            self.logs.append(f'执行失败: {str(e)}')
            return {'success': False, 'message': str(e), 'screenshots': []}
