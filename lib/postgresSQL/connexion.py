from sqlalchemy import create_engine
import os

def connexion_postresql():
    """
    connexion postgreSQL database
    """
    password = os.getenv('phoebe_ddb_pswd')
    host = 'localhost'
    port = '5432'
    database = 'phoebe_ddb'
    connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    return create_engine(connection_string)