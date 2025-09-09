# API de Transcrição de Áudio com Whisper

Esta é uma API REST para transcrição de áudio usando o modelo Whisper da OpenAI, containerizada com Docker.

## 🚀 Características

- **Endpoint de transcrição**: `/transcribe`
- **Múltiplos formatos**: WAV, MP3, MP4, MPEG, MPGA, M4A, OGG, FLAC
- **Múltiplos idiomas**: Detecção automática ou especificação manual
- **Modelos flexíveis**: tiny, base, small, medium, large
- **Containerizado**: Pronto para deploy com Docker
- **Health check**: Endpoint para monitoramento

## 📁 Estrutura dos Arquivos

```
whisper-transcription-api/
├── app.py              # Aplicação Flask principal
├── Dockerfile          # Configuração do container
├── docker-compose.yml  # Orquestração dos serviços
├── requirements.txt    # Dependências Python
├── test_api.py        # Script para testar a API
└── README.md          # Este arquivo
```

## 🛠️ Instalação e Execução

### Opção 1: Docker Compose (Recomendado)

1. **Clone ou crie os arquivos** em um diretório
2. **Execute o comando**:
   ```bash
   docker-compose up --build
   ```

### Opção 2: Docker Build Manual

1. **Construa a imagem**:
   ```bash
   docker build -t whisper-api .
   ```

2. **Execute o container**:
   ```bash
   docker run -p 5000:5000 whisper-api
   ```

### Opção 3: Execução Local (sem Docker)

1. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Execute a aplicação**:
   ```bash
   python app.py
   ```

## 📡 API Endpoint

### POST `/transcribe`
**Único endpoint da API** - transcreve um arquivo de áudio.

**Parâmetros**:
- `file` (obrigatório): Arquivo de áudio
- `language` (opcional): Código do idioma (ex: 'pt', 'en', 'es')
- `model_size` (opcional): Tamanho do modelo (tiny, base, small, medium, large)

**Exemplo de uso com cURL**:
```bash
curl -X POST \
  -F "file=@audio.wav" \
  -F "language=pt" \
  -F "model_size=base" \
  http://localhost:5000/transcribe
```

**Exemplo com Python requests**:
```python
import requests

with open('audio.wav', 'rb') as f:
    files = {'file': f}
    data = {'language': 'pt', 'model_size': 'base'}
    response = requests.post('http://localhost:5000/transcribe', files=files, data=data)
    result = response.json()
    print(result['transcription'])
```

**Resposta de sucesso**:
```json
{
  "filename": "audio.wav",
  "transcription": "Texto completo da transcrição...",
  "language": "pt",
  "segments": [
    {
      "start": 0.0,
      "end": 3.5,
      "text": "Primeiro segmento de texto..."
    }
  ]
}
```

### Documentação Interativa
Acesse `http://localhost:5000/docs` para a documentação Swagger automática, onde você pode:
- Ver todos os parâmetros detalhadamente
- Testar a API diretamente no navegador
- Ver exemplos de resposta

## 🧪 Testando a API

Use o script de teste fornecido:

```bash
# Instalar requests se necessário
pip install requests

# Teste básico
python test_api.py audio.wav

# Com idioma específico
python test_api.py audio.wav pt

# Com modelo específico
python test_api.py audio.wav pt small
```

## 🔧 Configurações

### Limites da Aplicação
- **Tamanho máximo do arquivo**: 50MB
- **Formatos suportados**: wav, mp3, mp4, mpeg, mpga, m4a, ogg, flac

### Modelos Whisper Disponíveis
- **tiny**: Mais rápido, menos preciso
- **base**: Balanceado (padrão)
- **small**: Boa precisão
- **medium**: Alta precisão
- **large**: Máxima precisão, mais lento

### Variáveis de Ambiente
- `FLASK_ENV`: Ambiente da aplicação (production/development)

## 🐳 Docker

### Volumes
- `whisper_cache`: Cache dos modelos Whisper para melhor performance

### Health Check
O container inclui health check automático que verifica o endpoint `/health` a cada 30 segundos.

## 📊 Monitoramento

### Logs
Os logs da aplicação incluem informações sobre:
- Carregamento dos modelos
- Processamento de arquivos
- Erros e exceções

### Status Codes
- `200`: Sucesso
- `400`: Erro de validação (arquivo inválido, parâmetros incorretos)
- `500`: Erro interno do servidor

## 🚀 Deploy em Produção

### Considerações
1. **Recursos**: Modelos maiores requerem mais RAM e CPU
2. **Storage**: Considere usar volumes persistentes para cache
3. **Segurança**: Implemente autenticação se necessário
4. **Rate Limiting**: Considere limitar requests por usuário
5. **Load Balancer**: Para alta disponibilidade

### Exemplo com nginx
```nginx
upstream whisper_api {
    server localhost:5000;
}

server {
    listen 80;
    server