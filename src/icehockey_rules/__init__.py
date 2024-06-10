__version__ = "0.3.0"

from pathlib import Path

_package_dir = Path(__file__).resolve().parent
config_dir = _package_dir.parent.parent / "config"
data_dir = _package_dir.parent.parent / "data"