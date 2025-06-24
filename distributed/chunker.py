### 🔹 `chunker.py` — File Chunking Logic
```python
import os

def chunk_file(filepath, chunk_size=1024 * 1024):
    with open(filepath, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            yield chunk

def save_chunks(chunks, dest_dir, base_name):
    os.makedirs(dest_dir, exist_ok=True)
    for idx, chunk in enumerate(chunks):
        with open(os.path.join(dest_dir, f"{base_name}.part{idx}"), 'wb') as f:
            f.write(chunk)
```

---