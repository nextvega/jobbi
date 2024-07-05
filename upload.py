import os
from dotenv import load_dotenv
from ftplib import FTP

load_dotenv()

BASEDIR = os.path.dirname(os.path.abspath(__file__)) 

hostname = '127.0.0.1'
port = 8080
username = os.getenv('FTP_USERNAME')
password = os.getenv('FTP_PASSWORD')

def send_files_via_ftp(files):
    try:
        # Crear conexión FTP
        ftp = FTP()
        ftp.connect(hostname, 8080)
        ftp.login(username, password)

        # Subir archivos al servidor FTP
        for file in files:
            with open(file, 'rb') as f:
                # Obtener el nombre base del archivo
                filename = os.path.basename(file)
                # Subir el archivo al servidor FTP
                ftp.storbinary(f'STOR {filename}', f)

        # Cerrar conexión FTP
        ftp.quit()
        print("Archivos enviados exitosamente al servidor FTP.")

    except Exception as e:
        print(f"Error: {e} - Compruebe si el servidor esta activo")