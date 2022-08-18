from sqlmodel import create_engine
from dotenv import load_dotenv
import os

load_dotenv()

def connect_to_db():
    """This method connects to the database using the credentials from .env file"""
    user = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')
    host = os.getenv('DB_HOST')
    port = os.getenv('DB_PORT')
    database = os.getenv('DB_NAME')
    conn_url = 'mysql+pymysql://{user}:{password}@{host}:{port}/{database}'
    return create_engine(conn_url.format(user=user, password=password, host=host, port=port, database=database))

