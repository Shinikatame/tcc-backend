from dotenv import load_dotenv
from os import getenv

load_dotenv()

USERNAME = getenv('DATABASE_USERNAME')
PASSWORD = getenv('DATABASE_PASSWORD')
HOST = getenv('DATABASE_HOST')
NAME = getenv('DATABASE')

DATABASE_URL =  f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{HOST}/{NAME}'

with open('alembic.example', 'r', encoding = 'UTF-8') as file:
    text = file.read().replace('DATABASE_URL', DATABASE_URL)
    
    with open('alembic.ini', 'w+', encoding = 'UTF-8') as file:
        file.write(text)