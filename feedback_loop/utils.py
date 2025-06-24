# feedback_loop/utils.py

def apply_diff(original, diff_lines):
    import difflib
    patched = list(difflib.restore(diff_lines, 2))
    return "\n".join(patched)
