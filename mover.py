# mover.py
import shutil
from pathlib import Path

def mover_arquivo(arquivo: Path, destino: Path):
    if not arquivo.exists():
        print(f"Aviso: {arquivo} não existe mais na origem, ignorando.")
        return

    destino.mkdir(parents=True, exist_ok=True)
    destino_arquivo = destino / arquivo.name

    contador = 1
    while destino_arquivo.exists():
        destino_arquivo = destino / f"{arquivo.stem}_{contador}{arquivo.suffix}"
        contador += 1

    shutil.move(str(arquivo), destino_arquivo)
    print(f"Movido: {arquivo.name} -> {destino_arquivo.name}")
