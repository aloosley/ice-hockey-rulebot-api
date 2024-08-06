__version__ = "0.7.0"

from pathlib import Path

_package_dir = Path(__file__).resolve().parent
app_dir = _package_dir.parent.parent
config_dir = app_dir / "config"
data_dir = app_dir / "data"
