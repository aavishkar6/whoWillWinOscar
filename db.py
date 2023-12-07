from sqlalchemy import create_engine, text
import pandas as pd
import numpy as np

from defaults import (
    DB_USER,
    DB_PASSWORD,
    DB_HOST,
    DB_NAME
)

#returns the engine created above.
def create_sql_engine():
    conn_string = 'mysql+pymysql://{user}:{password}@{host}/{db}?charset={encoding}'.format(
        host = DB_HOST,
        user = DB_USER,
        db = DB_NAME,
        password = DB_PASSWORD,
        encoding = 'utf8mb4')
    
    engine = create_engine(conn_string)

    return engine

def get_data(engine, sql_query):
    with engine.connect() as con:
        data = pd.read_sql(text(sql_query), con=con)

    return (data)
