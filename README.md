Colocar na pasta /root ( projeto, credentials.json, requirements.txt, setup.sh, setup_projeto.py e youtube_semi.sh )


Executar script inicial
```

chmod +x setup.sh
```
```

./setup.sh

```
---

Entrar no ambiente virtual
```
cd video-generator/scripts
```
```
python3 -m venv venv
```
```
source venv/bin/activate
```
---

Execução dos scripts
```
pip install -r /root/video-generator/requirements.txt
```
```
python3 1-generate_historia.py
```
```
python3 2-generate_audio.py
```
```
python3 3-minutos_narracao.py
```
```
python3 4-fetch_videos.py
```
```
python3 5-fetch_thumbnail.py
```
```
python3 6-generate_video.py
```
```
python3 7-upload_to_youtube.py
```
---

Executar todos no semiautomático
```
chmod +x youtube_semi.sh
```
```
./youtube_semi.sh
```








