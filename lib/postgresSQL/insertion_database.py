import pandas as pd
from sqlalchemy import create_engine
import os

def push_to_postgres(df_pd:pd.DataFrame, username:str, type_insertion:str ='append'):
    """
    push data in the local postresqlSQL phoebe_ddb
    """
    password = os.getenv('phoebe_ddb_pswd')
    host = 'localhost'
    port = '5432'
    database = 'phoebe_ddb'

    connection_string = f'postgresql://{username}:{password}@{host}:{port}/{database}'
    engine = create_engine(connection_string)
    df_pd.to_sql('city_bar', engine, if_exists=type_insertion, index=False)