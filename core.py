from pathlib import Path
import mimetypes

def listar_arquivos(pasta: Path, mostrar_ocultos: bool = False):
    if not pasta.exists():
        raise FileNotFoundError(f"Pasta não encontrada: {pasta}")
    if not pasta.is_dir():
        raise NotADirectoryError(f"Não é uma pasta: {pasta}")

    arquivos = []
    for entrada in pasta.iterdir():
        if entrada.is_dir():
            continue
        if not mostrar_ocultos and entrada.name.startswith('.'):
            continue
        arquivos.append(entrada)
    return arquivos

def descobrir_categoria(arquivo: Path, categorias) -> str:
    # Verificar pela extensão primeiro (mais confiável)
    ext = arquivo.suffix.lower()
    for categoria, extensoes in categorias.items():
        if ext in extensoes:
            return categoria

    # Depois tenta identificar pelo tipo MIME
    tipo, _ = mimetypes.guess_type(arquivo.name)
    if tipo:
        if tipo.startswith("image/"):
            return "Imagens"
        elif tipo.startswith("video/"):
            return "Vídeos"
        elif tipo.startswith("audio/"):
            return "Áudios"
        elif (
            tipo.startswith("application/vnd.ms-excel") or
            tipo.startswith("application/vnd.openxmlformats-officedocument.spreadsheetml") or
            "spreadsheet" in tipo  # cobre LibreOffice (ods)
        ):
            return "Planilhas"
        elif tipo.startswith("application/msword") or tipo.startswith("application/vnd.openxmlformats-officedocument.wordprocessingml"):
            return "Documentos"
        elif tipo.startswith("application/vnd.ms-powerpoint") or tipo.startswith("application/vnd.openxmlformats-officedocument.presentationml"):
            return "Documentos"
        elif tipo.startswith("application/pdf"):
            return "Documentos"
        elif tipo.startswith("application/zip") or tipo.endswith("compressed"):
            return "Compactados"
        elif tipo.startswith("application/x-msdownload"):
            return "Executáveis"
        elif tipo.startswith("application/x-iso9660-image"):
            return "Imagens de Disco"

    return "Outros"
