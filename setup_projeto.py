# setup_projeto.py

import os

# Caminho base do projeto
BASE_DIR = "/root/video-generator"

# Estrutura de diretórios necessária
PASTAS = [
    "assets/audio",
    "assets/texto",
    "assets/images",
    "assets/videos",
    "assets/videos/clips",
    "scripts"
]

# Arquivos básicos (vazios inicialmente)
ARQUIVOS = [
    "assets/texto/historia.txt",
    "assets/audio/narracao.wav",
    "assets/audio/duracao.txt",
    "assets/images/thumbnail.jpg"
]

print(f"Criando estrutura de projeto em: {BASE_DIR}\n")
os.makedirs(BASE_DIR, exist_ok=True)

# Criar pastas
for pasta in PASTAS:
    caminho = os.path.join(BASE_DIR, pasta)
    os.makedirs(caminho, exist_ok=True)
    print(f"Pasta criada: {caminho}")

# Criar arquivos vazios se não existirem
for arquivo in ARQUIVOS:
    caminho = os.path.join(BASE_DIR, arquivo)
    if not os.path.exists(caminho):
        with open(caminho, 'w', encoding='utf-8') as f:
            pass
        print(f"Arquivo criado: {caminho}")

import shutil

# Copiar scripts de /root/projeto para /root/video-generator/scripts
origem_scripts = "/root/projeto"
destino_scripts = os.path.join(BASE_DIR, "scripts")

if os.path.exists(origem_scripts):
    arquivos = [f for f in os.listdir(origem_scripts) if f.endswith(".py")]
    for arquivo in arquivos:
        origem = os.path.join(origem_scripts, arquivo)
        destino = os.path.join(destino_scripts, arquivo)
        shutil.copy2(origem, destino)
        print(f"📥 Script copiado: {arquivo} → scripts/")
else:
    print("Pasta /root/projeto não encontrada. Nenhum script foi copiado.")

print("\nEstrutura do projeto criada com sucesso!")


