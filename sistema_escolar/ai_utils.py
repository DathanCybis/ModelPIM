# ia.py
from datetime import datetime, timedelta
import random

def classificar_atividade(titulo: str) -> str:
    """Classifica uma atividade pelo título."""
    titulo = titulo.lower()
    if any(palavra in titulo for palavra in ["prova", "exame", "teste"]):
        return "Alta dificuldade"
    elif any(palavra in titulo for palavra in ["trabalho", "pesquisa", "relatório"]):
        return "Média dificuldade"
    elif any(palavra in titulo for palavra in ["exercício", "atividade", "tarefa"]):
        return "Baixa dificuldade"
    else:
        return "Dificuldade indefinida"

def recomendar_data_entrega() -> str:
    """Sugere a próxima data útil para entrega de uma atividade."""
    hoje = datetime.now()
    proxima = hoje + timedelta(days=1)
    while proxima.weekday() >= 5:  # 5 = sábado, 6 = domingo
        proxima += timedelta(days=1)
    return proxima.strftime("%d/%m/%Y")

def analisar_texto_aluno(texto: str) -> str:
    """Analisa um texto simples e retorna um feedback simulado."""
    texto = texto.lower()
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

def responder_pergunta(pergunta: str) -> str:
    """Responde perguntas simples sobre aulas e relatórios."""
    pergunta = pergunta.lower()
    if "relatório" in pergunta:
        return "Você pode gerar relatórios em PDF ou CSV com as informações de alunos e aulas."
    elif "aula" in pergunta:
        return "As aulas estão cadastradas com disciplina, professor, turma, horário e sala."
    elif "data" in pergunta:
        return f"A próxima data útil recomendada é {recomendar_data_entrega()}."
    else:
        return "Desculpe, ainda não sei responder isso. Estou aprendendo! 🤖"
