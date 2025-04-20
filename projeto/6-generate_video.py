# 6-generate_video.py

import os
from moviepy.editor import VideoFileClip, concatenate_videoclips, AudioFileClip

VIDEOS_DIR = "/root/video-generator/assets/videos/clips"
AUDIO_PATH = "/root/video-generator/assets/audio/narracao.wav"
OUTPUT_VIDEO_PATH = "/root/video-generator/assets/videos/video_final.mp4"

# Listar vídeos
video_files = sorted([f for f in os.listdir(VIDEOS_DIR) if f.endswith(('.mp4', '.mov', '.avi'))])
if not video_files:
    raise ValueError("Nenhum vídeo encontrado.")

print(f"Vídeos encontrados: {video_files}")

# Carregar áudio e obter duração
if not os.path.exists(AUDIO_PATH):
    raise FileNotFoundError("Narração não encontrada.")

audio_clip = AudioFileClip(AUDIO_PATH)
duracao_audio = audio_clip.duration

# Carregar vídeos e cortar até a duração do áudio
video_clips = []
tempo_total = 0

for file in video_files:
    path = os.path.join(VIDEOS_DIR, file)
    try:
        clip = VideoFileClip(path).resize(height=1080)

        if tempo_total + clip.duration > duracao_audio:
            restante = duracao_audio - tempo_total
            if restante > 1:
                clip = clip.subclip(0, restante)
                video_clips.append(clip)
                tempo_total += restante
            break
        else:
            video_clips.append(clip)
            tempo_total += clip.duration

        if tempo_total >= duracao_audio:
            break

    except Exception as e:
        print(f"Erro ao carregar {file}: {e}")

if not video_clips:
    raise ValueError("Nenhum clipe válido carregado.")

# Concatenar e adicionar áudio
final_video = concatenate_videoclips(video_clips, method="compose")
final_video = final_video.set_audio(audio_clip)

# Exportar vídeo final
final_video.write_videofile(
    OUTPUT_VIDEO_PATH,
    codec="libx264",
    audio_codec="aac",
    fps=24,
    threads=4,
    preset="ultrafast"
)

print(f"Vídeo final gerado em: {OUTPUT_VIDEO_PATH}")
