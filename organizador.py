#!/usr/bin/env python3
from pathlib import Path
import argparse
import sys
import os
import shutil

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA_OK = True
except ImportError:
    COLORAMA_OK = False

from categorias import carregar_categorias
from util import formato_tamanho
from core import listar_arquivos, descobrir_categoria

CORES = {
    "Executáveis": Fore.RED if COLORAMA_OK else "",
    "Imagens": Fore.BLUE if COLORAMA_OK else "",
    "Compactados": Fore.YELLOW if COLORAMA_OK else "",
    "Documentos": Fore.GREEN if COLORAMA_OK else "",
    "Vídeos": Fore.MAGENTA if COLORAMA_OK else "",
    "Áudios": Fore.CYAN if COLORAMA_OK else "",
    "Imagens de Disco": Fore.WHITE if COLORAMA_OK else "",
    "Planilhas": Fore.LIGHTGREEN_EX if COLORAMA_OK else "",
    "Outros": ""
}

def organizar_arquivos(pasta, arquivos, categorias):
    """
    Move os arquivos para subpastas baseadas em suas categorias.
    """
    if not arquivos:
        print("Nenhum arquivo para organizar.")
        return

    print(f"\nIniciando a organização da pasta: {pasta}")
    print("Movendo arquivos...")

    for f in arquivos:
        # Pega a categoria do arquivo
        categoria = descobrir_categoria(f, categorias)
        
        # Define o caminho completo para a pasta de destino
        caminho_destino_pasta = pasta / categoria
        
        # Cria a pasta de destino se ela não existir.
        # A opção exist_ok=True evita erros caso a pasta já exista.
        try:
            caminho_destino_pasta.mkdir(parents=True, exist_ok=True)
        except PermissionError:
            print(f"Erro: Permissão negada para criar a pasta '{caminho_destino_pasta}'.")
            continue
            
        caminho_destino_arquivo = caminho_destino_pasta / f.name

        try:
            shutil.move(f, caminho_destino_arquivo)
            # Imprime no formato desejado: Movendo foto.jpg -> Downloads/Imagens
            print(f"Movido: {f.name} -> {pasta.name}/{categoria}/")
        except shutil.SameFileError:
            print(f"Pulado: {f.name} já existe no destino.")
        except Exception as e:
            print(f"Erro ao mover '{f.name}': {e}")
            
    print("\nOrganização concluída!")

def main():
    parser = argparse.ArgumentParser(description="Gerenciador de arquivos para sua pasta de Downloads.")
    parser.add_argument("pasta", nargs="?", default=str(Path.home() / "Downloads"),
                        help="Pasta a ser gerenciada (padrão: ~/Downloads)")
    parser.add_argument("--mostrar-ocultos", action="store_true",
                        help="Incluir arquivos ocultos (começam com .)")
    parser.add_argument("--ordenar", choices=["nome", "tamanho", "data"], default="nome",
                        help="Critério de ordenação: nome, tamanho ou data (padrão: nome)")
    parser.add_argument("--reverso", action="store_true",
                        help="Inverter a ordem da listagem")
    parser.add_argument("--exportar", choices=["csv", "json"], help="Exportar resultado para CSV ou JSON")
    parser.add_argument("--categorias", default="categorias.json",
                        help="Arquivo JSON com categorias customizadas (padrão: categorias.json)")
    parser.add_argument("--sem-cor", action="store_true", help="Desabilitar saída colorida")
    
    # NOVO: Argumento para iniciar a organização
    parser.add_argument("--organizar", action="store_true", 
                        help="Move os arquivos para subdiretórios com base em suas categorias.")
                        
    args = parser.parse_args()

    categorias = carregar_categorias(args.categorias)

    pasta = Path(args.pasta).expanduser()
    try:
        arquivos = listar_arquivos(pasta, args.mostrar_ocultos)
    except FileNotFoundError:
        print("Erro: Pasta não encontrada.")
        sys.exit(1)
    except NotADirectoryError:
        print("Erro: O caminho informado não é uma pasta.")
        sys.exit(1)
    except PermissionError:
        print("Erro: Permissão negada para acessar a pasta.")
        sys.exit(1)
    except Exception as e:
        print("Erro inesperado:", e)
        sys.exit(1)
    
    # Lógica para decidir se apenas lista ou se organiza
    if args.organizar:
        print(f"Total de arquivos a serem organizados: {len(arquivos)}")
        organizar_arquivos(pasta, arquivos, categorias)
    else:
        # Seu código de listagem, que permanece inalterado
        print(f"Arquivos encontrados em: {pasta}")
        print(f"Total: {len(arquivos)}\n")
    
        stats = {f: f.stat() for f in arquivos}
    
        if args.ordenar == "nome":
            arquivos_ordenados = sorted(arquivos, key=lambda p: p.name.lower(), reverse=args.reverso)
        elif args.ordenar == "tamanho":
            arquivos_ordenados = sorted(arquivos, key=lambda p: stats[p].st_size, reverse=args.reverso)
        elif args.ordenar == "data":
            arquivos_ordenados = sorted(arquivos, key=lambda p: stats[p].st_mtime, reverse=args.reverso)
        else:
            arquivos_ordenados = arquivos
    
        max_nome = max((len(f.name) for f in arquivos_ordenados), default=0)
        max_categoria = max((len(descobrir_categoria(f, categorias)) for f in arquivos_ordenados), default=8)
    
        print(f"{'Arquivo'.ljust(max_nome)}  {'Tamanho'.rjust(10)}  {'Categoria'.ljust(max_categoria)}")
        print("-" * (max_nome + 13 + max_categoria))
        
        for f in arquivos_ordenados:
            try:
                tamanho = formato_tamanho(stats[f].st_size)
            except Exception:
                tamanho = "—"
            categoria = descobrir_categoria(f, categorias)
            cor = CORES.get(categoria, "") if COLORAMA_OK and not args.sem_cor else ""
            reset = Style.RESET_ALL if COLORAMA_OK and not args.sem_cor else ""
            print(f"{f.name.ljust(max_nome)}  {tamanho.rjust(10)}  {cor}{categoria.ljust(max_categoria)}{reset}")
    
        if args.exportar == "csv":
            import csv
            with open("resultado.csv", "w", newline="", encoding="utf-8") as fcsv:
                writer = csv.writer(fcsv)
                writer.writerow(["Arquivo", "Tamanho", "Categoria"])
                for f in arquivos_ordenados:
                    writer.writerow([f.name, formato_tamanho(stats[f].st_size), descobrir_categoria(f, categorias)])
            print("\nExportado para resultado.csv")
        elif args.exportar == "json":
            import json
            dados = [
                {"arquivo": f.name, "tamanho": formato_tamanho(stats[f].st_size), "categoria": descobrir_categoria(f, categorias)}
                for f in arquivos_ordenados
            ]
            with open("resultado.json", "w", encoding="utf-8") as fj:
                json.dump(dados, fj, ensure_ascii=False, indent=2)
            print("\nExportado para resultado.json")

if __name__ == "__main__":
    main()
