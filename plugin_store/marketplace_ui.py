import json
import os

class PluginMarketplace:
    def __init__(self, registry_path='plugin_store/plugin_registry.json'):
        self.registry_path = registry_path
        self.load_plugins()

    def load_plugins(self):
        with open(self.registry_path, 'r') as f:
            self.plugins = json.load(f)["plugins"]

    def list_plugins(self):
        print("🛍️ Available Plugins:")
        for plugin in self.plugins:
            if plugin['approved']:
                print(f"\n- {plugin['name']} by {plugin['author']}")
                print(f"  ➤ Description: {plugin['description']}")
                print(f"  ➤ Version: {plugin['version']} | Price: ${plugin['price']}")
                print(f"  ➤ Trust Score: {plugin['trust_score']} | Rating: {plugin['rating']}⭐")

    def search_plugins(self, keyword):
        results = [p for p in self.plugins if keyword.lower() in p['name'].lower()]
        return results

    def install_plugin(self, plugin_id):
        for plugin in self.plugins:
            if plugin["id"] == plugin_id and plugin['approved']:
                print(f"✅ Installing plugin: {plugin['name']}")
                # Here you would copy file, register plugin, etc.
                return True
        print("❌ Plugin not found or not approved.")
        return False
