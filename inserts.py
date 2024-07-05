import os
import sqlite3
import pandas as pd
from datetime import datetime

BASEDIR = os.path.dirname(os.path.abspath(__file__)) 
db = sqlite3.connect(os.path.join(BASEDIR, "db.sqlite3"))
cursor = db.cursor

def summary_data(file_summary, file_etl):
    df_summary = pd.read_csv(file_summary)
    df_etl = pd.read_csv(file_etl)

    summary_data = df_summary.to_json(orient='records')
    etl_data = df_etl.to_json(orient='records')
    try:
        db = sqlite3.connect(os.path.join(BASEDIR, "db.sqlite3"))
        cursor = db.cursor()

        # Registrar la información de proceso en una tabla de procesos
        execution_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO process_table (execution_date, summary_filename, etl_filename) VALUES (?, ?, ?)", (execution_date, summary_data, etl_data))
        db.commit()

        print("Datos guardados exitosamente en la base de datos SQLite.")

    except sqlite3.Error as e:
        print(f"Error al trabajar con la base de datos SQLite: {e}")