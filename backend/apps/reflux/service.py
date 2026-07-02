import json
from datetime import datetime
from difflib import unified_diff
from apps.reflux.models import KbRefluxRecord
from apps.auto_run.models import KbRunRecord
from apps.knowledge.models import KbAsset, KbAssetStep, KbAssetScript, KbAssetVersion
from core.logger import log_error


class RefluxService:

    @staticmethod
    def trigger_reflux(project_id: int, asset_id: int, run_record_id: int,
                       execution_result: str, error_msg: str = ''):
        if execution_result == 'pass':
            asset = KbAsset.objects.filter(id=asset_id).first()
            if asset:
                asset.update_time = datetime.now()
                asset.save()
            return

        reflux_record = KbRefluxRecord.objects.create(
            project_id=project_id,
            asset_id=asset_id,
            run_record_id=run_record_id,
            reflux_type='structural',
            status='pending',
        )
        return reflux_record

    @staticmethod
    def compute_diff(asset_id: int) -> dict:
        scripts = KbAssetScript.objects.filter(asset_id=asset_id).order_by('-script_version')[:2]
        steps = KbAssetStep.objects.filter(asset_id=asset_id).order_by('sort_num')

        script_diff = ''
        if scripts.count() >= 2:
            new_script = scripts[0].script_content.splitlines(keepends=True)
            old_script = scripts[1].script_content.splitlines(keepends=True)
            diff_lines = list(unified_diff(old_script, new_script, lineterm=''))
            script_diff = '\n'.join(diff_lines)

        steps_data = [{'sort_num': s.sort_num, 'step_content': s.step_content, 'action_type': s.action_type}
                      for s in steps]

        return {
            'script_diff': script_diff,
            'steps': steps_data,
            'step_count': len(steps_data),
        }

    @staticmethod
    def apply_reflux(reflux_id: int, action: str, audit_user: str = ''):
        record = KbRefluxRecord.objects.filter(id=reflux_id).first()
        if not record:
            raise ValueError('回流记录不存在')

        if action == 'merge':
            asset = KbAsset.objects.filter(id=record.asset_id).first()
            if not asset:
                raise ValueError('资产不存在')

            if record.new_script:
                KbAssetScript.objects.filter(asset=asset, is_last=True).update(is_last=False)
                last_scripts = KbAssetScript.objects.filter(asset=asset).order_by('-script_version')
                next_version = last_scripts[0].script_version + 1 if last_scripts.exists() else 1
                KbAssetScript.objects.create(
                    asset=asset,
                    engine_type=asset.engine_type,
                    script_content=record.new_script,
                    script_version=next_version,
                    is_last=True,
                )

            if record.new_step_data:
                new_steps = json.loads(record.new_step_data) if isinstance(record.new_step_data, str) else record.new_step_data
                KbAssetStep.objects.filter(asset=asset).delete()
                for i, step in enumerate(new_steps):
                    KbAssetStep.objects.create(asset=asset, sort_num=i + 1, **step)

            asset.version += 1
            asset.status = 'published'
            asset.save()

            KbAssetVersion.objects.create(
                asset=asset,
                version_num=asset.version,
                version_content=json.dumps({'reflux_id': reflux_id}, ensure_ascii=False),
                version_type='reflux',
            )

            record.status = 'approved'
        elif action == 'ignore':
            record.status = 'ignored'
        elif action == 'fail':
            record.status = 'failed'
        else:
            raise ValueError(f'未知操作: {action}')

        record.audit_user = audit_user
        record.audit_time = datetime.now()
        record.save()
        return record
