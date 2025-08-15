import sqlite3

def obter_conexao(db_path="meus_produtos.db"):
    """Retorna conexão com SQLite."""
    return sqlite3.connect(db_path)

def criar_banco():
    conn = obter_conexao()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tb_produtos (
            codigo_fornecedor INTEGER NOT NULL,
            codigo_produto INTEGER NOT NULL,
            codigo_universal INTEGER NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco TEXT NOT NULL,
            PRIMARY KEY (codigo_fornecedor, codigo_produto, codigo_universal)
        )
    ''')
    conn.commit()
    conn.close()

def process_insert_or_update(lista_dados):
    conn = obter_conexao()
    cursor = conn.cursor()
    
    # Lógica para inserir ou atualizar os dados
    
    cursor.executemany('''
    INSERT INTO tb_produtos (codigo_fornecedor, codigo_produto, codigo_universal, nome, descricao, preco)
    VALUES (?, ?, ?, ?, ?, ?)
    ON CONFLICT(codigo_fornecedor, codigo_produto, codigo_universal) DO UPDATE SET
        nome=excluded.nome,
        descricao=excluded.descricao,
        preco=excluded.preco,
        nome=excluded.nome;
    ''', lista_dados)

    conn.commit()
    conn.close()