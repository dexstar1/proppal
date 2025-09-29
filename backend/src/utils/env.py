import os
from typing import Optional


def load_dotenv_simple(path: str = ".env") -> bool:
    """
    Minimal .env loader. Reads KEY=VALUE lines and sets os.environ if not already set.
    Ignores blank lines and those starting with '#'. Returns True if file was loaded.
    """
    if not os.path.exists(path):
        return False
    try:
        with open(path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    continue
                key, val = line.split('=', 1)
                key = key.strip()
                val = val.strip()
                if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                if key and key not in os.environ:
                    os.environ[key] = val
        return True
    except Exception:
        return False
