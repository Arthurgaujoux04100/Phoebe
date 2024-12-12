import pandas as pd
import polars as pl
import argparse
from lib.postgresSQL.insertion_database import push_to_postgres

def get_city_table_tranform():
    """
    transform city_table for postresql database
    """
    return (
        pl.read_excel('raw_data/ville_barreau.xlsx')
        .select(
            pl.col('codgeo').cast(pl.Utf8),
            pl.col('libgeo').cast(pl.Utf8).alias('city_name'),
            pl.col('tj_libgeo').cast(pl.Utf8).alias('bar_name'),
        )
        .to_pandas()
    )

def main(city_table:bool):
    if city_table:
        push_to_postgres(df_pd=get_city_table_tranform(), username='arthurgaujoux', type_insertion='replace')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-ct", "--city_table", help="trigger city_table insertion into database", action='store_true')
    args = parser.parse_args()
    main(args.city_table)
