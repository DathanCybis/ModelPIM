import customtkinter as ctk
from datetime import datetime

def criar_tela_dashboard(frame, controller=None):
    """
    Tela inicial do sistema com visão geral e status dos módulos.
    Adaptada para o padrão visual do projeto (CustomTkinter).
    """

    # =========================== CABEÇALHO ======================================
    titulo = ctk.CTkLabel(frame, text="🏠 Dashboard Principal", 
                          font=("Helvetica", 20, "bold"))
    titulo.pack(pady=(10, 5))

    subtitulo = ctk.CTkLabel(frame, 
        text="Visão Geral do Sistema de Gestão Educacional",
        font=("Helvetica", 14))
    subtitulo.pack(pady=(0, 10))

    # =========================== MENSAGEM DE SUSTENTABILIDADE ===================
    sustentabilidade = ctk.CTkLabel(
        frame,
        text=(
            "🌳 SUSTENTABILIDADE: Use relatórios digitais!\n"
            "A cada relatório gerado, simulamos a economia de 10 folhas de papel."
        ),
        font=("Helvetica", 11, "italic"),
        text_color="#2fa572",
        justify="center",
        wraplength=500
    )
    sustentabilidade.pack(pady=(10, 20))

    # =========================== STATUS DOS MÓDULOS =============================
    ctk.CTkLabel(frame, text="📦 Status dos Módulos:", 
                 font=("Helvetica", 13, "bold")).pack(pady=(0, 10))

    status = {
        "Alunos & Turmas": "✅ Ativo",
        "Aulas": "✅ Ativo",
        "Relatórios Digitais (CSV)": "✅ Ativo",
        "IA - Classificador & Relatórios": "✅ Ativo",
        "Interface CustomTkinter": "✅ Ativo"
    }

    container_status = ctk.CTkFrame(frame, fg_color="transparent")
    container_status.pack(pady=(0, 20))

    for modulo, st in status.items():
        linha = ctk.CTkLabel(
            container_status,
            text=f"• {modulo}: {st}",
            font=("Helvetica", 12),
            anchor="w",
            justify="left"
        )
        linha.pack(anchor="w", padx=30, pady=2)

    # =========================== INFORMAÇÕES DO SISTEMA =========================
    separador = ctk.CTkLabel(frame, text="───────────────────────────────", 
                             text_color="gray")
    separador.pack(pady=(10, 5))

    data_atual = datetime.now().strftime("%d/%m/%Y - %H:%M")
    info_label = ctk.CTkLabel(
        frame,
        text=f"🕓 Última atualização: {data_atual}\n👨‍💻 Sistema desenvolvido com integração de IA e relatórios inteligentes.",
        font=("Helvetica", 10),
        justify="center",
        text_color="gray"
    )
    info_label.pack(pady=(5, 15))

    # =========================== BOTÃO DE ATUALIZAÇÃO ===========================
    def atualizar_dashboard():
        novo_horario = datetime.now().strftime("%d/%m/%Y - %H:%M")
        info_label.configure(
            text=f"🕓 Última atualização: {novo_horario}\n👨‍💻 Sistema desenvolvido com integração de IA e relatórios inteligentes."
        )

    ctk.CTkButton(
        frame, text="🔄 Atualizar Informações", width=220,
        fg_color="#1f5aa6", text_color="white", command=atualizar_dashboard
    ).pack(pady=(0, 10))
