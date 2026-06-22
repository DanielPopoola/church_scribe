from config import load_config
from dependencies import build_dependencies
from watcher import start

if __name__ == "__main__":
    config = load_config()
    deps = build_dependencies(config)
    start(deps)