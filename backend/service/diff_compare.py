import ast
import difflib


class DiffCompare:

    @staticmethod
    def compare_text(old_text: str, new_text: str) -> dict:
        diff = list(difflib.unified_diff(
            old_text.splitlines(keepends=True),
            new_text.splitlines(keepends=True),
            lineterm='',
        ))
        return {
            'has_changes': len(diff) > 0,
            'diff_lines': '\n'.join(diff),
            'added': sum(1 for d in diff if d.startswith('+') and not d.startswith('+++')),
            'removed': sum(1 for d in diff if d.startswith('-') and not d.startswith('---')),
        }

    @staticmethod
    def compare_scripts(old_script: str, new_script: str) -> dict:
        try:
            old_tree = ast.parse(old_script)
            new_tree = ast.parse(new_script)
            old_dump = ast.dump(old_tree, annotate_fields=False)
            new_dump = ast.dump(new_tree, annotate_fields=False)
            has_changes = old_dump != new_dump
            text_diff = DiffCompare.compare_text(old_script, new_script)
            return {
                'has_changes': has_changes,
                'ast_match': not has_changes,
                'diff_lines': text_diff['diff_lines'],
                'added_lines': text_diff['added'],
                'removed_lines': text_diff['removed'],
            }
        except SyntaxError:
            return DiffCompare.compare_text(old_script, new_script)

    @staticmethod
    def compare_steps(old_steps: list, new_steps: list) -> dict:
        old_texts = [s.get('step_content', '') if isinstance(s, dict) else str(s) for s in old_steps]
        new_texts = [s.get('step_content', '') if isinstance(s, dict) else str(s) for s in new_steps]
        old_combined = '\n'.join(old_texts)
        new_combined = '\n'.join(new_texts)
        return DiffCompare.compare_text(old_combined, new_combined)
