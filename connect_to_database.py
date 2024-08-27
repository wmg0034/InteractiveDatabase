import pandas as pd
import sqlalchemy as sa
from sqlalchemy.engine import URL
from sqlalchemy import create_engine

conn_str = (
    r"Driver={SQL Server};"
    r"Server=DESKTOP-0632H95\SQLEXPRESS;"
    r"Database=Pokemon;"
    r"Trusted_Connection=yes;"
    )

connection_url = URL.create("mssql+pyodbc", query={"odbc_connect": conn_str})
engine = create_engine(connection_url)

def get_table(  hp_slider, 
                atk_slider, 
                dfs_slider, 
                spatk_slider, 
                spdfs_slider, 
                spd_slider,
                type1_select,
                type2_select,
                gen_select):
    
    #It's possible this is the dumbest way to solve this problem, but here we pass a big query to the database based on the ranges and selections the user has made.
    query = "SELECT * FROM Poke_Table WHERE "
    query += 'HP >= %d AND HP <= %d AND ' %(hp_slider[0], hp_slider[1])
    query += 'Attack >= %d AND Attack <= %d AND ' %(atk_slider[0], atk_slider[1])
    query += 'Defense >= %d AND Defense <= %d AND ' %(dfs_slider[0], dfs_slider[1])
    query += 'SpAttack >= %d AND SpAttack <= %d AND ' %(spatk_slider[0], spatk_slider[1])
    query += 'SpDefense >= %d AND SpDefense <= %d AND ' %(spdfs_slider[0], spdfs_slider[1])
    query += 'Speed >= %d AND Speed <= %d AND ' %(spd_slider[0], spd_slider[1])
    
    if len(type1_select) == 1:
        query += r"Type1 LIKE '%" + type1_select[0] + r"%' AND "
    if len(type1_select) > 1:    
        query += 'Type1 IN {} AND '.format(tuple(type1_select))


    if len(type2_select) == 1:
        query += r"Type2 LIKE '%" + type2_select[0] + r"%' AND "
    if len(type2_select) > 1:    
        query += 'Type2 IN {} AND '.format(tuple(type2_select))
    

    if len(gen_select) == 1:
        num = gen_select[0]
        query += "Generation = %d" %num
    if len(gen_select) > 1:    
        query += 'Generation IN {}'.format(tuple(gen_select))

    with engine.begin() as conn:
        df = pd.read_sql_query(sa.text(query), conn)
    return(df)