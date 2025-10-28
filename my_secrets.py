from pathlib import Path

def get_secret(env, name):
    path = Path(f"/run/secrets/{env}_{name}")
    return path.read_text().strip() if path.exists() else None