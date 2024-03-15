# Use a imagem oficial do Python como base
FROM python:3.9

# Define o diretório de trabalho dentro do contêiner
WORKDIR /app

# Copie os arquivos necessários para o diretório de trabalho
COPY requirements.txt .

# Instale as dependências do Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie todo o código-fonte para o diretório de trabalho
COPY . .

# Defina a variável de ambiente PYTHONUNBUFFERED para garantir que a saída do Python seja exibida imediatamente
ENV PYTHONUNBUFFERED 1

# Inicie a aplicação quando o contêiner for iniciado
CMD ["python", "app.py"]
