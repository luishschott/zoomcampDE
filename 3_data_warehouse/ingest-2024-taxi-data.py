import sys
import os
from tqdm import tqdm
from google.cloud import storage

def download(taxi_color, year, month):
    filename = f'{taxi_color}_tripdata_{year}-{month}.parquet'
    os.system(f'wget https://d37ci6vzurychx.cloudfront.net/trip-data/{filename} -O {filename}' )
    print(f'{filename} DOWNLOADED')


def upload_to_bucket(taxi_color, year, month):

    storage_client = storage.Client()
    bucket_name = "taxi_data_448017"
    filename = f"{taxi_color}_tripdata_{year}-{month}.parquet"
    bucket = storage_client.get_bucket(bucket_name)
    blob = bucket.blob(filename)

    print(f"UPLOADING: {filename}")

    blob.upload_from_filename(filename)

    print(f"{filename} UPLOADED.")


def main():
    year = '2024'
    taxi = 'yellow'

    for i in range(1,8):
        month = f'{i:02}'

        download('yellow', '2024', month)
        upload_to_bucket('yellow', '2024', month)


if __name__ == '__main__':

    main()

