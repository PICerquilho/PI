import sqlite3

def criar_banco_dados():
    conn = sqlite3.connect('alunos.db')
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS alunos (
            rg TEXT PRIMARY KEY,
            nome TEXT,
            foto TEXT,
            sala TEXT
        )
    ''')

    conn.commit()
    conn.close()

if __name__ == '__main__':
    criar_banco_dados()
    print("Banco de dados e tabela criados com sucesso!")