from apps.llm_engine.models import LlmGlobalConfig, LlmPromptTemplate, LlmGenerateLog
from apps.llm_engine.client import LLMClient
from core.security import aes_decrypt
from core.logger import log_error


class LLMService:

    @staticmethod
    def get_active_config(project_id: int):
        config = LlmGlobalConfig.objects.filter(
            project_id=project_id, is_enable=True, is_default=True
        ).first()
        if not config:
            config = LlmGlobalConfig.objects.filter(
                project_id=project_id, is_enable=True
            ).first()
        return config

    @staticmethod
    def create_client(config: LlmGlobalConfig) -> LLMClient:
        api_key = aes_decrypt(config.api_key)
        return LLMClient(
            api_base=config.api_base,
            api_key=api_key,
            model_name=config.model_name,
            temperature=config.temperature,
            max_tokens=config.max_tokens,
            timeout=config.timeout,
        )

    @staticmethod
    def render_template(template_content: str, variables: dict) -> str:
        result = template_content
        for key, value in variables.items():
            placeholder = '{' + key + '}'
            result = result.replace(placeholder, str(value))
        return result

    @staticmethod
    def get_template(project_id: int, template_type: str) -> LlmPromptTemplate:
        template = LlmPromptTemplate.objects.filter(
            project_id=project_id, template_type=template_type, is_enable=True, is_default=True
        ).first()
        if not template:
            template = LlmPromptTemplate.objects.filter(
                project_id=project_id, template_type=template_type, is_enable=True
            ).first()
        return template

    @staticmethod
    def generate_script(project_id: int, asset_id: int = None,
                        steps_text: str = '', elements_text: str = '',
                        template_type: str = 'script_gen',
                        extra_vars: dict = None) -> dict:
        config = LLMService.get_active_config(project_id)
        if not config:
            return {'success': False, 'content': '', 'cost_time': 0, 'error': '未找到可用的LLM配置'}

        template = LLMService.get_template(project_id, template_type)
        variables = {
            'steps': steps_text,
            'elements': elements_text,
        }
        if extra_vars:
            variables.update(extra_vars)

        if template:
            system_prompt = LLMService.render_template(template.template_content, variables)
        else:
            system_prompt = (
                '你是一个专业的Python自动化测试工程师。请根据以下自然语言步骤，'
                '生成标准的Playwright Python自动化测试脚本。'
                '只返回Python代码，不要包含解释文字。'
                f'\n\n自然语言步骤:\n{steps_text}'
                f'\n\n页面元素:\n{elements_text}'
            )

        client = LLMService.create_client(config)
        messages = [{'role': 'user', 'content': system_prompt}]
        result = client.chat(messages)

        log_entry = LlmGenerateLog.objects.create(
            project_id=project_id,
            asset_id=asset_id,
            template_type=template_type,
            input_content=system_prompt[:1000],
            output_script=result.get('content', ''),
            cost_time=result.get('cost_time', 0),
            status='success' if result.get('success') else 'fail',
            error_msg=result.get('error', ''),
        )

        return {
            'success': result.get('success'),
            'content': result.get('content', ''),
            'cost_time': result.get('cost_time', 0),
            'error': result.get('error', ''),
            'log_id': log_entry.id,
        }
