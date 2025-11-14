import sqlite3
DB = "sistema_escolar.db"

# ---------- ALUNOS ----------
def conectar_banco_alunos():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            datanasc TEXT NOT NULL,
            turma TEXT NOT NULL
        )
    """)
    conn.commit(); conn.close()

def cadastrar_alunos(nome, datanasc, turma):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO alunos (nome, datanasc, turma) VALUES (?, ?, ?)", (nome, datanasc, turma))
    conn.commit(); conn.close()

def listar_alunos():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT id, nome, datanasc, turma FROM alunos ORDER BY id"); rows = cur.fetchall(); conn.close(); return rows

def atualizar_alunos(id_, nome, datanasc, turma):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("UPDATE alunos SET nome=?, datanasc=?, turma=? WHERE id=?", (nome, datanasc, turma, id_))
    conn.commit(); conn.close()

def excluir_alunos(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("DELETE FROM alunos WHERE id=?", (id_,)); conn.commit(); conn.close()

def buscar_alunos(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT nome, datanasc, turma FROM alunos WHERE id=?", (id_,)); aluno = cur.fetchone(); conn.close(); return aluno

# ---------- TURMAS ----------
def conectar_banco_turmas():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS turmas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT NOT NULL,
            professor TEXT NOT NULL,
            turno TEXT NOT NULL,
            capacidade INTEGER,
            sala TEXT
        )
    """)
    conn.commit(); conn.close()

def cadastrar_turmas(turma, professor, turno, capacidade=None, sala=None):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO turmas (turma, professor, turno, capacidade, sala) VALUES (?, ?, ?, ?, ?)", (turma, professor, turno, capacidade, sala))
    conn.commit(); conn.close()

def listar_turmas():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT id, turma, professor, turno, capacidade, sala FROM turmas ORDER BY id"); rows = cur.fetchall(); conn.close(); return rows

def buscar_nome_turmas():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT turma FROM turmas ORDER BY turma"); turms = [t[0] for t in cur.fetchall()]; conn.close(); return turms if turms else ["Nenhuma cadastrada"]

def atualizar_turmas(id_, turma, professor, turno, capacidade, sala):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("UPDATE turmas SET turma=?, professor=?, turno=?, capacidade=?, sala=? WHERE id=?", (turma, professor, turno, capacidade, sala, id_))
    conn.commit(); conn.close()

def excluir_turmas(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("DELETE FROM turmas WHERE id=?", (id_,)); conn.commit(); conn.close()

def buscar_turmas(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT turma, professor, turno, capacidade, sala FROM turmas WHERE id=?", (id_,)); row = cur.fetchone(); conn.close(); return row

# ---------- PROFESSORES ----------
def conectar_banco_professores():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS professores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            data_nasc TEXT NOT NULL,
            especialidade TEXT NOT NULL,
            telefone TEXT,
            email TEXT
        )
    """)
    conn.commit(); conn.close()

def cadastrar_professor(nome, data_nasc, especialidade, telefone=None, email=None):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO professores (nome, data_nasc, especialidade, telefone, email) VALUES (?, ?, ?, ?, ?)", (nome, data_nasc, especialidade, telefone, email))
    conn.commit(); conn.close()

def listar_professores():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT id, nome, data_nasc, especialidade, telefone, email FROM professores ORDER BY id"); rows = cur.fetchall(); conn.close(); return rows

def buscar_nome_professores():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT nome FROM professores ORDER BY nome"); profs = [p[0] for p in cur.fetchall()]; conn.close(); return profs if profs else ["Nenhum cadastrado"]

def buscar_professor(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT nome, data_nasc, especialidade, telefone, email FROM professores WHERE id = ?", (id_,)); row = cur.fetchone(); conn.close(); return row

def atualizar_professor(id_, nome, data_nasc, especialidade, telefone, email):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("UPDATE professores SET nome = ?, data_nasc = ?, especialidade = ?, telefone = ?, email = ? WHERE id = ?", (nome, data_nasc, especialidade, telefone, email, id_))
    conn.commit(); conn.close()

def excluir_professor(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("DELETE FROM professores WHERE id = ?", (id_,)); conn.commit(); conn.close()

# ---------- AULAS ----------
def conectar_banco_aulas():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS aulas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            disciplina TEXT NOT NULL,
            professor TEXT NOT NULL,
            turma TEXT NOT NULL,
            horario TEXT NOT NULL,
            sala TEXT
        )
    """)
    conn.commit(); conn.close()

def cadastrar_aula(disciplina, professor, turma, horario, sala):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO aulas (disciplina, professor, turma, horario, sala) VALUES (?, ?, ?, ?, ?)", (disciplina, professor, turma, horario, sala))
    conn.commit(); conn.close()

def listar_aulas():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT id, disciplina, professor, turma, horario, sala FROM aulas ORDER BY id"); rows = cur.fetchall(); conn.close(); return rows

def atualizar_aula(id_, disciplina, professor, turma, horario, sala):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("UPDATE aulas SET disciplina=?, professor=?, turma=?, horario=?, sala=? WHERE id=?", (disciplina, professor, turma, horario, sala, id_))
    conn.commit(); conn.close()

def excluir_aula(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("DELETE FROM aulas WHERE id=?", (id_,)); conn.commit(); conn.close()

# ---------- ATIVIDADES ----------
def conectar_banco_atividades():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS atividades (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            descricao TEXT,
            data_criacao TEXT NOT NULL,
            data_entrega TEXT,
            dificuldade TEXT,
            turma TEXT
        )
    """)
    conn.commit(); conn.close()

def cadastrar_atividade(titulo, descricao, data_criacao, data_entrega=None, dificuldade=None, turma=None):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO atividades (titulo, descricao, data_criacao, data_entrega, dificuldade, turma) VALUES (?, ?, ?, ?, ?, ?)",
                (titulo, descricao, data_criacao, data_entrega, dificuldade, turma))
    conn.commit(); conn.close()

def listar_atividades():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT id, titulo, descricao, data_criacao, data_entrega, dificuldade, turma FROM atividades ORDER BY id"); rows = cur.fetchall(); conn.close(); return rows

def buscar_atividade(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT titulo, descricao, data_criacao, data_entrega, dificuldade, turma FROM atividades WHERE id=?", (id_,)); row = cur.fetchone(); conn.close(); return row

def atualizar_atividade(id_, titulo, descricao, data_entrega, dificuldade, turma):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("UPDATE atividades SET titulo=?, descricao=?, data_entrega=?, dificuldade=?, turma=? WHERE id=?",
                (titulo, descricao, data_entrega, dificuldade, turma, id_))
    conn.commit(); conn.close()

def excluir_atividade(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("DELETE FROM atividades WHERE id=?", (id_,)); conn.commit(); conn.close()

# ---------- DIÁRIO ELETRÔNICO ----------
def conectar_banco_diario():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT NOT NULL,
            data TEXT NOT NULL,
            conteudo TEXT
        )
    """)
    conn.commit(); conn.close()

def cadastrar_diario(turma, data, conteudo):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("INSERT INTO diario (turma, data, conteudo) VALUES (?, ?, ?)", (turma, data, conteudo))
    conn.commit(); conn.close()

def listar_diario():
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT id, turma, data, conteudo FROM diario ORDER BY data DESC"); rows = cur.fetchall(); conn.close(); return rows

def buscar_diario(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("SELECT turma, data, conteudo FROM diario WHERE id=?", (id_,)); row = cur.fetchone(); conn.close(); return row

def excluir_diario(id_):
    conn = sqlite3.connect(DB); cur = conn.cursor()
    cur.execute("DELETE FROM diario WHERE id=?", (id_,)); conn.commit(); conn.close()


def conectar_bancos():
    conectar_banco_alunos()
    conectar_banco_turmas()
    conectar_banco_professores()
    conectar_banco_aulas()
    conectar_banco_atividades()
    conectar_banco_diario()

    