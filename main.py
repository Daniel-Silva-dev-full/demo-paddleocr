

import os
import sys
from leitor_placas import LeitorDePlacas, salvar_registros, CSV_PATH
import warnings
warnings.filterwarnings("ignore")

EXTENSOES_VALIDAS = (".jpg", ".jpeg", ".png", ".bmp")


def listar_imagens(caminho: str):
    if os.path.isdir(caminho):
        arquivos = sorted(
            os.path.join(caminho, nome)
            for nome in os.listdir(caminho)
            if nome.lower().endswith(EXTENSOES_VALIDAS)
        )
        return arquivos
    return [caminho]


def main():
    if len(sys.argv) < 2:
        print("Uso: python main.py <imagem_ou_pasta>")
        sys.exit(1)

    caminho_entrada = sys.argv[1]
    if not os.path.exists(caminho_entrada):
        print(f"Caminho nao encontrado: {caminho_entrada}")
        sys.exit(1)

    imagens = listar_imagens(caminho_entrada)
    if not imagens:
        print("Nenhuma imagem encontrada.")
        sys.exit(1)

    print(f"Carregando..")
    leitor = LeitorDePlacas(lang="pt")

    total_gravadas = 0
    for img in imagens:
        print(f"\nProcessando: {img}")
        registros = leitor.processar_imagem(img)

        if not registros:
            print("  Nenhuma placa reconhecida.")
            continue

        for r in registros:
            print(f"  Placa: {r['placa']}  (confianca={r['confianca']})  "
                  f"{r['data']} {r['hora']}")

        salvar_registros(registros)
        total_gravadas += len(registros)

    print(f"\n{total_gravadas} placas gravadas em '{CSV_PATH}'.")


if __name__ == "__main__":
    main()
