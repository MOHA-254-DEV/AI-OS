import re

class VersionManager:
    def __init__(self):
        pass

    def is_newer_version(self, current_version, new_version):
        def version_tuple(v):
            return tuple(map(int, (v.split("."))))
        return version_tuple(new_version) > version_tuple(current_version)

    def validate_version_format(self, version):
        return bool(re.match(r'^\d+\.\d+\.\d+$', version))

    def compare_versions(self, v1, v2):
        return (v1 > v2) - (v1 < v2)
