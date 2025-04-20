# run_all.py

import os
import subprocess
import time

# Executa script e para se der erro
def executar_etapa(nome, script):
    print(f"\n {nome}...")
    try:
        subprocess.run(["python3", script], check=True)
    except subprocess.CalledProcessError:
        print(f"Falha ao executar: {script}. Abortando.")
        exit(1)

if __name__ == "__main__":
    inicio = time.time()

    executar_etapa("Gerando história", "1-generate_historia.py")
    executar_etapa("Gerando narração", "2-generate_audio.py")
    executar_etapa("Calculando duração da narração", "3-minutos_narracao.py")
    executar_etapa("Buscando vídeos para composição", "4-fetch_videos.py")
    executar_etapa("Gerando thumbnail", "5-fetch_thumbnail.py")
    executar_etapa("Montando vídeo final", "6-generate_video.py")
    executar_etapa("Enviando para o YouTube", "7-upload_to_youtube.py")

    fim = time.time()
    duracao = round(fim - inicio, 2)
    print(f"\nProcesso concluído com sucesso em {duracao} segundos!")
