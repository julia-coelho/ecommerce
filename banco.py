#Aluna: Júlia Coelho Rodrigues
#RA: 22408388

import sqlite3

#responsavel por conexao e estrutura do banco

#caminho ao arquivo do banco
caminho_banco = 'ecommerce.db'


#conectar ao banco de dados
def get_conexao():
    return sqlite3.connect(caminho_banco)


#criar tabelas
def criar_tabelas(conexao):
    cursor = conexao.cursor()

    #criar a tabela categorias
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS categorias(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT UNIQUE NOT NULL
    )
    """)


    #criar a tabela produtos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS produtos(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                marca TEXT NOT NULL,
                categoria_id INTEGER,
                preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),
                desconto_unitario REAL DEFAULT 0 CHECK(desconto_unitario >= 0 AND desconto_unitario <= preco_unitario),
                FOREIGN KEY (categoria_id) REFERENCES categorias(id) ON DELETE RESTRICT
                UNIQUE (nome, marca)     -- dois produtos podem ter o mesmo nome desde que não sejam da mesma marca
    )
    """)

    #criar a tabela clientes
    #todas as datas em formato iso: 'YYYY-MM-DD'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clientes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   email TEXT UNIQUE NOT NULL,
                   senha_hash TEXT NOT NULL,
                   aniversario TEXT NOT NULL,
                   telefone TEXT UNIQUE NOT NULL,
                   endereco TEXT NOT NULL,      -- endereco esta em formato JSON string
                   data_cadastro TEXT NOT NULL
    )
    """)

    #criar a tabela pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pedidos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   cliente_id INTEGER NOT NULL,
                   total_final REAL NOT NULL CHECK(total_final >= 0),
                   total_sem_desconto REAL NOT NULL CHECK(total_sem_desconto >= 0 AND total_sem_desconto >= total_final),
                   desconto_global REAL DEFAULT 0 CHECK(desconto_global >= 0 AND desconto_global <= total_sem_desconto),
                   data TEXT NOT NULL,
                   FOREIGN KEY (cliente_id) REFERENCES clientes(id) ON DELETE RESTRICT
    )
    """)
    
    #criar tabela pagamentos
    #todas as datas em formato iso: 'YYYY-MM-DD'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS pagamentos(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,        
                   pedido_id INTEGER NOT NULL,
                   total REAL NOT NULL CHECK(total > 0),
                   tipo TEXT NOT NULL CHECK(tipo IN ('debito', 'credito', 'boleto', 'pix', 'paypal')),
                   status TEXT NOT NULL CHECK(status IN ('pendente', 'pago', 'falhou', 'cancelado', 'em disputa')),
                   transacao_id TEXT UNIQUE NOT NULL,       -- codigo da operadora/pagamento
                   data_pagamento TEXT,     -- NULL se ainda nao foi pago
                   pagador_nome TEXT NOT NULL,
                   endereco_conta TEXT NOT NULL,        -- ex: email do paypal, numero do cartao (hash)
                   FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE RESTRICT
    )
    """)
    
    #criar tabela itens_pedido
    #sao os itens dos pedidos
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS itens_pedido(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   produto_id INTEGER NOT NULL,
                   pedido_id INTEGER NOT NULL,
                   quantidade INTEGER NOT NULL CHECK(quantidade > 0),
                   preco_unitario REAL NOT NULL CHECK(preco_unitario >= 0),     -- preco do produto no momento da compra
                   desconto_unitario REAL DEFAULT 0 CHECK(desconto_unitario >= 0 AND desconto_unitario <= preco_unitario),       -- desconto aplicado aquele produto especifico naquele pedido especifico
                   FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT,
                   FOREIGN KEY (pedido_id) REFERENCES pedidos(id) ON DELETE CASCADE,
                   UNIQUE (produto_id, pedido_id)       -- para um mesmo pedido, so pode haver um item-pedido de cada produto
    )
    """)
    
    #criar tabela lotes
    #todas as datas em formato iso: 'YYYY-MM-DD'
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS lotes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   produto_id INTEGER NOT NULL,     -- o estoque pode ter varios lotes do mesmo produto
                   numero_lote TEXT NOT NULL,       -- pode ser o mesmo para lotes de produtos diferentes
                   data_fabricacao TEXT NOT NULL,
                   data_vencimento TEXT,        -- produtos nao-pereciveis podem nao ter data de validade (ex: roupas), nesse caso recebem data_vencimento = NULL
                   quantidade INTEGER NOT NULL CHECK(quantidade >= 0),
                   FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE RESTRICT,
                   UNIQUE (produto_id, numero_lote)     -- para lotes do mesmo produto, os numero_lote devem ser sempre diferentes
    )
    """)

    #criar tabela item_pedido_lotes
    #tabela de conexao entre itens_pedido e lotes
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS item_pedido_lotes(
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   lote_id INTEGER NOT NULL,
                   item_pedido_id INTEGER NOT NULL,
                   quantidade INTEGER NOT NULL CHECK(quantidade >= 0),     -- quantidade de itens daquele lote especifico no item_pedido
                   FOREIGN KEY (lote_id) REFERENCES lotes(id) ON DELETE RESTRICT,
                   FOREIGN KEY (item_pedido_id) REFERENCES itens_pedido(id) ON DELETE CASCADE,
                   UNIQUE (lote_id, item_pedido_id)     -- para um mesmo item_pedido, os lotes devem ser sempre diferentes, ou seja, exemplares do mesmo lote sempre vao para o mesmo item_pedido_lote quando colocados no mesmo pedido
    )
    """)

    conexao.commit()


def close_connection():
    conexao = get_conexao()
    conexao.close()

