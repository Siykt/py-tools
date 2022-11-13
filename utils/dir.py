from pathlib import Path


def createDir(p: Path):
    if not p.exists():
        p.mkdir(parents=True)
