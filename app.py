from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('quitandas.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/cadastro', methods=['POST'])
def cadastro():
    nome = request.form['nome']
    email = request.form['email']
    senha = request.form['senha']

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM usuarios WHERE email = ?', (email,))
    user = cursor.fetchone()
    if user:
        return jsonify({"error": "Este e-mail já está cadastrado!"})

    cursor.execute('INSERT INTO usuarios (nome, email, senha) VALUES (?, ?, ?)', (nome, email, senha))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    senha = request.form['senha']

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios WHERE email = ? AND senha = ?', (email, senha))
    user = cursor.fetchone()
    
    conn.close()

    if user:
        session['user'] = user["name"]
        return redirect(url_for('compras'))
    else:
        return jsonify({"error": "E-mail ou senha incorretos!"})

@app.route('/compras')
def compras():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('compras.html')

@app.route('/escolher_entrega', methods=['POST'])
def escolher_entrega():
    tipo_entrega = request.form['tipo_entrega']
    session['tipo_entrega'] = tipo_entrega
    if tipo_entrega == 'Retirada':
        return redirect(url_for('pagamento'))
    else:
        return redirect(url_for('endereco'))

@app.route('/endereco', methods=['GET', 'POST'])
def endereco():
    if 'user' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        endereco = request.form['endereco']
        session['endereco'] = endereco
        return redirect(url_for('pagamento'))

    return render_template('endereco.html')

@app.route('/pagamento', methods=['GET', 'POST'])
def pagamento():
    if 'user' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        forma_pagamento = request.form['forma_pagamento']
        session['forma_pagamento'] = forma_pagamento
        return redirect(url_for('acompanhamento'))

    return render_template('pagamento.html')

@app.route('/acompanhamento')
def acompanhamento():
    if 'user' not in session:
        return redirect(url_for('index'))
    return render_template('acompanhamento.html')

if __name__ == '__main__':
    app.run(debug=True)
