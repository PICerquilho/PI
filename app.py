from flask import Flask, render_template, request, jsonify
import sqlite3
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def get_db_connection():
    conn = sqlite3.connect('alunos.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastrar', methods=['POST'])
def cadastrar():
    rg = request.form['rg']
    nome = request.form['nome']
    sala = request.form['sala']
    foto = request.files['foto']

    if foto and allowed_file(foto.filename):
        filename = secure_filename(foto.filename)
        foto.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        foto_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    else:
        foto_path = None

    conn = get_db_connection()
    conn.execute('INSERT INTO alunos (rg, nome, foto, sala) VALUES (?, ?, ?, ?)', (rg, nome, foto_path, sala))
    conn.commit()
    conn.close()

    return 'Aluno cadastrado com sucesso!'

@app.route('/buscar', methods=['GET'])
def buscar():
    termo_busca = request.args.get('termo_busca')

    conn = get_db_connection()
    alunos = conn.execute('SELECT * FROM alunos WHERE nome LIKE ?', ('%' + termo_busca + '%',)).fetchall()
    conn.close()

    resultados = [{'rg': aluno['rg'], 'nome': aluno['nome'], 'foto': aluno['foto'], 'sala': aluno['sala']} for aluno in alunos]
    return jsonify(resultados)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'gif'}

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)