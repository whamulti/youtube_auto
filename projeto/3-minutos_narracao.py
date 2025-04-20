# 3-minutos_narracao.py

import os
import subprocess
from mutagen.wave import WAVE

# Caminhos dos arquivos
audio_path = "/root/video-generator/assets/audio/narracao.wav"
output_path = "/root/video-generator/assets/audio/duracao.txt"

# Verifica se o arquivo de áudio existe
if not os.path.exists(audio_path):
    raise FileNotFoundError(f"O arquivo de áudio não foi encontrado: {audio_path}")

duracao_segundos = None

try:
    # Usar Mutagen para WAV
    audio = WAVE(audio_path)
    if hasattr(audio.info, "length") and audio.info.length > 0:
        duracao_segundos = int(audio.info.length)
        print(f"Duração detectada via Mutagen: {duracao_segundos} segundos")
    else:
        raise ValueError("⚠️ Mutagen não conseguiu detectar a duração.")

except Exception as e:
    print(f" Erro com Mutagen: {e}. Tentando com FFmpeg...")

    try:
        ffmpeg_cmd = [
            "ffprobe", "-v", "error",
            "-show_entries", "format=duration",
            "-of", "default=noprint_wrappers=1:nokey=1",
            audio_path
        ]
        result = subprocess.run(ffmpeg_cmd, capture_output=True, text=True)
        duracao_segundos = int(float(result.stdout.strip()))
        print(f"Duração detectada via FFmpeg: {duracao_segundos} segundos")
    except Exception as ffmpeg_error:
        raise RuntimeError(f"Não foi possível obter a duração do áudio: {ffmpeg_error}")

# Salva a duração no arquivo
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(str(duracao_segundos))

print(f"Arquivo salvo: {output_path} (Duração: {duracao_segundos} segundos)")
