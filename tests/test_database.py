import sqlite3
import pytest
import sys
import os

# Adiciona a pasta raiz do projeto ao PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.database import process_insert_or_update

@pytest.fixture
def db_memoria():
    """Cria um banco SQLite em memória com tabela e chave composta."""
    conn = sqlite3.connect("file::memory:?cache=shared", uri=True)
    cur = conn.cursor()
    cur.execute("""
         CREATE TABLE IF NOT EXISTS tb_produtos (
            codigo_fornecedor INTEGER NOT NULL,
            codigo_produto INTEGER NOT NULL,
            codigo_universal INTEGER NOT NULL,
            nome TEXT NOT NULL,
            descricao TEXT NOT NULL,
            preco TEXT NOT NULL,
            PRIMARY KEY (codigo_fornecedor, codigo_produto, codigo_universal)
        )
    """)
    conn.commit()
    yield conn
    conn.close()

def test_insert_on_conflict_update(db_memoria, monkeypatch):
    # Substitui a função de conexão para usar o banco em memória
    monkeypatch.setattr("app.database.obter_conexao", lambda: sqlite3.connect("file::memory:?cache=shared", uri=True))

    # 1. Inserção inicial
    lista_produtos = [
        (1, 101, 1234567890123, "Produto A", "Descrição A", "10.00")
    ]

    process_insert_or_update(lista_produtos)

    cur = db_memoria.cursor()
    cur.execute("SELECT preco FROM tb_produtos WHERE codigo_fornecedor=? AND codigo_produto=?", ("1", "101"))
    assert cur.fetchone()[0] == "10.00"

    lista_produtos_atualizar = [
        (1, 101, 1234567890123, "Produto A", "Descrição A", "20.00")
    ]

    # 2. Atualização pelo conflito de chave composta
    process_insert_or_update(lista_produtos_atualizar)

    cur.execute("SELECT preco FROM tb_produtos WHERE codigo_fornecedor=? AND codigo_produto=?", ("1", "101"))
    assert cur.fetchone()[0] == "20.00"

def test_inserir_registro_diferente(db_memoria, monkeypatch):
    monkeypatch.setattr("app.database.obter_conexao", lambda: sqlite3.connect("file::memory:?cache=shared", uri=True))

    lista_produtos_adicionar = [
        (1, 102, 1234567890124, "Produto B", "Descrição B", "40.00"),
        (2, 201, 1234567890125, "Produto C", "Descrição C", "60.00")
    ]
    process_insert_or_update(lista_produtos_adicionar)

    cur = db_memoria.cursor()
    cur.execute("SELECT COUNT(*) FROM tb_produtos")
    assert cur.fetchone()[0] == 2
