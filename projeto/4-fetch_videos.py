# 4-fetch_videos.py

import os
import requests
import shutil
import random

# 🔹 Configuração da API Pixabay
PIXABAY_API_KEY = "40457207-b09699ac3ca52bd492865e5a8"
PIXABAY_API_URL = "https://pixabay.com/api/videos/"

# 🔹 Caminhos e parâmetros
DURACAO_PATH = "/root/video-generator/assets/audio/duracao.txt"
VIDEOS_DIR = "/root/video-generator/assets/videos/clips"
NUM_VIDEOS = 20
MIN_DURACAO = 10  # Ignora vídeos com menos de 10s

TERMOS_BIBLICOS = ["Bible", "Jesus", "Christianity", "Biblical stories", "Church", "Cross"]
tema_escolhido = random.choice(TERMOS_BIBLICOS)

os.makedirs(VIDEOS_DIR, exist_ok=True)

# 🔹 Ler duração
if not os.path.exists(DURACAO_PATH):
    raise FileNotFoundError(f"Arquivo de duração não encontrado: {DURACAO_PATH}")

with open(DURACAO_PATH, "r", encoding="utf-8") as f:
    try:
        duracao_total = int(f.read().strip())
    except ValueError:
        raise ValueError("A duração no arquivo não é um número válido.")

print(f"⏱️ Duração total da narração: {duracao_total} segundos")
print(f"🔍 Buscando vídeos relacionados a: {tema_escolhido}")

# 🔹 Buscar vídeos
params = {
    "key": PIXABAY_API_KEY,
    "q": tema_escolhido,
    "video_type": "film",
    "per_page": NUM_VIDEOS
}

response = requests.get(PIXABAY_API_URL, params=params)
if response.status_code != 200:
    raise RuntimeError(f"Erro na requisição à API Pixabay: {response.status_code}")

data = response.json()
videos_disponiveis = data.get("hits", [])
if not videos_disponiveis:
    raise ValueError(f"Nenhum vídeo encontrado para o tema '{tema_escolhido}'.")

random.shuffle(videos_disponiveis)

# 🔹 Baixar vídeos
soma_duracao = 0
downloaded = 0

for idx, video in enumerate(videos_disponiveis):
    duracao = video.get("duration", 0)
    if duracao < MIN_DURACAO:
        print(f"Ignorando vídeo curto ({duracao}s)")
        continue

    url = video["videos"]["large"]["url"]
    nome_arquivo = f"clip_{downloaded+1}.mp4"
    destino = os.path.join(VIDEOS_DIR, nome_arquivo)

    try:
        print(f"⬇️ Baixando: {url}")
        r = requests.get(url, stream=True, timeout=30)
        r.raise_for_status()
        with open(destino, "wb") as f:
            shutil.copyfileobj(r.raw, f)
        print(f"Salvo: {destino}")
        soma_duracao += duracao
        downloaded += 1
    except Exception as e:
        print(f"Erro ao baixar vídeo {idx+1}: {e}")

    if soma_duracao >= duracao_total:
        print(f"Duração alvo atingida: {soma_duracao}s")
        break

print(f"{downloaded} vídeo(s) baixado(s), totalizando {soma_duracao} segundos.")
