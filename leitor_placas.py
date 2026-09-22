

import csv
import os
import re
from datetime import datetime, timedelta
from paddleocr import PaddleOCR
import warnings
warnings.filterwarnings("ignore")

# Configuracao
CSV_PATH = "placas_detectadas.csv"
CSV_CABECALHO = ["placa", "confianca", "data", "hora", "arquivo"]

REGEX_PLACA = re.compile(r"^[A-Z]{3}[0-9][A-Z0-9][0-9]{2}$")
JANELA_DEDUPLICACAO = timedelta(seconds=30)


class LeitorDePlacas:
    def __init__(self, lang: str = "pt"):
        self.ocr = PaddleOCR(use_textline_orientation=True, lang=lang)
        self._ultima_deteccao = {}  # placa -> datetime da ultima vez gravada

    @staticmethod
    def normalizar(texto: str) -> str:
        limpo = re.sub(r"[^A-Za-z0-9]", "", texto).upper()
        return limpo

    def extrair_placas(self, resultado_ocr):
        candidatos = []

        for pagina in resultado_ocr:
            textos = pagina.get("rec_texts", [])
            confiancas = pagina.get("rec_scores", [])

            for texto_bruto, confianca in zip(textos, confiancas):
                texto = self.normalizar(texto_bruto)
                if REGEX_PLACA.match(texto):
                    candidatos.append((texto, confianca))

        return candidatos
    
    # Processamento de uma imagem
    def processar_imagem(self, caminho_imagem: str):
        resultado = self.ocr.predict(caminho_imagem)
        placas = self.extrair_placas(resultado)

        registros_novos = []
        agora = datetime.now()

        for placa, confianca in placas:
            ultima = self._ultima_deteccao.get(placa)
            if ultima and (agora - ultima) < JANELA_DEDUPLICACAO:
                continue 

            self._ultima_deteccao[placa] = agora
            registros_novos.append(
                {
                    "placa": placa,
                    "confianca": round(float(confianca), 3),
                    "data": agora.strftime("%Y-%m-%d"),
                    "hora": agora.strftime("%H:%M:%S"),
                    "arquivo": os.path.basename(caminho_imagem),
                }
            )

        return registros_novos

# CSV
def garantir_csv(caminho: str = CSV_PATH):
    if not os.path.exists(caminho):
        with open(caminho, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=CSV_CABECALHO)
            writer.writeheader()


def salvar_registros(registros, caminho: str = CSV_PATH):
    if not registros:
        return
    garantir_csv(caminho)
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=CSV_CABECALHO)
        for r in registros:
            writer.writerow(r)
