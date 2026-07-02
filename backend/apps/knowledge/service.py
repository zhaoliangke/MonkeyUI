import json
from django.db import transaction
from apps.knowledge.models import KbCategory, KbAsset, KbAssetStep, KbAssetScript, KbAssetVersion
from apps.element_lib.models import KbElement
from core.middleware import get_current_project_id
from core.exception import NotFoundException


class KnowledgeService:

    @staticmethod
    def get_category_tree(project_id: int):
        roots = KbCategory.objects.filter(project_id=project_id, parent_id__isnull=True).order_by('sort')
        return roots

    @staticmethod
    @transaction.atomic
    def save_asset_with_steps(data: dict):
        asset_id = data.get('id')
        steps_data = data.pop('steps', [])

        if asset_id:
            asset = KbAsset.objects.filter(id=asset_id).first()
            if not asset:
                raise NotFoundException('资产不存在')
            for key, value in data.items():
                setattr(asset, key, value)
            asset.version += 1
            asset.save()
        else:
            asset = KbAsset.objects.create(**data)

        KbAssetStep.objects.filter(asset=asset).delete()
        invalid_elements = []

        for i, step in enumerate(steps_data):
            element_name = step.get('element_name', '')
            is_valid = step.get('is_valid', True)

            if element_name:
                element_exists = KbElement.objects.filter(
                    element_name=element_name, status='valid'
                ).exists()
                if not element_exists:
                    is_valid = False
                    invalid_elements.append(element_name)

            KbAssetStep.objects.create(
                asset=asset,
                sort_num=step.get('sort_num', i + 1),
                step_content=step.get('step_content', ''),
                element_name=element_name,
                action_type=step.get('action_type', ''),
                param=step.get('param', ''),
                assert_text=step.get('assert_text', ''),
                is_valid=is_valid,
            )

        version_snapshot = json.dumps({
            'asset_name': asset.asset_name,
            'status': asset.status,
            'steps_count': len(steps_data),
            'engine_type': asset.engine_type,
            'invalid_elements': invalid_elements,
        }, ensure_ascii=False)
        KbAssetVersion.objects.create(
            asset=asset,
            version_num=asset.version,
            version_content=version_snapshot,
            version_type='create' if not asset_id else 'edit',
        )

        return asset

    @staticmethod
    @transaction.atomic
    def save_script(asset_id: int, engine_type: str, script_content: str):
        asset = KbAsset.objects.filter(id=asset_id).first()
        if not asset:
            raise NotFoundException('资产不存在')

        KbAssetScript.objects.filter(asset=asset, is_last=True).update(is_last=False)

        last_scripts = KbAssetScript.objects.filter(asset=asset, engine_type=engine_type).order_by('-script_version')
        next_version = last_scripts[0].script_version + 1 if last_scripts.exists() else 1

        script = KbAssetScript.objects.create(
            asset=asset,
            engine_type=engine_type,
            script_content=script_content,
            script_version=next_version,
            is_last=True,
        )

        KbAssetVersion.objects.create(
            asset=asset,
            version_num=asset.version,
            version_content=json.dumps({'script_version': next_version}, ensure_ascii=False),
            version_type='ai_generate',
        )
        return script

    @staticmethod
    def get_version_diff(asset_id: int, version_a: int, version_b: int):
        v1 = KbAssetVersion.objects.filter(asset_id=asset_id, version_num=version_a).first()
        v2 = KbAssetVersion.objects.filter(asset_id=asset_id, version_num=version_b).first()
        result = {
            'version_a': v1.version_content if v1 else None,
            'version_b': v2.version_content if v2 else None,
            'version_a_time': str(v1.create_time) if v1 else None,
            'version_b_time': str(v2.create_time) if v2 else None,
        }
        return result

    @staticmethod
    def get_dashboard_stats(project_id: int) -> dict:
        assets = KbAsset.objects.filter(project_id=project_id)
        total = assets.count()
        published = assets.filter(status='published').count()
        invalidated = assets.filter(status='invalidated').count()

        from apps.crawler.models import KbCrawlerTask
        crawl_tasks = KbCrawlerTask.objects.filter(project_id=project_id)
        crawl_total = crawl_tasks.count()
        crawl_completed = crawl_tasks.filter(status='completed').count()

        from apps.auto_run.models import KbRunRecord
        run_records = KbRunRecord.objects.filter(project_id=project_id)
        run_total = run_records.count()
        run_passed = run_records.filter(result='pass').count()

        from apps.reflux.models import KbRefluxRecord
        reflux_pending = KbRefluxRecord.objects.filter(
            project_id=project_id, status='pending'
        ).count()

        return {
            'assets_total': total,
            'assets_published': published,
            'assets_invalidated': invalidated,
            'crawl_success_rate': round(crawl_completed / crawl_total * 100, 1) if crawl_total > 0 else 0,
            'execution_pass_rate': round(run_passed / run_total * 100, 1) if run_total > 0 else 0,
            'reflux_pending': reflux_pending,
            'crawl_total': crawl_total,
            'run_total': run_total,
        }
