from sqlalchemy import create_engine
from time import time
import pandas as pd
import numpy as np
import argparse
import os


def main(params):

    url = params.url
    user = params.user
    host = params.host
    port = params.port
    password = params.password
    database = params.database
    tablename = params.tablename

    fileName='output.csv.gz'
    os.system(f'wget {url} -O {fileName}')

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{database}')
    engine.connect()

    dtypes ={
        'store_and_fwd_flag':str
        , 'tpep_pickup_datetime': str
        , 'tpep_dropoff_datetime': str
        , 'passenger_count': 'Int64'
        , 'trip_distance': float
        , 'RatecodeID': 'Int64'
        , 'store_and_fwd_flag': str
        , 'PULocationID': 'Int64'
        , 'DOLocationID': 'Int64'
        , 'payment_type': 'Int64'
        , 'fare_amount': float
        , 'extra': float
        , 'mta_tax': float
        , 'tip_amount': float
        , 'tolls_amount': float
        , 'improvement_surcharge': float
        , 'total_amount': float
        , 'congestion_surcharge': float
    }
    df_iter = pd.read_csv(fileName, iterator=True, chunksize=100000, dtype=dtypes, compression= 'gzip')

    df = next(df_iter)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df_header = df.head(0)
    df_header.to_sql(name= tablename, con = engine, if_exists='replace')

    i = 1
    t_total = 0

    while True:

        try:
            t_start = time()

            df = next(df_iter)
            df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
            df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
            df.to_sql(name= tablename, con = engine, if_exists='append')
            
            t_end = time()
            
            
            t_total += (t_end - t_start)
            print(f'{i}º pedaco inserido em {(t_end - t_start):.1f}')
        
            i += 1
        except StopIteration:
            print(f'Insercao finalizada em {t_total} segundos')
            break
            


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Ingest taxi data do postgres')

    parser.add_argument('--host', help='host for posgress')
    parser.add_argument('--port', help='local port for postgres')
    parser.add_argument('--url', help='download url for the data')
    parser.add_argument('--tablename', help='postgress table name')
    parser.add_argument('--database', help='postgres database name')
    parser.add_argument('--user', help='user name for postgres access')
    parser.add_argument('--password', help='password for postgres access')

    args = parser.parse_args()

    print(args)
    main(args)

