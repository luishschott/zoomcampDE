# ZoomcampDE

Gerneral Zoomcamp DE Bootcamp repository

SQL queries for the WEEK 1 homework
====================================

**QUESTION 3:**

    WITH base as (
        SELECT
            lpep_pickup_datetime
            , trip_distance
        FROM "2019_yellow_taxi_data"
        WHERE 
            lpep_pickup_datetime >= '2019-10-01'
            AND lpep_dropoff_datetime < '2019-11-01'
        ORDER BY trip_distance ASC
    ),

    up_1_mile as (
        SELECT
            count(*)
        FROM base
        WHERE trip_distance <= 1
    ),

    from_1_to_3 as (
        SELECT
            COUNT(*)
        FROM base
        WHERE trip_distance > 1 AND trip_distance <= 3
    ),

    from_3_to_7 as (
        SELECT
            COUNT(*)
        FROM base
        WHERE trip_distance > 3 AND trip_distance <= 7
    ),

    from_7_to_10 as (
        SELECT
            COUNT(*)
        FROM base
        WHERE trip_distance > 7 AND trip_distance <= 10
    ),

    over_10 as (
        SELECT
            COUNT(*)
        FROM base
        WHERE trip_distance > 10
    )

    SELECT * FROM up_1_mile
    UNION ALL
    SELECT * FROM from_1_to_3
    UNION ALL
    SELECT * FROM from_3_to_7
    UNION ALL
    SELECT * FROM from_7_to_10
    UNION ALL
    SELECT * FROM over_10


**QUESTION 4:**

    SELECT
        lpep_pickup_datetime
        , trip_distance
    FROM public."2019_yellow_taxi_data"
    WHERE trip_distance = (
        SELECT 
            MAX(trip_distance)
        FROM public."2019_yellow_taxi_data" 
    )


**QUESTION 5:** 

    SELECT 
        zdata."Zone"
        , tdata."PULocationID"
        , SUM(tdata.total_amount)
        
    FROM public."2019_yellow_taxi_data" as tdata 
        LEFT JOIN public.taxi_zones_lookup as zdata
        ON tdata."PULocationID" = zdata."LocationID"
    WHERE lpep_pickup_datetime::date = '2019-10-18'
    GROUP BY "PULocationID", "Zone"
    HAVING SUM(total_amount) >= 13000
    ORDER BY SUM(total_amount) DESC


**QUESTION 6:**

    SELECT
        tdata.index
        , tdata.lpep_pickup_datetime
        , tdata.tip_amount
        , tdata."PULocationID"
        , pudata."Zone" as "PUzone"
        , tdata."DOLocationID"
        , dodata."Zone" as "DOzone"
    FROM public."2019_yellow_taxi_data" as tdata 
        LEFT JOIN public.taxi_zones_lookup as pudata
        ON tdata."PULocationID" = pudata."LocationID"
        LEFT JOIN public.taxi_zones_lookup as dodata
        ON tdata."DOLocationID" = dodata."LocationID"
    WHERE 
        pudata."Zone" = 'East Harlem North'
        AND tdata.lpep_pickup_datetime >= '2019-10-01'
        AND tdata.lpep_pickup_datetime < '2019-11-01'
    ORDER BY tdata.tip_amount DESC
    LIMIT 5


SQL queries for the WEEK 3 homework
====================================

### create tables

    CREATE OR REPLACE EXTERNAL TABLE `terraform-demo-448017.zoomcamp.yellow_tripdata_2024_external`
        OPTIONS(
            format = 'PARQUET',
            uris = ['gs://taxi_data_448017/yellow_tripdata_2024-*.parquet']
        );

    CREATE TABLE `terraform-demo-448017.zoomcamp.yellow_tripdata_2024` AS(
        SELECT * FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024_external`
    );


### Q2

    SELECT COUNT(DISTINCT(PULocationID)) FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024`;
    SELECT COUNT(DISTINCT(PULocationID)) FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024_external`;

### Q3

    SELECT PULocationID FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024`;
    SELECT PULocationID, DOLocationID FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024`;

### Q4

    SELECT COUNT(fare_amount) FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024` WHERE fare_amount = 0;

### Q5

    CREATE TABLE `terraform-demo-448017.zoomcamp.yellow_tripdata_2024_partitioned`
        PARTITION BY DATE(tpep_dropoff_datetime)
        CLUSTER BY VendorID
        AS(
            SELECT * FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024_external`
        );

### Q6

    SELECT DISTINCT(VendorID) FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024` WHERE tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15';
    SELECT DISTINCT(VendorID) FROM `terraform-demo-448017.zoomcamp.yellow_tripdata_2024_partitioned` WHERE tpep_dropoff_datetime >= '2024-03-01' and tpep_dropoff_datetime <= '2024-03-15';