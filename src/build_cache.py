
import hashlib
import json
from pathlib import Path
import py_compile


class SmartBuildCache:
    def __init__(self, project_dir, cache_dir):
        self.project_dir = Path(project_dir)
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache_file = self.cache_dir / "cache.json"

        if self.cache_file.exists():
            self.cache_data = json.loads(
                self.cache_file.read_text(encoding="utf-8")
            )
        else:
            self.cache_data = {}

    def calculate_hash(self, file_path):
        """Generate SHA-256 hash of a file."""
        sha256 = hashlib.sha256()

        with open(file_path, "rb") as file:
            for chunk in iter(lambda: file.read(8192), b""):
                sha256.update(chunk)

        return sha256.hexdigest()

    def build_project(self):
        """Rebuild changed files and reuse valid cached results."""
        print("\n===== SMART BUILD CACHE INVALIDATION =====")

        hits = 0
        misses = 0
        failures = 0

        for file_path in sorted(self.project_dir.glob("*.py")):
            file_hash = self.calculate_hash(file_path)
            file_name = file_path.name

            
            cached_hash = self.cache_data.get(file_name)

            output_file = self.cache_dir / (file_path.stem + ".pyc")

            if cached_hash == file_hash and output_file.exists():
                print(f"[CACHE HIT] {file_name} - Skipping build")
                hits += 1
            else:
                print(f"[CACHE MISS] {file_name} - Building...")


                try:
                    output_file = self.cache_dir / (
                        file_path.stem + ".pyc"
                    )

                    py_compile.compile(
                        str(file_path),
                        cfile=str(output_file),
                        doraise=True
                    )

                    self.cache_data[file_name] = file_hash
                    print(f"[BUILD SUCCESS] {file_name}")
                    misses += 1

                except py_compile.PyCompileError as error:
                    print(f"[BUILD FAILED] {file_name}: {error}")
                    failures += 1
                    self.cache_data.pop(file_name, None)

        self.cache_file.write_text(
            json.dumps(self.cache_data, indent=4),
            encoding="utf-8"
        )

        print("\n===== BUILD SUMMARY =====")
        print("Cache Hits:", hits)
        print("Cache Misses:", misses)
        print("Build Failures:", failures)