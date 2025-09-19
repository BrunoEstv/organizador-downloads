import json

CATEGORIAS_PADRAO = {
    "Imagens": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Vídeos": [".mp4", ".mkv", ".avi", ".mov", ".wmv"],
    "Áudios": [".mp3", ".wav", ".ogg", ".flac"],
    "Documentos": [".pdf", ".doc", ".docx", ".ppt", ".pptx", ".odt"],
    "Planilhas": [".xls", ".xlsx", ".csv", ".ods"],
    "Compactados": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Executáveis": [".exe", ".msi", ".bat", ".sh"],
    "Imagens de Disco": [".iso"],
    "Outros": []
}

def carregar_categorias(caminho="categorias.json"):
    try:
        with open(caminho, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return CATEGORIAS_PADRAO