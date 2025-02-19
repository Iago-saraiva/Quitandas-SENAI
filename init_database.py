import sqlite3

conn = sqlite3.connect('quitandas.db')
c = conn.cursor()

# Criação da tabela de usuários
c.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        senha TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
