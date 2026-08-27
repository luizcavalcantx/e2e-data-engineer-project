# Imagem base: Python enxuto, sem ferramenta desnecessária
FROM python:3.11-slim

#Diretorio de trabalho dentro do container
WORKDIR /app

# Copiando só o requirements
COPY requirements.txt .

# Instalando as dependencias
RUN pip install --no-cache-dir -r requirements.txt

# Copiando o restante do código (.dockerignore filtrando o que não deve entrar)
COPY . .

# Program fixo: sempre python
ENTRYPOINT [ "python" ]

# Script padrão (da pra substituir no AirFlow por outro argumento)
CMD ["extract_markets.py"]