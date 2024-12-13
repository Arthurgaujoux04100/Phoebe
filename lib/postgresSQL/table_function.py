import os
import pandas as pd
from sqlalchemy import create_engine
from lib.postgresSQL.connexion import connexion_postresql


def get_bar_name(city_user:list)->list:
    """
    get the bar name from the postgresql database 
    city_user = city from the user
    return :list
    """
    engine = connexion_postresql()
    query = f"""
        select 
            city_name,
            bar_name
        from city_bar
        where city_name in {tuple(city_user)}"""
    return  pd.read_sql(query, engine).values.tolist()


def get_all_french_cities()->list:
    """get all the french cities from the postgresql database"""
    engine = connexion_postresql()
    return (
        pd.read_sql("""
            select
                city_name 
            from city_bar
            """,
            engine
            )['city_name'].tolist()
    )