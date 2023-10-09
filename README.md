## Pré-requisitos

- Python 3.11.5 instalado em seu sistema.

## Passos para Executar em Modo de Produção

Siga estes passos para configurar e executar seu projeto FastAPI em modo de produção:

```bash
cp .env.example .env
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app