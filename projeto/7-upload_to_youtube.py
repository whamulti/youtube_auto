# 7-upload_to_youtube.py

import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# 🔹 Escopo de acesso para fazer o upload no YouTube
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

# 🔹 Caminhos dos arquivos
CLIENT_SECRET_FILE = '/root/video-generator/credentials.json'
VIDEO_PATH = "/root/video-generator/assets/videos/video_final.mp4"
THUMBNAIL_PATH = "/root/video-generator/assets/images/thumbnail.jpg"
HISTORIA_PATH = "/root/video-generator/assets/texto/historia.txt"

# 🔹 Verifica se os arquivos necessários existem
for file_path in [CLIENT_SECRET_FILE, VIDEO_PATH, THUMBNAIL_PATH, HISTORIA_PATH]:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo não encontrado: {file_path}")

# 🔹 Função para autenticar e obter o serviço da API
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    flow.redirect_uri = 'http://localhost'

    auth_url, _ = flow.authorization_url(prompt='consent')
    print(f"Acesse a URL abaixo, autorize e cole o código gerado:\n{auth_url}")

    code = input("Cole o código de autorização aqui: ")
    flow.fetch_token(code=code)

    return build('youtube', 'v3', credentials=flow.credentials)

# 🔹 Função para gerar título e descrição com base na história
def gerar_titulo_descricao(historia_path):
    with open(historia_path, "r", encoding="utf-8") as f:
        historia = f.read().strip()

    # Criar título atrativo baseado nas primeiras palavras da história
    palavras_historia = historia.split()
    titulo = f"Passagem bíblica: {' '.join(palavras_historia[:5])}..."

    # Criar descrição utilizando a história
    descricao = f"""
Este vídeo mergulha na incrível história de {' '.join(palavras_historia[:10])}...
Descubra os detalhes e explore cada mistério revelado.

Assista agora e embarque nessa história!

#História #Mistério #Descobertas
"""
    return titulo, descricao

# 🔹 Função para fazer o upload do vídeo
def upload_video(file_path, titulo, descricao, category, tags, thumbnail_path):
    youtube = get_authenticated_service()

    request_body = {
        'snippet': {
            'title': titulo,
            'description': descricao,
            'tags': tags,
            'categoryId': category
        },
        'status': {
            'privacyStatus': 'private'  # ou 'public' ou 'unlisted'
        }
    }

    try:
        print(f"Enviando vídeo: {titulo}...")
        media_file = MediaFileUpload(file_path, chunksize=-1, resumable=True, mimetype="video/mp4")
        request = youtube.videos().insert(part="snippet,status", body=request_body, media_body=media_file)
        response = request.execute()
        video_id = response['id']
        print(f"Vídeo '{titulo}' enviado com sucesso! ID do vídeo: {video_id}")

        # 🔹 Upload da Thumbnail
        print(f"Enviando thumbnail...")
        youtube.thumbnails().set(videoId=video_id, media_body=MediaFileUpload(thumbnail_path)).execute()
        print("Thumbnail enviada com sucesso!")

    except HttpError as e:
        print(f"Erro ao enviar vídeo: {e}")

# 🔹 Gerar título e descrição com base na história
titulo, descricao = gerar_titulo_descricao(HISTORIA_PATH)

# 🔹 Categoria do vídeo no YouTube (22 = "People & Blogs")
video_category = "22"
video_tags = ["história", "mistério", "descobertas"]

# 🔹 Chamada para fazer o upload
upload_video(VIDEO_PATH, titulo, descricao, video_category, video_tags, THUMBNAIL_PATH)
