# ai_utils.py
from datetime import datetime, timedelta

KEYWORDS_ALTA = {"difícil", "complexo", "projeto", "laboratório", "avançado", "pesquisa"}
KEYWORDS_MEDIA = {"médio", "intermediário", "exercício", "tarefa"}
KEYWORDS_BAIXA = {"fácil", "leitura", "resumo", "leves"}

def normalize_text(text):
    return (text or "").lower()

def classificar_dificuldade(titulo, descricao):
    txt = normalize_text(titulo + " " + (descricao or ""))
    score = 0
    for k in KEYWORDS_ALTA:
        if k in txt:
            score += 2
    for k in KEYWORDS_MEDIA:
        if k in txt:
            score += 1
    for k in KEYWORDS_BAIXA:
        if k in txt:
            score -= 1
    if len(txt) > 500:
        score += 1
    elif len(txt) < 50:
        score -= 1
    if score >= 2:
        return "Alta"
    if score == 1:
        return "Média"
    return "Baixa"

def recomendar_data_entrega(data_criacao_str, dificuldade):
    if isinstance(data_criacao_str, str):
        try:
            dt = datetime.fromisoformat(data_criacao_str)
        except Exception:
            dt = datetime.today()
    elif isinstance(data_criacao_str, datetime):
        dt = data_criacao_str
    else:
        dt = datetime.today()
    if dificuldade == "Alta":
        dias = 2
    elif dificuldade == "Média":
        dias = 5
    else:
        dias = 8
    recomendada = dt + timedelta(days=dias)
    return recomendada.date().isoformat()
