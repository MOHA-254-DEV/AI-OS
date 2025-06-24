### 🔹 `peer_io.py` — Peer-to-Peer File Transfer Helpers
```python
import socket
import os

CHUNK_SIZE = 1024 * 1024

def send_file_to_peer(peer_ip, peer_port, filepath):
    sock = socket.socket()
    sock.connect((peer_ip, peer_port))

    filename = os.path.basename(filepath)
    sock.send(filename.encode())
    sock.recv(1024)  # ack

    with open(filepath, 'rb') as f:
        while chunk := f.read(CHUNK_SIZE):
            sock.sendall(chunk)
    sock.shutdown(socket.SHUT_WR)
    sock.close()

def receive_file(listen_port, output_dir):
    server = socket.socket()
    server.bind(("", listen_port))
    server.listen(1)
    conn, _ = server.accept()

    filename = conn.recv(1024).decode()
    conn.send(b"ACK")

    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'wb') as f:
        while chunk := conn.recv(CHUNK_SIZE):
            f.write(chunk)
    conn.close()
    server.close()
```

---