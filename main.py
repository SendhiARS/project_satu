import os
import connection
import sqlparse
import pandas as pd

if __name__ == '__main__' :
    #conenction data source
    conf = connection.config('marketplace_prod')
    conn, engine = connection.get_conn(conf, 'Datasource')
    cursor = conn.cursor()

    #conection dwh
    conf_dwh = connection.config('dwh')
    conn_dwh, engine_dwh = connection.get_conn(conf_dwh, 'DWH')
    cursor_dwh = conn.cursor()

    #get query string
    path_query = os.getcwd() + '/query/'
    query = sqlparse.format(
        open(path_query + 'query.sql', 'r').read(), strip_connection=True
    ).strip()
    dwh_design = sqlparse.format(
        open(path_query + 'dwh_design.sql', 'r').read(), strip_connection=True
    ).strip()

    try:
    #get data
        print('[INFO] ETL Running..')
        df = pd.read_sql(query, engine)

    #create schema dwh
        cursor_dwh.execute(dwh_design)
        conn_dwh.commit()

    #ingest data to dwh
        df.to_sql(
            'dim_orders_snd',
            engine_dwh,
            schema='public',
            if_exists='append',
            index=False
        )
        print('[INFO] ETL Done..')
        
    except Exception as e:
        print('[INFO] ETL Failed..')
        print(str(e))
