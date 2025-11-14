import sqlite3

# Nome do arquivo do banco de dados SQLite
DB = "sistema_escolar.db"


# ============================================================
# =====================   ALUNOS   ============================
# ============================================================

def conectar_banco_alunos():
    """
    Cria a tabela 'alunos' caso ainda não exista.
    Responsável por armazenar informações básicas dos alunos.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS alunos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            datanasc TEXT NOT NULL,
            turma TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def cadastrar_alunos(nome, datanasc, turma):
    """
    Insere um novo aluno no banco de dados.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO alunos (nome, datanasc, turma) VALUES (?, ?, ?)",
        (nome, datanasc, turma)
    )

    conn.commit()
    conn.close()


def listar_alunos():
    """
    Retorna uma lista com todos os alunos cadastrados.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT id, nome, datanasc, turma FROM alunos ORDER BY id")
    rows = cur.fetchall()

    conn.close()
    return rows


def atualizar_alunos(id_, nome, datanasc, turma):
    """
    Atualiza os dados de um aluno já existente no banco.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "UPDATE alunos SET nome=?, datanasc=?, turma=? WHERE id=?",
        (nome, datanasc, turma, id_)
    )

    conn.commit()
    conn.close()


def excluir_alunos(id_):
    """
    Remove um aluno do banco pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM alunos WHERE id=?", (id_,))

    conn.commit()
    conn.close()


def buscar_alunos(id_):
    """
    Busca um aluno específico pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT nome, datanasc, turma FROM alunos WHERE id=?", (id_,))
    aluno = cur.fetchone()

    conn.close()
    return aluno


# ============================================================
# =====================   TURMAS   ============================
# ============================================================

def conectar_banco_turmas():
    """
    Cria a tabela 'turmas' caso ainda não exista.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

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

    conn.commit()
    conn.close()


def cadastrar_turmas(turma, professor, turno, capacidade=None, sala=None):
    """
    Insere uma nova turma no banco.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO turmas (turma, professor, turno, capacidade, sala) VALUES (?, ?, ?, ?, ?)",
        (turma, professor, turno, capacidade, sala)
    )

    conn.commit()
    conn.close()


def listar_turmas():
    """
    Retorna todas as turmas cadastradas.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT id, turma, professor, turno, capacidade, sala FROM turmas ORDER BY id")
    rows = cur.fetchall()

    conn.close()
    return rows


def buscar_nome_turmas():
    """
    Retorna apenas os nomes das turmas.
    Usado para dropdowns na interface.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT turma FROM turmas ORDER BY turma")
    turmas = [t[0] for t in cur.fetchall()]

    conn.close()
    return turmas if turmas else ["Nenhuma cadastrada"]


def atualizar_turmas(id_, turma, professor, turno, capacidade, sala):
    """
    Atualiza os dados de uma turma específica.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "UPDATE turmas SET turma=?, professor=?, turno=?, capacidade=?, sala=? WHERE id=?",
        (turma, professor, turno, capacidade, sala, id_)
    )

    conn.commit()
    conn.close()


def excluir_turmas(id_):
    """
    Exclui uma turma pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM turmas WHERE id=?", (id_,))

    conn.commit()
    conn.close()


def buscar_turmas(id_):
    """
    Busca os detalhes de uma turma específica.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT turma, professor, turno, capacidade, sala FROM turmas WHERE id=?",
        (id_,)
    )
    turma = cur.fetchone()

    conn.close()
    return turma


# ============================================================
# ===================   PROFESSORES   =========================
# ============================================================

def conectar_banco_professores():
    """
    Cria a tabela 'professores' caso ainda não exista.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

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

    conn.commit()
    conn.close()


def cadastrar_professor(nome, data_nasc, especialidade, telefone=None, email=None):
    """
    Insere um novo professor no banco.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO professores (nome, data_nasc, especialidade, telefone, email) VALUES (?, ?, ?, ?, ?)",
        (nome, data_nasc, especialidade, telefone, email)
    )

    conn.commit()
    conn.close()


def listar_professores():
    """
    Retorna todos os professores cadastrados.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT id, nome, data_nasc, especialidade, telefone, email FROM professores ORDER BY id")
    rows = cur.fetchall()

    conn.close()
    return rows


def buscar_nome_professores():
    """
    Retorna apenas os nomes dos professores.
    Útil para seletores de interface.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT nome FROM professores ORDER BY nome")
    nomes = [p[0] for p in cur.fetchall()]

    conn.close()
    return nomes if nomes else ["Nenhum cadastrado"]


def buscar_professor(id_):
    """
    Retorna os dados completos de um professor pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT nome, data_nasc, especialidade, telefone, email FROM professores WHERE id=?",
        (id_,)
    )
    row = cur.fetchone()

    conn.close()
    return row


def atualizar_professor(id_, nome, data_nasc, especialidade, telefone, email):
    """
    Atualiza os dados de um professor.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE professores
        SET nome=?, data_nasc=?, especialidade=?, telefone=?, email=?
        WHERE id=?
        """,
        (nome, data_nasc, especialidade, telefone, email, id_)
    )

    conn.commit()
    conn.close()


def excluir_professor(id_):
    """
    Remove um professor do banco.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM professores WHERE id=?", (id_,))

    conn.commit()
    conn.close()


# ============================================================
# ======================   AULAS   ============================
# ============================================================

def conectar_banco_aulas():
    """
    Cria a tabela 'aulas' caso ainda não exista.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

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

    conn.commit()
    conn.close()


def cadastrar_aula(disciplina, professor, turma, horario, sala):
    """
    Insere uma nova aula no banco.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO aulas (disciplina, professor, turma, horario, sala) VALUES (?, ?, ?, ?, ?)",
        (disciplina, professor, turma, horario, sala)
    )

    conn.commit()
    conn.close()


def listar_aulas():
    """
    Lista todas as aulas cadastradas.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("SELECT id, disciplina, professor, turma, horario, sala FROM aulas ORDER BY id")
    rows = cur.fetchall()

    conn.close()
    return rows


def atualizar_aula(id_, disciplina, professor, turma, horario, sala):
    """
    Atualiza os dados de uma aula específica.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE aulas
        SET disciplina=?, professor=?, turma=?, horario=?, sala=?
        WHERE id=?
        """,
        (disciplina, professor, turma, horario, sala, id_)
    )

    conn.commit()
    conn.close()


def excluir_aula(id_):
    """
    Exclui uma aula pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM aulas WHERE id=?", (id_,))

    conn.commit()
    conn.close()


# ============================================================
# ====================   ATIVIDADES   =========================
# ============================================================

def conectar_banco_atividades():
    """
    Cria a tabela 'atividades' caso ainda não exista.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

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

    conn.commit()
    conn.close()


def cadastrar_atividade(titulo, descricao, data_criacao, data_entrega=None, dificuldade=None, turma=None):
    """
    Insere uma nova atividade no banco.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO atividades (titulo, descricao, data_criacao, data_entrega, dificuldade, turma)
        VALUES (?, ?, ?, ?, ?, ?)
        """,
        (titulo, descricao, data_criacao, data_entrega, dificuldade, turma)
    )

    conn.commit()
    conn.close()


def listar_atividades():
    """
    Lista todas as atividades cadastradas.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, titulo, descricao, data_criacao, data_entrega, dificuldade, turma
        FROM atividades
        ORDER BY id
    """)
    rows = cur.fetchall()

    conn.close()
    return rows


def buscar_atividade(id_):
    """
    Retorna os dados completos de uma atividade pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        SELECT titulo, descricao, data_criacao, data_entrega, dificuldade, turma
        FROM atividades
        WHERE id=?
        """,
        (id_,)
    )
    row = cur.fetchone()

    conn.close()
    return row


def atualizar_atividade(id_, titulo, descricao, data_entrega, dificuldade, turma):
    """
    Atualiza uma atividade já existente.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE atividades
        SET titulo=?, descricao=?, data_entrega=?, dificuldade=?, turma=?
        WHERE id=?
        """,
        (titulo, descricao, data_entrega, dificuldade, turma, id_)
    )

    conn.commit()
    conn.close()


def excluir_atividade(id_):
    """
    Exclui uma atividade pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM atividades WHERE id=?", (id_,))

    conn.commit()
    conn.close()


# ============================================================
# =================   DIÁRIO ELETRÔNICO   =====================
# ============================================================

def conectar_banco_diario():
    """
    Cria a tabela 'diario' caso ainda não exista.
    Armazena anotações de aulas e registros do professor.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS diario (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            turma TEXT NOT NULL,
            data TEXT NOT NULL,
            conteudo TEXT
        )
    """)

    conn.commit()
    conn.close()


def cadastrar_diario(turma, data, conteudo):
    """
    Insere um registro no diário eletrônico.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO diario (turma, data, conteudo) VALUES (?, ?, ?)",
        (turma, data, conteudo)
    )

    conn.commit()
    conn.close()


def listar_diario():
    """
    Lista registros do diário, ordenando da data mais recente para a mais antiga.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("""
        SELECT id, turma, data, conteudo
        FROM diario
        ORDER BY data DESC
    """)
    rows = cur.fetchall()

    conn.close()
    return rows


def buscar_diario(id_):
    """
    Busca um registro específico do diário pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute(
        "SELECT turma, data, conteudo FROM diario WHERE id=?",
        (id_,)
    )
    row = cur.fetchone()

    conn.close()
    return row


def excluir_diario(id_):
    """
    Exclui um registro do diário pelo ID.
    """
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.execute("DELETE FROM diario WHERE id=?", (id_,))

    conn.commit()
    conn.close()


# ============================================================
# ===========   FUNÇÃO PARA INICIAR TODOS OS BANCOS   =========
# ============================================================

def conectar_bancos():
    """
    Executa todas as funções de criação das tabelas.
    Garantindo que todo o banco do sistema esteja pronto.
    """
    conectar_banco_alunos()
    conectar_banco_turmas()
    conectar_banco_professores()
    conectar_banco_aulas()
    conectar_banco_atividades()
    conectar_banco_diario()
