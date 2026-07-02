import threading
import time
from core.logger import log_error


class TaskScheduler:
    _tasks = {}
    _lock = threading.Lock()

    @classmethod
    def submit(cls, task_id: str, func, *args, **kwargs):
        def wrapper():
            try:
                func(*args, **kwargs)
                cls._tasks[task_id] = 'completed'
            except Exception as e:
                log_error(f'任务 {task_id} 失败: {str(e)}')
                cls._tasks[task_id] = f'failed: {str(e)}'

        thread = threading.Thread(target=wrapper, daemon=True)
        thread.start()
        cls._tasks[task_id] = 'running'
        return thread

    @classmethod
    def get_status(cls, task_id: str) -> str:
        return cls._tasks.get(task_id, 'unknown')

    @classmethod
    def submit_batch(cls, tasks: list):
        results = []
        for task in tasks:
            task_id = task.get('task_id', str(time.time()))
            func = task.get('func')
            args = task.get('args', [])
            kwargs = task.get('kwargs', {})
            cls.submit(task_id, func, *args, **kwargs)
            results.append({'task_id': task_id, 'status': 'submitted'})
        return results
