# 1-generate_historia.py

import os
import random
import requests
import time

OUTPUT_DIR = "/root/video-generator/assets/texto"
os.makedirs(OUTPUT_DIR, exist_ok=True)
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "historia.txt")

# Lista de livros com abreviação para uso na URL (sem acento) e total de capítulos
LIVROS = [
    {"nome": "Gênesis", "url": "genesis", "capitulos": 50},
    {"nome": "Salmos", "url": "psalms", "capitulos": 150},
    {"nome": "João", "url": "john", "capitulos": 21},
    {"nome": "Mateus", "url": "matthew", "capitulos": 28},
    {"nome": "Apocalipse", "url": "revelation", "capitulos": 22},
    {"nome": "Romanos", "url": "romans", "capitulos": 16},
    {"nome": "Atos", "url": "acts", "capitulos": 28}
]

# Tentar até 5 vezes gerar uma passagem válida
for tentativa in range(5):
    livro = random.choice(LIVROS)
    capitulo = random.randint(1, livro["capitulos"])

    print(f"Tentativa {tentativa+1}: {livro['nome']} capítulo {capitulo}...")
    versiculos = []

    for versiculo in range(1, 30):  # tenta os 30 primeiros
        url = f"https://bible-api.com/{livro['url']}+{capitulo}:{versiculo}?translation=almeida"
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                texto = data.get("text", "").strip()
                if texto:
                    versiculos.append(f"{versiculo}. {texto}")
                else:
                    break
            else:
                break
        except Exception as e:
            print(f"Erro ao buscar versículo {versiculo}: {e}")
            break

    if versiculos:
        historia = " ".join([v.split(". ", 1)[-1] for v in versiculos])
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(historia)
        print(f"Passagem salva em: {OUTPUT_FILE}")
        break
    else:
        print("Nenhum versículo válido encontrado, tentando outro capítulo...")
        time.sleep(2)
else:
    print("Todas as tentativas falharam. A API pode estar indisponível.")
