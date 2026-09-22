# Demo: PaddleOCR reconhecendo placa de carro

1. Carrega o PaddleOCR.
2. Le toda a imagem e mostra no terminal tudo o que a biblioteca conseguiu
   reconhecer.
3. Filtra so os textos que batem com o formato de placa brasileira
   (antigo `ABC1234` ou Mercosul `ABC1D23`).
4. Salva as placas encontradas em `placas_detectadas.csv`, com data e hora.

## Como rodar

```bash
pip install -r requirements.txt
python main.py capturas/placa-carro-1.jpg
```
Na primeira execucao o Paddleocr baixa os modelos automaticamente.

**Referências:** [GitHub](https://github.com/PaddlePaddle/PaddleOCR) | [AI Studio](https://aistudio.baidu.com/paddleocr)
