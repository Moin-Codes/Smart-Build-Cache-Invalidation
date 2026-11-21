
from pathlib import Path
from build_cache import SmartBuildCache

# Get the main project directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Define project and cache directories
PROJECT_DIR = BASE_DIR / "sample_project"
CACHE_DIR = BASE_DIR / "cache"


def main():
    print("Starting Smart Build-Cache System...")

    # Initialize the build cache
    build_cache = SmartBuildCache(
        PROJECT_DIR,
        CACHE_DIR
    )

    # Execute automated build
    build_cache.build_project()

    print("\nBuild process completed!")


if __name__ == "__main__":
    main()