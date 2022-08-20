import pandas as pd
from sqlalchemy.orm import Session
from schemas.card import Card, CardCreate
from db.conn import connect_to_db, connect_to_sqlite_db
from db import models
from db.crud import DBCrud

engine = connect_to_sqlite_db()

crud = DBCrud()

def cards_from_csv(csv_file:str):
    """Importa os cards de um arquivo csv para o banco de dados.
    - csv_file: caminho do arquivo csv
    """
    df = pd.read_csv(csv_file, encoding='utf-8', delimiter=',')
    df.fillna('', inplace=True) # substitui os valores nulos por vazio
    print(f'{df.shape[0]} cards para importar')
    for index, row in df.iterrows(): # para cada linha do dataframe
        text = row['text'] # pega o texto da linha
        tags = row['tag'] # pega as tags da linha
        if tags: # se existirem tags
            tags = tags.split(';') # separa as tags por ponto e vírgula em uma lista
        tags = [{"name": tag} for tag in tags] # cria um dicionário para cada tag e adiciona a lista de tags
        try:
            card = CardCreate(texto=text, tags=tags) # cria um card com as informações do dataframe
            crud.create_card(card) # importa o card para o banco de dados
        except Exception as e: # se houver erro
            print(f'Erro ao importar card {text}') # imprime o erro
            print(e)
            continue # continua para o próximo card