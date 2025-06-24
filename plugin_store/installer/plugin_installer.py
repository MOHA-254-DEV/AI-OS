import os
import zipfile
import tarfile
import json
import shutil
import tempfile
import subprocess
import requests
from urllib.parse import urlparse
from plugin_store.installer.dependency_resolver import DependencyResolver

class PluginInstaller:
    def __init__(self, plugin_dir='plugins', log_file='plugin_store/installer/installer_logs.json'):
        self.plugin_dir = plugin_dir
        self.resolver = DependencyResolver()
        self.log_file = log_file
        self._init_logs()

    def _init_logs(self):
        if not os.path.exists(self.log_file):
            with open(self.log_file, 'w') as f:
                json.dump([], f)

    def _log(self, entry):
        with open(self.log_file, 'r+') as f:
            logs = json.load(f)
            logs.append(entry)
            f.seek(0)
            json.dump(logs, f, indent=2)

    def _download_plugin(self, url):
        response = requests.get(url, stream=True)
        if response.status_code != 200:
            raise Exception(f"❌ Download failed: {url}")
        
        file_ext = os.path.splitext(urlparse(url).path)[-1]
        temp_path = os.path.join(tempfile.gettempdir(), os.path.basename(urlparse(url).path))
        with open(temp_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return temp_path

    def _extract_plugin(self, archive_path, extract_to):
        if archive_path.endswith('.zip'):
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(extract_to)
        elif archive_path.endswith(('.tar.gz', '.tgz')):
            with tarfile.open(archive_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_to)
        else:
            raise Exception("❌ Unsupported archive format.")

    def _verify_metadata(self, plugin_path):
        manifest = os.path.join(plugin_path, 'plugin.json')
        if not os.path.exists(manifest):
            raise Exception("❌ Plugin metadata file (plugin.json) not found.")
        with open(manifest) as f:
            metadata = json.load(f)
        required_keys = ['id', 'name', 'version', 'description']
        for key in required_keys:
            if key not in metadata:
                raise Exception(f"❌ Missing metadata key: {key}")
        return metadata

    def install_from_url(self, url):
        try:
            archive = self._download_plugin(url)
            temp_dir = tempfile.mkdtemp()
            self._extract_plugin(archive, temp_dir)
            
            # assume first folder is plugin
            content_list = os.listdir(temp_dir)
            if len(content_list) != 1:
                raise Exception("❌ Archive structure is invalid.")
            plugin_root = os.path.join(temp_dir, content_list[0])

            metadata = self._verify_metadata(plugin_root)
            dest_path = os.path.join(self.plugin_dir, metadata["id"])

            if os.path.exists(dest_path):
                shutil.rmtree(dest_path)
            shutil.copytree(plugin_root, dest_path)

            # Resolve dependencies
            self.resolver.install_dependencies(plugin_root)

            self._log({"plugin": metadata["id"], "status": "installed", "from": url})
            print(f"✅ Plugin '{metadata['name']}' v{metadata['version']} installed successfully.")
        except Exception as e:
            self._log({"plugin": url, "status": "failed", "error": str(e)})
            print(f"❌ Installation failed: {e}")
