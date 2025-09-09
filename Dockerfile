# Usar imagem base leve com Python
FROM python:3.10-slim

# Definir diretório de trabalho
WORKDIR /app

# Instalar dependências do sistema necessárias para áudio e ffmpeg
RUN apt-get update && apt-get install -y \
  ffmpeg \
  git \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements
COPY requirements.txt .

# Instalar dependências Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY app.py .

# Criar diretório para uploads temporários
RUN mkdir -p /tmp/uploads

# Expor a porta do FastAPI
EXPOSE 5000

# Rodar o servidor com Uvicorn (melhor prática p/ FastAPI)
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "5000"]
