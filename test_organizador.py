# test_organizador.py
import pytest
from util import formato_tamanho
from core import listar_arquivos, descobrir_categoria
from categorias import CATEGORIAS_PADRAO

def test_formato_tamanho():
    assert formato_tamanho(0) == "0.0 B"
    assert formato_tamanho(1023) == "1023.0 B"
    assert formato_tamanho(1024) == "1.0 KB"
    assert formato_tamanho(1048576) == "1.0 MB"

def test_descobrir_categoria(tmp_path):
    arq_img = tmp_path / "foto.jpg"
    arq_img.write_bytes(b"fake")
    arq_doc = tmp_path / "doc.pdf"
    arq_doc.write_bytes(b"fake")
    assert descobrir_categoria(arq_img, CATEGORIAS_PADRAO) == "Imagens"
    assert descobrir_categoria(arq_doc, CATEGORIAS_PADRAO) == "Documentos"

def test_listar_arquivos(tmp_path):
    (tmp_path / "arquivo1.txt").write_text("abc")
    (tmp_path / "arquivo2.txt").write_text("def")
    (tmp_path / ".oculto").write_text("xyz")
    (tmp_path / "subpasta").mkdir()
    arquivos = listar_arquivos(tmp_path, mostrar_ocultos=False)
    nomes = sorted([a.name for a in arquivos])
    assert nomes == ["arquivo1.txt", "arquivo2.txt"]
    arquivos = listar_arquivos(tmp_path, mostrar_ocultos=True)
    nomes = sorted([a.name for a in arquivos])
    assert nomes == [".oculto", "arquivo1.txt", "arquivo2.txt"]