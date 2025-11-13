# telas/relatorios_ia.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import *
import io
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def criar_tela_relatorios_ia(frame):
    # ========================= FUNÇÕES INTERNAS ================================
    def gerar_relatorio_pdf():
        dados = listar_aulas()  # usa o mesmo banco de aulas
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

    def responder_ia():
        pergunta = entry_pergunta.get().strip()
        if not pergunta:
            messagebox.showwarning("Aviso", "Digite uma pergunta antes de enviar!")
            return

        resposta = processar_pergunta(pergunta)
        text_resposta.configure(state="normal")
        text_resposta.delete("1.0", "end")
        text_resposta.insert("end", resposta)
        text_resposta.configure(state="disabled")

    # Aqui seria o ponto de integração da IA (por enquanto simulado)
    def processar_pergunta(pergunta):
        pergunta = pergunta.lower()
        if "aula" in pergunta and "quantas" in pergunta:
            return f"Há um total de {len(listar_aulas())} aulas registradas no sistema."
        elif "professor" in pergunta:
            return f"O sistema possui {len(buscar_nome_professores())} professores cadastrados."
        elif "turma" in pergunta:
            return f"Existem {len(buscar_nome_turmas())} turmas registradas."
        else:
            return "Ainda não tenho dados suficientes para responder a isso, mas em breve terei! 🤖"

    # ========================== INTERFACE =====================================

    ctk.CTkButton(frame, text="📄 GERAR RELATÓRIO PDF", fg_color="#1f5aa6", text_color="white",
                  width=360, command=gerar_relatorio_pdf).pack(pady=(10, 6))
    ctk.CTkButton(frame, text="📊 ATUALIZAR ESTATÍSTICAS", fg_color="#1f5aa6", text_color="white",
                  width=360, command=carregar_estatisticas).pack(pady=(0, 10))

    label_estatisticas = ctk.CTkLabel(frame, text="📊 Estatísticas:\nCarregue para ver os dados.",
                                      justify="left", anchor="w")
    label_estatisticas.pack(pady=(0, 10))

    ctk.CTkLabel(frame, text="🤖 Pergunte à IA sobre o sistema:").pack(pady=(6, 4))
    entry_pergunta = ctk.CTkEntry(frame, placeholder_text="Ex: Quantas aulas existem cadastradas?", width=360)
    entry_pergunta.pack(pady=(0, 6))
    ctk.CTkButton(frame, text="Perguntar à IA", fg_color="#4a7ac9", text_color="white", width=360,
                  command=responder_ia).pack(pady=(0, 10))

    text_resposta = ctk.CTkTextbox(frame, width=360, height=140, state="disabled")
    text_resposta.pack(pady=(0, 10))

    # Atualiza estatísticas automaticamente ao abrir a aba
    frame.bind("<Visibility>", lambda e: carregar_estatisticas())
