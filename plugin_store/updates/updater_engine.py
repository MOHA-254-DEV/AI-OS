import os
import json
import shutil
from plugin_store.updates.version_manager import VersionManager

class PluginUpdater:
    def __init__(self, registry_path='plugin_registry.json', plugin_folder='plugins/'):
        self.registry_path = registry_path
        self.plugin_folder = plugin_folder
        self.version_manager = VersionManager()
        self._load_registry()

    def _load_registry(self):
        with open(self.registry_path, 'r') as f:
            self.registry = json.load(f)

    def _save_registry(self):
        with open(self.registry_path, 'w') as f:
            json.dump(self.registry, f, indent=2)

    def check_updates(self):
        updates = []
        for plugin_id, plugin in self.registry.items():
            latest_version = plugin.get('latest_version')
            current_version = plugin.get('version')
            if self.version_manager.is_newer_version(current_version, latest_version):
                updates.append((plugin_id, current_version, latest_version))
        return updates

    def apply_update(self, plugin_id, new_files_path):
        plugin_path = os.path.join(self.plugin_folder, plugin_id)
        if os.path.exists(plugin_path):
            shutil.rmtree(plugin_path)
        shutil.copytree(new_files_path, plugin_path)
        self.registry[plugin_id]['version'] = self.registry[plugin_id]['latest_version']
        self._save_registry()
        print(f"🔄 Plugin {plugin_id} updated to version {self.registry[plugin_id]['latest_version']}")

    def update_all(self):
        for plugin_id, current, latest in self.check_updates():
            print(f"📦 Updating {plugin_id} from v{current} ➜ v{latest}")
            new_files_path = f'updates_repo/{plugin_id}/{latest}'  # pretend repo
            self.apply_update(plugin_id, new_files_path)
