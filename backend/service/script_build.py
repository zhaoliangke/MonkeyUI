from service.nlp_parse import NLPParser


class ScriptBuilder:

    @staticmethod
    def build_playwright_script(steps: list) -> str:
        lines = [
            'from playwright.sync_api import sync_playwright',
            '',
            'def run(playwright):',
            '    browser = playwright.chromium.launch(headless=True)',
            '    context = browser.new_context()',
            '    page = context.new_page()',
        ]

        parsed_steps = NLPParser.parse_steps(steps)
        for i, parsed in enumerate(parsed_steps):
            step_text = steps[i].get('step_content', '') if isinstance(steps[i], dict) else str(steps[i])
            lines.append('')
            lines.append(f'    # {step_text}')

            action = parsed.get('action_type', '')
            element = parsed.get('element_name', '')
            param = parsed.get('param', '')

            if action == 'navigate':
                lines.append(f'    page.goto("{param}")')
            elif action == 'click':
                loc = ScriptBuilder._resolve_locator(element)
                lines.append(f'    page.click("{loc}")')
            elif action == 'fill':
                loc = ScriptBuilder._resolve_locator(element)
                lines.append(f'    page.fill("{loc}", "{param}")')
            elif action == 'select':
                loc = ScriptBuilder._resolve_locator(element)
                lines.append(f'    page.select_option("{loc}", "{param}")')
            elif action == 'wait':
                lines.append(f'    page.wait_for_timeout({int(param) * 1000 if param else 1000})')
            elif action == 'assert_visible':
                loc = ScriptBuilder._resolve_locator(element)
                lines.append(f'    assert page.is_visible("{loc}"), "{element} 不可见"')
            elif action == 'assert_text':
                loc = ScriptBuilder._resolve_locator(element)
                assert_text = parsed.get('assert_text', '')
                lines.append(f'    assert page.inner_text("{loc}") == "{assert_text}"')
            else:
                lines.append(f'    page.wait_for_timeout(1000)  # {step_text}')

        lines.append('')
        lines.append('    browser.close()')
        lines.append('')
        lines.append('')
        lines.append('with sync_playwright() as playwright:')
        lines.append('    run(playwright)')

        return '\n'.join(lines)

    @staticmethod
    def _resolve_locator(element_name: str) -> str:
        if element_name.startswith('#') or element_name.startswith('.') or element_name.startswith('['):
            return element_name
        return f'text={element_name}'
