import argparse
import pandas as pd
from schemas.card import Card, CardCreate
from db.conn import connect_to_db
from sqlalchemy.orm import Session
from db import models

engine = connect_to_db()

def import_cards_from_csv(csv_file:str):
    """Importa os cards de um arquivo csv para o banco de dados.
    - csv_file: caminho do arquivo csv
    """
    df = pd.read_csv(csv_file, encoding='utf-8', delimiter=',')
    print(f'{df.shape[0]} cards para importar')
    for _, row in df.iterrows():
        print(row)
        text = row['text']
        tags = row['tag'].split(';')
        card_db = models.Card(texto=text)
        for tag in tags:
            card_db.tags.append(models.Tag(name=tag))
        with Session(engine, expire_on_commit=False) as session:
            try:
                session.add(card_db)
                session.commit()
                session.refresh(card_db)
            except Exception as e:
                raise e
    print('Importação concluída')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-f --file', dest='csv_file', type=str, help='caminho para o arquivo csv', required=True)
    args = parser.parse_args()
    import_cards_from_csv(args.csv_file)
    print('Importação concluída')