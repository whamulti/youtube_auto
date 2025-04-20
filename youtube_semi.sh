#!/bin/bash

echo "Tornando setup.sh executável..."
chmod +x setup.sh

echo "Executando setup.sh..."
./setup.sh

echo "Acessando diretório de scripts..."
cd /root/video-generator/scripts || exit 1

echo "Criando ambiente virtual (caso não exista)..."
python3 -m venv venv

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências do projeto..."
pip install -r /root/video-generator/requirements.txt

echo "Copiando arquivo de credenciais para o local correto..."
cp /root/credentials.json /root/video-generator/credentials.json

echo "Executando pipeline completa do projeto..."
python3 run_all.py
