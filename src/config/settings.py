import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent

sys.path.append(str(PROJECT_ROOT))

DATABASE_PATH = PROJECT_ROOT / "database", "veiculos.db"
DATABASE_URL = f"sqlite:///{DATABASE_PATH}"
