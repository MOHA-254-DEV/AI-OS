### 🔹 `file_sync.py` — Core File Distribution Protocol
```python
import os
from distributed.chunker import chunk_file, save_chunks
from distributed.peer_io import send_file_to_peer, receive_file

class FileDistributor:
    def __init__(self, peers: list[str], chunk_size=1024 * 1024):
        self.peers = peers
        self.chunk_size = chunk_size

    def distribute_file(self, filepath):
        filename = os.path.basename(filepath)
        chunks = list(chunk_file(filepath, self.chunk_size))
        num_peers = len(self.peers)

        for idx, chunk in enumerate(chunks):
            peer_ip, peer_port = self.peers[idx % num_peers]
            temp_path = f"/tmp/{filename}.part{idx}"
            with open(temp_path, 'wb') as f:
                f.write(chunk)
            send_file_to_peer(peer_ip, peer_port, temp_path)

    def receive_files(self, listen_port, output_dir):
        receive_file(listen_port, output_dir)
```

---