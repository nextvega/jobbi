import requests
import json
import os
import pandas as pd
from datetime import datetime
from summary_data import summary
from inserts import summary_data
from upload import send_files_via_ftp

# directorio base
BASEDIR = os.path.dirname(os.path.abspath(__file__)) 

url_api = 'https://dummyjson.com/users'
out_filename_json = os.path.join(BASEDIR,f"files/json/data_{datetime.today().strftime('%Y%m%d')}.json")

response = requests.get(url_api)

if __name__ == "__main__":
    if response.status_code == 200:
        # creacion del json
        with open(out_filename_json, 'w') as f:
            json.dump(response.json(), f)

        # creacion del csv
        with open(out_filename_json, 'r') as f:
            data = json.load(f)

        # creacion del csv
        dataframe = pd.DataFrame(data)
        out_filename_csv = os.path.join(BASEDIR,f"files/csv/ETL_{datetime.today().strftime('%Y%m%d')}.csv")
        dataframe.to_csv(out_filename_csv, index=False)

        # creacion del summary csv
        summary_filename = summary(data['users'])

        # INSERT en la base
        summary_data(summary_filename, out_filename_csv)

        # Envio al FTP
        files_to_send = [out_filename_json, out_filename_csv, summary_filename]
        send_files_via_ftp(files_to_send)

    else:
        print(response)
        error_message = {"error": f"Error en la solicitud: código {response.status_code}"}
        with open(out_filename_json, 'w') as f:
            json.dump(error_message, f)