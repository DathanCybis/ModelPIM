from datetime import datetime, timedelta
import random

# ====================== CLASSIFICAÇÃO DE ATIVIDADE ============================
def classificar_dificuldade(titulo, descricao=None):
    """
    Classifica a dificuldade de uma atividade com base em palavras-chave.
    Mantém compatibilidade com o formato antigo: (titulo, descricao).
    """
    texto = (titulo or "").lower()
    if descricao:
        texto += " " + descricao.lower()

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
    Sugere a próxima data útil para entrega.
    Mantém compatibilidade com o formato antigo.
    """
    hoje = datetime.now()

    # Caso o sistema anterior passe uma string de data
    if isinstance(data_criacao_str, str):
        try:
            hoje = datetime.fromisoformat(data_criacao_str)
        except Exception:
            pass

    # Define prazo baseado na dificuldade
    if dificuldade == "Alta":
        dias = 2
    elif dificuldade == "Média":
        dias = 5
    elif dificuldade == "Baixa":
        dias = 8
    else:
        dias = 3  # padrão

    proxima = hoje + timedelta(days=dias)
    # pula fim de semana
    while proxima.weekday() >= 5:  # 5 = sábado, 6 = domingo
        proxima += timedelta(days=1)

    return proxima.strftime("%d/%m/%Y")


# ====================== ANÁLISE DE TEXTO DE ALUNO ===========================
def analisar_texto_aluno(texto: str) -> str:
    """Analisa um texto simples e retorna um feedback."""
    texto = (texto or "").lower()
    if "não entendi" in texto or "difícil" in texto:
        return "O aluno demonstrou dificuldade. Recomenda-se reforçar o conteúdo."
    elif "gostei" in texto or "interessante" in texto:
        return "O aluno mostrou engajamento positivo."
    elif "fácil" in texto or "tranquilo" in texto:
        return "O aluno entendeu bem o conteúdo."
    else:
        return random.choice([
            "O aluno apresentou compreensão parcial.",
            "Análise neutra — sem indícios claros de dificuldade.",
            "Expressão neutra, sem emoção detectada."
        ])


# ====================== RESPOSTAS GERAIS DE IA ==============================
def responder_pergunta(pergunta: str) -> str:
    """Responde perguntas simples sobre aulas e relatórios."""
    pergunta = (pergunta or "").lower()
    if "relatório" in pergunta:
        return "Você pode gerar relatórios em PDF ou CSV com as informações de alunos e aulas."
    elif "aula" in pergunta:
        return "As aulas estão cadastradas com disciplina, professor, turma, horário e sala."
    elif "data" in pergunta:
        return f"A próxima data útil recomendada é {recomendar_data_entrega()}."
    else:
        return "Desculpe, ainda não sei responder isso. Estou aprendendo! 🤖"
