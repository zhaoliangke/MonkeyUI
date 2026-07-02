import json
import re
from datetime import datetime
from apps.crawler.models import KbCrawlerTask
from apps.environment.models import KbEnv, KbCredential
from apps.element_lib.models import KbElement
from apps.knowledge.models import KbAsset, KbAssetStep
from core.middleware import get_current_project_id
from core.security import aes_decrypt
from core.logger import log_error


class CrawlerService:

    @staticmethod
    def test_connectivity(env_id: int, credential_id: int = None):
        env = KbEnv.objects.filter(id=env_id).first()
        if not env:
            return {'success': False, 'message': '环境不存在'}
        if env.env_type == 'production':
            return {'success': False, 'message': '生产环境禁止爬取'}
        return {'success': True, 'message': '连通性正常'}

    @staticmethod
    def should_filter_element(tag_name: str, attrs: dict, styles: dict) -> bool:
        if attrs.get('aria-hidden') == 'true':
            return True
        display = styles.get('display', '')
        visibility = styles.get('visibility', '')
        if display == 'none' or visibility == 'hidden':
            return True
        if tag_name in ('script', 'style', 'noscript', 'iframe', 'svg', 'path'):
            return True
        return False

    @staticmethod
    def generate_locator(tag_name: str, attrs: dict) -> tuple:
        element_id = attrs.get('id', '')
        name = attrs.get('name', '')
        class_name = attrs.get('class', '')
        text = attrs.get('text', '')[:50]
        placeholder = attrs.get('placeholder', '')
        data_testid = attrs.get('data-testid', '')

        if data_testid:
            return ('css', f'[data-testid="{data_testid}"]')
        if element_id:
            return ('css', f'#{element_id}')
        if name:
            return ('css', f'[name="{name}"]')
        if placeholder:
            return ('css', f'[placeholder="{placeholder}"]')
        if text and tag_name in ('a', 'button', 'span'):
            return ('xpath', f'//{tag_name}[contains(text(), "{text}")]')
        if class_name:
            first_class = class_name.split()[0]
            return ('css', f'{tag_name}.{first_class}')
        return ('css', tag_name)

    @staticmethod
    def parse_elements_from_html(html_content: str, base_url: str) -> dict:
        elements = []
        steps = []
        interactive_tags = {
            'input': 'fill', 'textarea': 'fill', 'select': 'select',
            'button': 'click', 'a': 'click',
        }

        for tag, action in interactive_tags.items():
            pattern = rf'<{tag}\b[^>]*>'
            for match in re.finditer(pattern, html_content):
                tag_text = match.group()
                attrs = {}
                for attr_name in ('id', 'name', 'class', 'placeholder', 'data-testid', 'type', 'href', 'value'):
                    m = re.search(rf'{attr_name}="([^"]*)"', tag_text)
                    if m:
                        attrs[attr_name] = m.group(1)
                element_name = attrs.get('name') or attrs.get('id') or attrs.get('placeholder') or f'{tag}_{match.start()}'
                locator_type, locator_value = CrawlerService.generate_locator(tag, attrs)
                elements.append({
                    'element_name': element_name,
                    'element_type': tag,
                    'locator_type': locator_type,
                    'locator_value': locator_value,
                    'page_name': base_url,
                })
                step_content = f'{action} 元素[{element_name}]' + (f' 输入[{attrs.get("placeholder", "")}]' if action == 'fill' else '')
                steps.append({
                    'sort_num': len(steps) + 1,
                    'step_content': step_content,
                    'element_name': element_name,
                    'action_type': action,
                    'param': attrs.get('value', attrs.get('placeholder', '')),
                    'assert_text': '',
                    'is_valid': True,
                })

        return {'elements': elements, 'steps': steps}

    @staticmethod
    def incremental_compare(project_id: int, new_elements: list, page_name: str) -> dict:
        old_keys = set(KbElement.objects.filter(
            project_id=project_id, page_name=page_name
        ).values_list('element_name', flat=True))

        new_keys = {e['element_name'] for e in new_elements}
        added = new_keys - old_keys
        removed = old_keys - new_keys
        unchanged = new_keys & old_keys

        return {
            'added': list(added),
            'removed': list(removed),
            'unchanged': list(unchanged),
            'added_count': len(added),
            'removed_count': len(removed),
            'unchanged_count': len(unchanged),
        }

    @staticmethod
    def execute_crawl(task_id: int):
        task = KbCrawlerTask.objects.filter(id=task_id).first()
        if not task:
            return
        task.status = 'running'
        task.start_time = datetime.now()
        task.result_msg = '正在加载页面...'
        task.save()

        try:
            from playwright.sync_api import sync_playwright
            project_id = task.project_id

            env = KbEnv.objects.filter(id=task.env_id).first() if task.env_id else None
            credential = KbCredential.objects.filter(id=task.credential_id).first() if task.credential_id else None

            with sync_playwright() as p:
                task.result_msg = '启动浏览器...'
                task.save()

                browser = p.chromium.launch(headless=True)
                context = browser.new_context()
                if credential:
                    if credential.cookie:
                        cookies = json.loads(aes_decrypt(credential.cookie))
                        context.add_cookies(cookies)

                task.result_msg = '加载页面中...'
                task.save()

                page = context.new_page()
                page.goto(task.url, wait_until='networkidle', timeout=30000)

                task.result_msg = '解析页面元素...'
                task.save()

                html_content = page.content()

                result = CrawlerService.parse_elements_from_html(html_content, task.url)
                elements_data = result['elements']
                steps_data = result['steps']

                task.element_count = len(elements_data)
                task.step_count = len(steps_data)
                task.result_msg = f'解析完成，共{len(elements_data)}个元素'
                task.save()

                diff_result = CrawlerService.incremental_compare(project_id, elements_data, task.url)

                for elem in elements_data:
                    existing = KbElement.objects.filter(
                        project_id=project_id, page_name=elem['page_name'], element_name=elem['element_name']
                    ).first()
                    if existing:
                        existing.locator_type = elem['locator_type']
                        existing.locator_value = elem['locator_value']
                        existing.status = 'valid'
                        existing.last_refresh_time = datetime.now()
                        existing.save()
                    else:
                        KbElement.objects.create(
                            project_id=project_id,
                            page_name=elem['page_name'],
                            element_name=elem['element_name'],
                            element_type=elem['element_type'],
                            locator_type=elem['locator_type'],
                            locator_value=elem['locator_value'],
                            status='valid',
                            last_refresh_time=datetime.now(),
                        )

                task.status = 'completed'
                task.end_time = datetime.now()
                diff_msg = f'新增{diff_result["added_count"]}，废弃{diff_result["removed_count"]}，不变{diff_result["unchanged_count"]}'
                task.result_msg = f'采集完成: 共{len(elements_data)}个元素，{len(steps_data)}个步骤。增量对比: {diff_msg}'
                task.save()

                existing_asset = KbAsset.objects.filter(
                    project_id=project_id, crawler_url=task.url
                ).first()

                if existing_asset:
                    KbAssetStep.objects.filter(asset=existing_asset).delete()
                    for i, step in enumerate(steps_data):
                        KbAssetStep.objects.create(asset=existing_asset, sort_num=i + 1, **step)
                    existing_asset.status = 'published'
                    existing_asset.save()
                    task.auto_asset_id = existing_asset.id
                else:
                    asset = KbAsset.objects.create(
                        project_id=project_id,
                        asset_name=f'{task.task_name}',
                        status='draft',
                        priority='P2',
                        crawler_url=task.url,
                        env_type=env.env_type if env else '',
                        engine_type='playwright',
                        create_user=task.create_user,
                    )
                    for i, step in enumerate(steps_data):
                        KbAssetStep.objects.create(asset=asset, sort_num=i + 1, **step)
                    task.auto_asset_id = asset.id

                task.save()
                browser.close()
        except Exception as e:
            log_error(f'爬取任务失败: {str(e)}')
            task.status = 'failed'
            task.result_msg = str(e)
            task.end_time = datetime.now()
            task.save()
