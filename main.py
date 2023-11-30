from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database import Base, engine

from importlib import import_module
from os import listdir

app = FastAPI(docs_url = '/')

origins = ['*']

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers = ['*']
)

def load(path = 'routers'): 
    dir = listdir(path)
    dir.sort()

    for file in dir:
        if not file.startswith('_'):
            if file.endswith('.py'):
                module = import_module(f'{path}.{file}'.replace('.py', '').replace('/', '.'))
                app.include_router(module.router)

            else:
                load(path + '/' + file)

load()

if __name__ == '__main__':
    from uvicorn import run
    run(app, host = '0.0.0.0', port = 8000)
