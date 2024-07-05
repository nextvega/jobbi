from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
import os

basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'db.sqlite3')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +db_path
db = SQLAlchemy(app)

class process_table(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    execution_date = db.Column(db.String(50), nullable=False)
    summary_filename = db.Column(db.String(100), nullable=False)
    etl_filename = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f'<Process {self.id} - {self.execution_date} - {self.summary_filename} - {self.etl_filename}>'


@app.route('/')
def index():
    # Ejemplo de consulta a la base de datos
    # usuarios = Usuario.query.all()
    # return render_template('index.html', usuarios=usuarios)
    processes = process_table.query.all()
    return render_template('index.html',  processes=processes)

if __name__ == '__main__':
    app.run(debug=True)