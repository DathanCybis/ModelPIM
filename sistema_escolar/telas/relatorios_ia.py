# telas/relatorios_ia.py
import customtkinter as ctk
from tkinter import messagebox
from banco import *
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from ia import classificar_dificuldade, recomendar_data_entrega, analisar_texto_aluno, responder_pergunta

def criar_tela_relatorios_ia(frame):
    # ========================= FUNÇÕES INTERNAS ================================

    def gerar_relatorio_pdf():
        dados = listar_aulas()
        if not dados:
            messagebox.showinfo("Relatório", "Não há dados de aulas para gerar relatório.")
            return

        buffer = io.BytesIO()
        c = canvas.Canvas(buffer, pagesize=A4)
        c.setFont("Helvetica-Bold", 16)
        c.drawString(200, 800, "RELATÓRIO DE AULAS")
        c.setFont("Helvetica", 12)
        y = 770

        for aula in dados:
            texto = f"{aula[1]} - {aula[2]} - {aula[3]} - {aula[4]} - {aula[5]}"
            c.drawString(50, y, texto)
            y -= 18
            if y < 50:
                c.showPage()
                y = 770

        c.save()
        with open("relatorio_aulas.pdf", "wb") as f:
            f.write(buffer.getvalue())
        buffer.close()
        messagebox.showinfo("Relatório", "Relatório PDF gerado com sucesso!")

    def carregar_estatisticas():
        total_aulas = len(listar_aulas())
        total_professores = len(buscar_nome_professores())
        total_turmas = len(buscar_nome_turmas())
        label_estatisticas.configure(
            text=f"📊 Estatísticas:\n"
                 f"Total de Aulas: {total_aulas}\n"
                 f"Total de Professores: {total_professores}\n"
                 f"Total de Turmas: {total_turmas}"
        )

    # ---------------- FUNÇÃO PARA LIMPAR CAMPOS ----------------
    def limpar_campos_ia():
        entry_titulo.delete(0, "end")
        entry_texto.delete(0, "end")
        entry_pergunta.delete(0, "end")
        text_resposta.configure(state="normal")
        text_resposta.delete("1.0", "end")
        text_resposta.configure(state="disabled")

    def responder_ia():
        pergunta = entry_pergunta.get().strip()
        if not pergunta:
            messagebox.showwarning("Aviso", "Digite uma pergunta antes de enviar!")
            return
        resposta = responder_pergunta(pergunta)
        text_resposta.configure(state="normal")
        text_resposta.delete("1.0", "end")
        text_resposta.insert("end", resposta)
        text_resposta.configure(state="disabled")

    # ========================== INTERFACE RELATÓRIOS ============================
    ctk.CTkButton(frame, text="📄 GERAR RELATÓRIO PDF", fg_color="#1f5aa6", text_color="white",
                  width=360, command=gerar_relatorio_pdf).pack(pady=(10, 6))
    ctk.CTkButton(frame, text="📊 ATUALIZAR ESTATÍSTICAS", fg_color="#1f5aa6", text_color="white",
                  width=360, command=carregar_estatisticas).pack(pady=(0, 10))

    label_estatisticas = ctk.CTkLabel(frame, text="📊 Estatísticas:\nCarregue para ver os dados.",
                                      justify="left", anchor="w")
    label_estatisticas.pack(pady=(0, 10))

    # ========================== SEÇÃO DE IA =====================================
    ctk.CTkLabel(frame, text="🧠 Assistente Inteligente", font=("Helvetica", 16, "bold")).pack(pady=(8, 10))

    # --- Classificar Atividade ---
    entry_titulo = ctk.CTkEntry(frame, placeholder_text="Título da atividade...(prova, trabalho, tarefa)", width=360)
    entry_titulo.pack(pady=(0, 6))
    ctk.CTkButton(frame, text="Classificar Dificuldade", fg_color="#4a7ac9", text_color="white", width=360,
                  command=lambda: messagebox.showinfo(
                      "Classificação de Atividade",
                      f"Dificuldade: {classificar_dificuldade(entry_titulo.get())}"
                  )).pack(pady=(0, 8))

    # --- Recomendação de Data ---
    ctk.CTkButton(frame, text="📅 Recomendar Data de Entrega", fg_color="#4a7ac9", text_color="white", width=360,
                  command=lambda: messagebox.showinfo(
                      "Recomendação de Data",
                      f"Próxima data útil sugerida: {recomendar_data_entrega()}"
                  )).pack(pady=(0, 8))

    # --- Análise de Texto do Aluno ---
    entry_texto = ctk.CTkEntry(frame, placeholder_text="Texto do aluno...(gostei, fácil, difícil)", width=360)
    entry_texto.pack(pady=(0, 6))
    ctk.CTkButton(frame, text="Analisar Texto do Aluno", fg_color="#4a7ac9", text_color="white", width=360,
                  command=lambda: messagebox.showinfo(
                      "Análise de Texto",
                      analisar_texto_aluno(entry_texto.get())
                  )).pack(pady=(0, 8))

    # --- Perguntas Gerais ---
    ctk.CTkLabel(frame, text="💬 Pergunte à IA sobre o sistema:").pack(pady=(10, 4))
    entry_pergunta = ctk.CTkEntry(frame, placeholder_text="Ex: Quantas aulas existem cadastradas? (relatório, data)", width=360)
    entry_pergunta.pack(pady=(0, 6))

    text_resposta = ctk.CTkTextbox(frame, width=360, height=120, state="disabled")
    text_resposta.pack(pady=(0, 10))

    ctk.CTkButton(frame, text="Perguntar à IA", fg_color="#4a7ac9", text_color="white", width=360,
                  command=responder_ia).pack(pady=(0, 10))

    # --- Botão Limpar Campos ---
    ctk.CTkButton(frame, text="Limpar Campos", fg_color="#7a7a7a", text_color="white", width=360,
                  command=limpar_campos_ia).pack(pady=(0, 10))

    # Atualiza estatísticas automaticamente ao abrir a aba
    frame.bind("<Visibility>", lambda e: carregar_estatisticas() if e.widget == frame else None)
