import os

def save_file(file_obj, save_path: str):
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    with open(save_path, "wb") as f:
        f.write(file_obj.read())
    return save_path

def delete_file(save_path: str):
    if os.path.exists(save_path):
        os.remove(save_path)
        return True
    return False
