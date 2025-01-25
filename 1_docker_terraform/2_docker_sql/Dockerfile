FROM python:3.9

RUN apt-get install wget
RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY ingesting_yellow_taxi_data.py ingesting_yellow_taxi_data.py

ENTRYPOINT [ "python", "ingesting_yellow_taxi_data.py" ]