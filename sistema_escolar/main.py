import customtkinter as ctk
from banco import conectar_bancos
from telas import alunos, professores, turmas, aulas, atividades, relatorios_ia, dashboard

# Define o tema visual geral para claro
ctk.set_appearance_mode("light")

# Tenta aplicar o tema azul padrão (caso o arquivo não exista, ignora)
try:
    ctk.set_default_color_theme("blue")
except Exception:
    pass


# ===============================
# INICIALIZAÇÃO DO SISTEMA E DA JANELA PRINCIPAL
# ===============================

# Inicializa todos os bancos de dados necessários do sistema
conectar_bancos()

# Cria a janela principal da aplicação
janela = ctk.CTk()
janela.title("Sistema Acadêmico Integrado")       # Título da janela
janela.geometry("1300x850")                       # Tamanho inicial da janela
janela.minsize(1000, 700)                         # Tamanho mínimo permitido


# ===============================
# HEADER (CABEÇALHO SUPERIOR)
# ===============================

# Cria a área do cabeçalho
header = ctk.CTkFrame(
    janela,
    height=90,
    fg_color="#f0f4fb",
    corner_radius=0
)
header.pack(side="top", fill="x")

# Ícone simples (pode ser substituído por imagem no futuro)
ctk.CTkLabel(header, text="🎓", font=("Helvetica", 28)).place(relx=0.02, rely=0.18)

# Título principal
ctk.CTkLabel(
    header,
    text="Sistema Acadêmico Integrado",
    font=("Helvetica", 20, "bold"),
    text_color="#183b7a"
).place(relx=0.08, rely=0.22)

# Subtítulo / slogan
ctk.CTkLabel(
    header,
    text="Digital • Sustentável • Integrado",
    font=("Helvetica", 10),
    text_color="#3b5f9a"
).place(relx=0.08, rely=0.62)


# ===============================
# ÁREA PRINCIPAL DO SISTEMA
# ===============================

# Frame principal que contém as abas
content = ctk.CTkFrame(janela, fg_color="#ffffff")
content.pack(expand=True, fill="both", padx=12, pady=12)

# Criando o TabView (as abas do sistema)
tabview = ctk.CTkTabview(
    content,
    width=1100,
    height=640,
    corner_radius=8
)
tabview.pack(expand=True, fill="both", padx=12, pady=12)


# ===============================
# CRIAÇÃO DAS ABAS
# Cada aba chama uma função do módulo correspondente
# ===============================

# Dashboard
tabview.add("Dashboard")
dashboard.criar_tela_dashboard(tabview.tab("Dashboard"))

# Aba de Alunos
tabview.add("Alunos")
alunos.criar_tela_alunos(tabview.tab("Alunos"))

# Aba de Professores
tabview.add("Professores")
professores.criar_tela_professores(tabview.tab("Professores"))

# Aba de Turmas
tabview.add("Turmas")
turmas.criar_tela_turmas(tabview.tab("Turmas"))

# Aba de Aulas
tabview.add("Aulas")
aulas.criar_tela_aulas(tabview.tab("Aulas"))

# Aba de Atividades
tabview.add("Atividades")
atividades.criar_tela_atividades(tabview.tab("Atividades"))

# Aba de Relatórios com IA
tabview.add("Relatórios e IA")
relatorios_ia.criar_tela_relatorios_ia(tabview.tab("Relatórios e IA"))


# ===============================
# LOOP PRINCIPAL
# Mantém a janela aberta e o sistema em execução
# ===============================
janela.mainloop()
