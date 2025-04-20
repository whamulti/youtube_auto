# 5-fetch_thumbnail.py

import os
import requests
import shutil
import random
from PIL import Image
from io import BytesIO

# 🔹 Configuração da API Pexels
PEXELS_API_KEY = "OaR9SQ7X828gmGSFRp9F1XtIhtch7bEoJ1UIRsluqfi2gIwt8c4aDjQr"
PEXELS_API_URL = "https://api.pexels.com/v1/search"

# 🔹 Caminho de saída
IMAGES_DIR = "/root/video-generator/assets/images"
THUMBNAIL_PATH = os.path.join(IMAGES_DIR, "thumbnail.jpg")
os.makedirs(IMAGES_DIR, exist_ok=True)

# 🔹 Palavras-chave bíblicas
TERMOS_BIBLICOS = ["Bible", "Jesus", "Christianity", "Biblical stories", "Church", "Cross"]
query_biblica = random.choice(TERMOS_BIBLICOS)

print(f"🖼️ Buscando imagem sobre '{query_biblica}' na Pexels...")

# 🔹 Requisição à API
headers = {"Authorization": PEXELS_API_KEY}
params = {"query": query_biblica, "per_page": 5}
response = requests.get(PEXELS_API_URL, headers=headers, params=params)

if response.status_code != 200:
    raise RuntimeError(f"Erro {response.status_code} ao acessar API Pexels: {response.text}")

try:
    data = response.json()
except Exception:
    raise ValueError("Erro ao decodificar JSON da API Pexels.")

if "photos" not in data or len(data["photos"]) == 0:
    raise ValueError(f"Nenhuma imagem encontrada para o tema: {query_biblica}")

# 🔹 Escolhe e baixa imagem
photo = random.choice(data["photos"])
url = photo["src"]["large"]

try:
    img_response = requests.get(url, stream=True)
    img_response.raise_for_status()
    image = Image.open(BytesIO(img_response.content)).convert("RGB")
    image = image.resize((1280, 720))  # padrão de thumbnail do YouTube
    image.save(THUMBNAIL_PATH, "JPEG", quality=90)
    print(f"Thumbnail salva em: {THUMBNAIL_PATH}")
except Exception as e:
    raise RuntimeError(f"Falha ao baixar ou salvar imagem: {e}")
