# setup.sh

echo "Atualizando e limpando o sistema..."
apt update -y && apt upgrade -y && apt autoremove -y

echo "Instalando pacotes necessários do sistema..."
apt install -y python3 python3-venv python3-pip ffmpeg libsndfile1

echo "Criando ambiente virtual em /root/video-generator/venv ..."
python3 -m venv /root/video-generator/venv

echo "Instalando dependências do projeto..."
source /root/video-generator/venv/bin/activate
pip install -r /root/requirements.txt

echo "Criando estrutura de diretórios, arquivos e copiando scripts..."
python3 /root/setup_projeto.py

# Move o requirements.txt para o lugar correto, se ainda estiver fora
if [ -f /root/requirements.txt ]; then
    mv /root/requirements.txt /root/video-generator/
    echo "requirements.txt movido para /root/video-generator/"
fi

echo ""
echo "Setup concluído com sucesso!"
