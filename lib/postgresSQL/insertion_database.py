import pandas as pd
from sqlalchemy import create_engine
import os
from lib.postgresSQL.connexion import connexion_postresql

def push_to_postgres(df_pd:pd.DataFrame, username:str, type_insertion:str ='append'):
    """
    push data in the local postresqlSQL phoebe_ddb
    """
    engine = connexion_postresql()
    df_pd.to_sql('city_bar', engine, if_exists=type_insertion, index=False)