from datetime import datetime, date


def calcular_idade(data_nasc_str):
    """
    Calcula a idade com base em uma data de nascimento fornecida como string.

    Parâmetros
    ----------
    data_nasc_str : str
        Data de nascimento em formato 'DD/MM/YYYY'.
        Caso esse formato falhe, tenta interpretar no formato ISO 'YYYY-MM-DD'.

    Retorno
    -------
    int
        Idade inteira calculada com base na data atual.
    """
    try:
        # Tenta converter a data no formato padrão brasileiro
        data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y").date()
    except Exception:
        # Como fallback, tenta formato ISO (YYYY-MM-DD)
        data_nasc = datetime.fromisoformat(data_nasc_str).date()

    # Obtém a data atual
    hoje = date.today()

    # Cálculo básico da idade
    idade = hoje.year - data_nasc.year

    # Ajuste caso ainda não tenha feito aniversário no ano atual
    if (hoje.month, hoje.day) < (data_nasc.month, data_nasc.day):
        idade -= 1

    return idade


def verificar_idade(data_nasc_str):
    """
    Valida a data de nascimento no formato 'DD/MM/YYYY'.

    Parâmetros
    ----------
    data_nasc_str : str
        Data de nascimento que será validada.

    Retorno
    -------
    datetime.date
        Objeto date correspondente à data válida.

    Exceções
    --------
    ValueError
        Lançada quando a data não estiver no formato esperado 'DD/MM/YYYY'.
    """
    try:
        # Tenta converter obrigatoriamente no formato solicitado
        data_nasc = datetime.strptime(data_nasc_str, "%d/%m/%Y").date()
        return data_nasc
    except ValueError:
        # Mensagem clara para o usuário/sistema
        raise ValueError("Data inválida! Use o formato DD/MM/AAAA.")
