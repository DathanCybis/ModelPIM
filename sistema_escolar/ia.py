from datetime import datetime, timedelta
import random

# ====================== CLASSIFICAÇÃO DE ATIVIDADE ============================
def classificar_dificuldade(titulo, descricao=None):
    """
    Classifica a dificuldade de uma atividade com base em palavras-chave encontradas
    no título e/ou descrição.

    Parâmetros:
        titulo (str): Título da atividade (ex.: "Prova de Matemática").
        descricao (str, opcional): Descrição da atividade.

    Retorno:
        str: "Alta", "Média", "Baixa" ou "Indefinida".

    Observações:
        - A função é compatível com versões antigas que passavam apenas o título.
        - A classificação é feita por simples correspondência de palavras.
    """
    # Prepara o texto analisado
    texto = (titulo or "").lower()
    if descricao:
        texto += " " + descricao.lower()

    # Identifica dificuldade por palavras-chave
    if any(p in texto for p in ["prova", "exame", "teste"]):
        return "Alta"
    elif any(p in texto for p in ["trabalho", "pesquisa", "relatório"]):
        return "Média"
    elif any(p in texto for p in ["exercício", "atividade", "tarefa"]):
        return "Baixa"
    else:
        return "Indefinida"


# ====================== RECOMENDAÇÃO DE DATA ================================
def recomendar_data_entrega(data_criacao_str=None, dificuldade=None):
    """
    Sugere a próxima data útil para entrega de uma atividade.

    Parâmetros:
        data_criacao_str (str, opcional):
            Data no formato ISO (yyyy-mm-dd) usada como referência.
            Caso não seja válida, ignora e usa a data atual.
        dificuldade (str, opcional):
            Dificuldade da atividade: "Alta", "Média" ou "Baixa".

    Retorno:
        str: Data útil recomendada no formato DD/MM/YYYY.

    Regras:
        - Alta → +2 dias
        - Média → +5 dias
        - Baixa → +8 dias
        - Indefinida → +3 dias (padrão)
        - Se cair no fim de semana, pula para o próximo dia útil
    """
    hoje = datetime.now()

    # Caso tenha sido passado um texto de data, tenta converter
    if isinstance(data_criacao_str, str):
        try:
            hoje = datetime.fromisoformat(data_criacao_str)
        except Exception:
            pass  # Se falhar, mantém a data atual

    # Define o prazo com base na dificuldade
    if dificuldade == "Alta":
        dias = 2
    elif dificuldade == "Média":
        dias = 5
    elif dificuldade == "Baixa":
        dias = 8
    else:
        dias = 3  # Padrão

    proxima = hoje + timedelta(days=dias)

    # Remove finais de semana
    while proxima.weekday() >= 5:  # 5 = sábado, 6 = domingo
        proxima += timedelta(days=1)

    return proxima.strftime("%d/%m/%Y")


# ====================== ANÁLISE DE TEXTO DE ALUNO ===========================
def analisar_texto_aluno(texto: str) -> str:
    """
    Analisa um texto curto escrito pelo aluno e tenta identificar:
    - Dificuldade
    - Sentimento positivo
    - Facilidade
    - Expressão neutra

    Parâmetros:
        texto (str): Mensagem do aluno.

    Retorno:
        str: Feedback interpretado pelo sistema.
    """
    texto = (texto or "").lower()

    # Regras simples baseadas em palavras-chave
    if "não entendi" in texto or "difícil" in texto:
        return "O aluno demonstrou dificuldade. Recomenda-se reforçar o conteúdo."
    elif "gostei" in texto or "interessante" in texto:
        return "O aluno mostrou engajamento positivo."
    elif "fácil" in texto or "tranquilo" in texto:
        return "O aluno entendeu bem o conteúdo."
    else:
        # Resposta neutra aleatória
        return random.choice([
            "O aluno apresentou compreensão parcial.",
            "Análise neutra — sem indícios claros de dificuldade.",
            "Expressão neutra, sem emoção detectada."
        ])


# ====================== RESPOSTAS GERAIS DE IA ==============================
def responder_pergunta(pergunta: str) -> str:
    """
    Responde perguntas gerais sobre o sistema, de forma simples.

    Parâmetros:
        pergunta (str): Pergunta do usuário.

    Retorno:
        str: Resposta gerada.
    """
    pergunta = (pergunta or "").lower()

    # Identifica tema da pergunta
    if "relatório" in pergunta:
        return "Você pode gerar relatórios em PDF ou CSV com as informações de alunos e aulas."
    elif "aula" in pergunta:
        return "As aulas estão cadastradas com disciplina, professor, turma, horário e sala."
    elif "data" in pergunta:
        return f"A próxima data útil recomendada é {recomendar_data_entrega()}."
    else:
        # Resposta padrão
        return "Desculpe, ainda não sei responder isso. Estou aprendendo! 🤖"
