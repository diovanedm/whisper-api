from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import whisper
import tempfile
import os
import logging
from typing import Optional

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Whisper Transcription API", version="1.0.0")

# Formatos de áudio suportados
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'mp4', 'mpeg', 'mpga', 'm4a', 'ogg', 'flac'}

# Carregar o modelo Whisper
logger.info("Carregando modelo Whisper...")
model = whisper.load_model("base")
logger.info("Modelo Whisper carregado com sucesso!")

def is_allowed_file(filename: str) -> bool:
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.post("/transcribe")
async def transcribe(
    file: UploadFile = File(...),
    language: Optional[str] = Form(None),
    model_size: Optional[str] = Form("base")
):
    """
    Transcrever arquivo de áudio usando Whisper
    
    - **file**: Arquivo de áudio (obrigatório)
    - **language**: Código do idioma (opcional, ex: 'pt', 'en')
    - **model_size**: Tamanho do modelo (opcional: tiny, base, small, medium, large)
    """
    
    try:
        # Verificar se o arquivo tem extensão válida
        if not is_allowed_file(file.filename):
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Tipo de arquivo não suportado",
                    "supported_formats": list(ALLOWED_EXTENSIONS),
                    "received": file.filename.rsplit('.', 1)[1].lower() if '.' in file.filename else 'sem extensão'
                }
            )
        
        # Usar modelo diferente se solicitado
        current_model = model
        if model_size != 'base':
            if model_size in ['tiny', 'small', 'medium', 'large']:
                logger.info(f"Carregando modelo {model_size}...")
                current_model = whisper.load_model(model_size)
            else:
                raise HTTPException(
                    status_code=400,
                    detail={
                        "error": "Tamanho de modelo inválido",
                        "available_sizes": ["tiny", "base", "small", "medium", "large"]
                    }
                )
        
        # Salvar arquivo temporariamente
        file_extension = file.filename.rsplit('.', 1)[1].lower()
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_path = temp_file.name
        
        logger.info(f"Processando arquivo: {file.filename}")
        
        # Fazer a transcrição
        if language:
            result = current_model.transcribe(temp_path, language=language, verbose=False)
        else:
            result = current_model.transcribe(temp_path, verbose=False)
        
        # Limpar arquivo temporário
        os.unlink(temp_path)
        
        logger.info("Transcrição concluída com sucesso")
        
        # Retornar resultado
        return {
            "filename": file.filename,
            "transcription": result["text"].strip(),
            "language": result.get("language", "auto-detectado"),
            "segments": [
                {
                    "start": round(segment["start"], 2),
                    "end": round(segment["end"], 2),
                    "text": segment["text"].strip()
                }
                for segment in result["segments"]
            ]
        }
    
    except HTTPException:
        raise
    except Exception as e:
        # Limpar arquivo temporário em caso de erro
        try:
            if 'temp_path' in locals():
                os.unlink(temp_path)
        except:
            pass
        
        logger.error(f"Erro na transcrição: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Erro interno do servidor",
                "message": "Erro ao processar o arquivo de áudio"
            }
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)