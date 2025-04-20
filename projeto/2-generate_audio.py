# 2-generate_audio.py

import os
from TTS.api import TTS

# Caminhos
script_path = "/root/video-generator/assets/texto/historia.txt"
output_dir = "/root/video-generator/assets/audio"
os.makedirs(output_dir, exist_ok=True)
output_audio = os.path.join(output_dir, "narracao.wav")

# Verifica se o arquivo de texto existe
if not os.path.exists(script_path):
    raise FileNotFoundError(f"O arquivo de script não foi encontrado: {script_path}")

# Lê o texto
with open(script_path, "r", encoding="utf-8") as f:
    texto = f.read().strip()

if not texto:
    raise ValueError("O texto está vazio.")

# Modelo multilíngue que suporta português (voz natural)
print("Carregando modelo de voz multilíngue do Coqui TTS...")
model_name = "tts_models/multilingual/multi-dataset/your_tts"
tts = TTS(model_name)

# Buscar nome exato do speaker desejado (male-pt-3)
speaker = next(s for s in tts.speakers if "male-pt-3" in s)
language = "pt-br"

# Mostra os speakers disponíveis
print(f"🗣️ Vozes disponíveis: {[s.strip() for s in tts.speakers]}")

# Gera e salva o áudio
print(f"Gerando narração com a voz: {speaker.strip()}...")
tts.tts_to_file(text=texto, speaker=speaker, language=language, file_path=output_audio)
print(f"Narração salva em: {output_audio}")
