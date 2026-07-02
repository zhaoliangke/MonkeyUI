import re


class NLPParser:

    ACTION_PATTERNS = {
        'click': r'(?:点击|单击|click)\s*(?:元素|按钮|链接)?\s*[\[(]?([^)\]]+)[\])]?',
        'fill': r'(?:输入|填写|fill|type)\s*(?:内容|文本|值)?\s*[\[(]?([^)\]]+)[\])]?\s*(?:到|在|至)?\s*[\[(]?([^)\]]+)[\])]?',
        'select': r'(?:选择|select)\s*(?:选项|值)?\s*[\[(]?([^)\]]+)[\])]?\s*(?:从|在)?\s*[\[(]?([^)\]]+)[\])]?',
        'navigate': r'(?:导航|跳转|打开|go\s*to)\s*(?:到|至|URL)?\s*[\[(]?([^)\]]+)[\])]?',
        'assert_visible': r'(?:验证|断言|assert)\s*(?:元素|可见)?\s*[\[(]?([^)\]]+)[\])]?\s*(?:可见|存在|显示|visible)',
        'assert_text': r'(?:验证|断言|assert)\s*(?:文本|内容)?\s*[\[(]?([^)\]]+)[\])]?\s*(?:包含|等于|为)\s*[\[(]?([^)\]]+)[\])]?',
        'wait': r'(?:等待|wait)\s*(?:(\d+)\s*)?(?:秒|s)?',
    }

    @classmethod
    def parse_step(cls, step_text: str) -> dict:
        result = {
            'action_type': '',
            'element_name': '',
            'param': '',
            'assert_text': '',
        }

        for action_type, pattern in cls.ACTION_PATTERNS.items():
            match = re.search(pattern, step_text, re.IGNORECASE)
            if match:
                result['action_type'] = action_type
                if action_type == 'click':
                    result['element_name'] = match.group(1) or ''
                elif action_type == 'fill':
                    result['param'] = match.group(1) or ''
                    if match.lastindex and match.lastindex >= 2:
                        result['element_name'] = match.group(2) or ''
                    else:
                        if result['param'] and not result['element_name']:
                            result['element_name'] = result['param']
                            result['param'] = ''
                elif action_type == 'select':
                    result['param'] = match.group(1) or ''
                    if match.lastindex and match.lastindex >= 2:
                        result['element_name'] = match.group(2) or ''
                elif action_type == 'navigate':
                    result['param'] = match.group(1) or ''
                elif action_type == 'assert_visible':
                    result['element_name'] = match.group(1) or ''
                elif action_type == 'assert_text':
                    result['element_name'] = match.group(1) or ''
                    if match.lastindex and match.lastindex >= 2:
                        result['assert_text'] = match.group(2) or ''
                elif action_type == 'wait':
                    result['param'] = match.group(1) or '1'
                break

        return result

    @classmethod
    def parse_steps(cls, steps: list) -> list:
        return [cls.parse_step(s.get('step_content', '') if isinstance(s, dict) else s) for s in steps]
