import requests
import time
from core.logger import log_error


class LLMClient:

    def __init__(self, api_base: str, api_key: str, model_name: str = '',
                 temperature: float = 0.7, max_tokens: int = 4096, timeout: int = 60):
        self.api_base = api_base.rstrip('/')
        self.api_key = api_key
        self.model_name = model_name
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    def chat(self, messages: list, system_prompt: str = '') -> dict:
        url = f'{self.api_base}/chat/completions'
        headers = {
            'Authorization': f'Bearer {self.api_key}',
            'Content-Type': 'application/json',
        }
        payload = {
            'model': self.model_name,
            'messages': messages,
            'temperature': self.temperature,
            'max_tokens': self.max_tokens,
        }
        if system_prompt:
            payload['messages'].insert(0, {'role': 'system', 'content': system_prompt})

        for attempt in range(2):
            try:
                start_time = time.time()
                resp = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
                elapsed = time.time() - start_time
                if resp.status_code == 200:
                    data = resp.json()
                    content = data['choices'][0]['message']['content']
                    return {'success': True, 'content': content, 'cost_time': elapsed}
                else:
                    if attempt == 0:
                        continue
                    return {
                        'success': False,
                        'content': '',
                        'cost_time': elapsed,
                        'error': f'API返回状态码 {resp.status_code}: {resp.text[:500]}',
                    }
            except requests.Timeout:
                if attempt == 0:
                    continue
                return {'success': False, 'content': '', 'cost_time': 0, 'error': '请求超时'}
            except Exception as e:
                if attempt == 0:
                    continue
                log_error(f'LLM调用异常: {str(e)}')
                return {'success': False, 'content': '', 'cost_time': 0, 'error': str(e)}

        return {'success': False, 'content': '', 'cost_time': 0, 'error': '未知错误'}

    def test_connectivity(self) -> dict:
        models_url = f'{self.api_base}/models'
        headers = {'Authorization': f'Bearer {self.api_key}'}
        try:
            resp = requests.get(models_url, headers=headers, timeout=10)
            if resp.status_code in (200, 401, 403):
                return {'available': True, 'message': '模型连接正常'}
            return {'available': False, 'message': f'连接异常: HTTP {resp.status_code}'}
        except requests.Timeout:
            return {'available': False, 'message': '连接超时'}
        except Exception as e:
            return {'available': False, 'message': str(e)}
