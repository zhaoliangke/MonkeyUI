import threading
import json
from datetime import datetime
from apps.auto_run.models import KbRunRecord
from apps.knowledge.models import KbAsset, KbAssetStep, KbAssetScript
from apps.environment.models import KbEnv, KbCredential
from apps.reflux.service import RefluxService
from core.middleware import get_current_project_id
from core.security import aes_decrypt
from core.logger import log_error


class RunEngineService:

    @staticmethod
    def validate_prerequisites(asset: KbAsset) -> list:
        errors = []
        if not asset:
            errors.append('资产不存在')
            return errors
        script = KbAssetScript.objects.filter(asset=asset, is_last=True).first()
        if not script:
            errors.append('资产无可用脚本，请先生成脚本')
        steps = KbAssetStep.objects.filter(asset=asset).exists()
        if not steps:
            errors.append('资产无测试步骤')
        if not asset.engine_type:
            errors.append('未配置执行引擎')
        return errors

    @staticmethod
    def execute_asset(asset_id: int, run_type: str = 'single', env_id: int = None) -> int:
        project_id = get_current_project_id()
        asset = KbAsset.objects.filter(id=asset_id, project_id=project_id).first()

        errors = RunEngineService.validate_prerequisites(asset)
        if errors:
            raise ValueError('; '.join(errors))

        script = KbAssetScript.objects.filter(asset=asset, is_last=True).first()

        if env_id:
            env = KbEnv.objects.filter(id=env_id).first()
            if not env:
                raise ValueError('指定环境不存在')
            if env.env_type == 'production':
                raise ValueError('不支持在生产环境执行自动化测试')

        record = KbRunRecord.objects.create(
            project_id=project_id,
            asset_id=asset_id,
            script_version=script.script_version,
            run_type=run_type,
            result='running',
        )

        thread = threading.Thread(
            target=RunEngineService._run_script,
            args=(record.id, asset, script),
            daemon=True,
        )
        thread.start()
        return record.id

    @staticmethod
    def _run_script(record_id: int, asset: KbAsset, script: KbAssetScript):
        record = KbRunRecord.objects.filter(id=record_id).first()
        if not record:
            return

        start_time = datetime.now()
        logs = []

        try:
            import os
            import uuid

            run_id = uuid.uuid4().hex[:8]
            screenshot_dir = f'/tmp/screenshots/{run_id}'
            os.makedirs(screenshot_dir, exist_ok=True)

            logs.append(f'[{datetime.now().strftime("%H:%M:%S")}] 开始执行资产: {asset.asset_name}')
            logs.append(f'[{datetime.now().strftime("%H:%M:%S")}] 引擎类型: {asset.engine_type}')
            logs.append(f'[{datetime.now().strftime("%H:%M:%S")}] 脚本版本: {script.script_version}')

            exec_globals = {
                'asset_name': asset.asset_name,
                'engine_type': asset.engine_type,
                'run_params': json.loads(asset.run_param) if asset.run_param else {},
                'assert_config': json.loads(asset.assert_config) if asset.assert_config else {},
                'screenshot_dir': screenshot_dir,
                'logs': logs,
            }
            exec(script.script_content, exec_globals)

            elapsed = (datetime.now() - start_time).total_seconds()
            logs.append(f'[{datetime.now().strftime("%H:%M:%S")}] 执行完成，耗时: {elapsed:.2f}s')

            screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')] if os.path.exists(screenshot_dir) else []
            screenshot_paths = [f'{screenshot_dir}/{f}' for f in screenshots]

            record.result = 'pass'
            record.cost_time = elapsed
            record.log_content = '\n'.join(logs)
            record.screenshot_path = json.dumps(screenshot_paths, ensure_ascii=False)
            record.video_path = ''
            record.save()

            RefluxService.trigger_reflux(
                project_id=record.project_id,
                asset_id=record.asset_id,
                run_record_id=record.id,
                execution_result='pass',
            )
        except Exception as e:
            elapsed = (datetime.now() - start_time).total_seconds()
            logs.append(f'[{datetime.now().strftime("%H:%M:%S")}] 执行失败: {str(e)}')
            error_trace = __import__('traceback').format_exc()
            logs.append(error_trace)

            record.result = 'fail'
            record.cost_time = elapsed
            record.fail_reason = str(e)
            record.log_content = '\n'.join(logs)
            record.save()

            RefluxService.trigger_reflux(
                project_id=record.project_id,
                asset_id=record.asset_id,
                run_record_id=record.id,
                execution_result='fail',
                error_msg=str(e),
            )

    @staticmethod
    def execute_batch(asset_ids: list, run_type: str = 'batch'):
        record_ids = []
        for asset_id in asset_ids:
            try:
                rid = RunEngineService.execute_asset(asset_id, run_type)
                record_ids.append(rid)
            except Exception as e:
                log_error(f'批量执行资产 {asset_id} 失败: {str(e)}')
        return record_ids
