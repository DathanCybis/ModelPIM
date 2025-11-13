# main.py
import sys
import customtkinter as ctk
from banco import (conectar_banco_alunos, conectar_banco_turmas, conectar_banco_professores, conectar_banco_aulas, conectar_banco_atividades, conectar_banco_diario)
from telas import alunos, professores, turmas, aulas, atividades, relatorios_ia

ctk.set_appearance_mode("light") # tema claro (tradicional)
try:
    ctk.set_default_color_theme("blue") # tenta usar tema azul (se disponível)
except Exception:
    pass

def main():
    # inicializa bancos
    conectar_banco_alunos()
    conectar_banco_turmas()
    conectar_banco_professores()
    conectar_banco_aulas()
    conectar_banco_atividades()
    conectar_banco_diario()

    janela = ctk.CTk()
    janela.title("Sistema Acadêmico Integrado")
    janela.geometry("1200x800")
    janela.minsize(1000, 700)

    # Header (logo + title)
    header = ctk.CTkFrame(janela, height=90, fg_color="#f0f4fb", corner_radius=0)
    header.pack(side="top", fill="x")
    # Simples "ícone" texto - substitua por ImageLabel se tiver logo
    ctk.CTkLabel(header, text="🎓", font=("Helvetica", 28)).place(relx=0.02, rely=0.18)
    ctk.CTkLabel(header, text="Sistema Acadêmico Integrado", font=("Helvetica", 20, "bold"), text_color="#183b7a").place(relx=0.08, rely=0.22)
    ctk.CTkLabel(header, text="Digital • Sustentável • Integrado", font=("Helvetica", 10), text_color="#3b5f9a").place(relx=0.08, rely=0.62)

    # Conteúdo principal
    content = ctk.CTkFrame(janela, fg_color="#ffffff")
    content.pack(expand=True, fill="both", padx=12, pady=12)

    # Tabview central (as abas)
    tabview = ctk.CTkTabview(content, width=1100, height=640, corner_radius=8)
    tabview.pack(expand=True, fill="both", padx=12, pady=12)

    # Abas
    tabview.add("Alunos")
    alunos.criar_tela_alunos(tabview.tab("Alunos"))

    tabview.add("Professores")
    professores.criar_tela_professores(tabview.tab("Professores"))

    tabview.add("Turmas")
    turmas.criar_tela_turmas(tabview.tab("Turmas"))

    tabview.add("Aulas")
    aulas.criar_tela_aulas(tabview.tab("Aulas"))

    tabview.add("Atividades")
    atividades.criar_tela_atividades(tabview.tab("Atividades"))
    
    tabview.add("Relatórios e IA")
    relatorios_ia.criar_tela_relatorios_ia(tabview.tab("Relatórios e IA"))


    janela.mainloop()

if __name__ == "__main__":
    main()
