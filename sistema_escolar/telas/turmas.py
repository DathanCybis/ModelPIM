# telas/turmas.py
import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import *

def criar_tela_turmas(frame):
    def carregar_dados_turmas():
        for item in tree.get_children(): tree.delete(item)
        for t in listar_turmas():
            id_, turma, professor, turno, capacidade, sala = t
            tree.insert("", "end", values=(id_, turma, professor, turno, capacidade, sala))

    def inserir_dados_turmas():
        turma = entry_turma.get().strip(); professor = menu_professor.get(); turno = entry_turno.get().strip()
        capacidade = entry_capacidade.get().strip(); sala = entry_sala.get().strip()
        if not turma or not turno: messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (*)."); return
        if professor == "Selecione um professor": messagebox.showwarning("Atenção", "Selecione um professor válido."); return
        if capacidade and not capacidade.isdigit(): messagebox.showwarning("Atenção", "A capacidade deve ser um número."); return
        cadastrar_turmas(turma, professor, turno, capacidade, sala); carregar_dados_turmas(); limpar_dados_turmas(); messagebox.showinfo("Sucesso", f"A turma '{turma}' foi cadastrada com sucesso!")

    def editar_dados_turmas():
        selecionado = tree.selection()
        if not selecionado: messagebox.showwarning("Aviso", "Selecione uma turma para editar."); return
        id_ = tree.item(selecionado[0], "values")[0]; turma = entry_turma.get().strip(); professor = menu_professor.get(); turno = entry_turno.get().strip()
        capacidade = entry_capacidade.get().strip(); sala = entry_sala.get().strip()
        if not turma or not turno: messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (*)."); return
        if professor == "Selecione um professor": messagebox.showwarning("Atenção", "Selecione um professor válido."); return
        if capacidade and not capacidade.isdigit(): messagebox.showwarning("Atenção", "A capacidade deve ser um número."); return
        atualizar_turmas(id_, turma, professor, turno, capacidade, sala); carregar_dados_turmas(); limpar_dados_turmas(); messagebox.showinfo("Sucesso", f"Dados da turma '{turma}' foram atualizados!")

    def excluir_dados_turmas():
        selecionado = tree.selection()
        if not selecionado: messagebox.showwarning("Aviso", "Selecione uma turma para excluir."); return
        id_, turma = tree.item(selecionado[0], "values")[0:2]
        if messagebox.askyesno("Confirmação", f"Tem certeza que deseja excluir a turma '{turma}'?"): excluir_turmas(id_); carregar_dados_turmas(); limpar_dados_turmas(); messagebox.showinfo("Removido", f"A turma '{turma}' foi excluída com sucesso.")

    def limpar_dados_turmas():
        entry_turma.delete(0, "end"); menu_professor.set("Selecione um professor"); entry_turno.delete(0, "end"); entry_capacidade.delete(0, "end"); entry_sala.delete(0, "end"); tree.selection_remove(tree.selection()); atualizar_menu_professores()

    def ao_selecionar_turmas(event):
        selecionado = tree.selection()
        if selecionado:
            valores = tree.item(selecionado[0], "values"); id_ = valores[0]; turma = buscar_turmas(id_)
            if turma:
                entry_turma.delete(0, "end"); entry_turno.delete(0, "end"); entry_capacidade.delete(0, "end"); entry_sala.delete(0, "end")
                entry_turma.insert(0, turma[0]); menu_professor.set(turma[1]); entry_turno.insert(0, turma[2]); entry_capacidade.insert(0, turma[3]); entry_sala.insert(0, turma[4])

    def atualizar_menu_professores(event=None):
        professores = buscar_nome_professores(); menu_professor.configure(values=professores)
        if professores: menu_professor.set("Selecione um professor")

    entry_turma = ctk.CTkEntry(frame, placeholder_text='* Turma...', width=360); entry_turma.pack(pady=(8,6))
    entry_turno = ctk.CTkEntry(frame, placeholder_text='* Turno...', width=360); entry_turno.pack(pady=(0,8))
    entry_capacidade = ctk.CTkEntry(frame, placeholder_text='Capacidade...', width=360); entry_capacidade.pack(pady=(0,8))
    entry_sala = ctk.CTkEntry(frame, placeholder_text='Sala...', width=360); entry_sala.pack(pady=(0,8))
    menu_professor = ctk.CTkOptionMenu(frame, values=buscar_nome_professores(), width=360); menu_professor.pack(pady=(0,8)); menu_professor.set("Selecione um professor")
    frame.bind("<Visibility>", atualizar_menu_professores)

    ctk.CTkButton(frame, text='CADASTRAR TURMA', fg_color="#1f5aa6", text_color="white", width=360, command=inserir_dados_turmas).pack(pady=(0,6))
    ctk.CTkButton(frame, text='EDITAR TURMA', fg_color="#1f5aa6", text_color="white", width=360, command=editar_dados_turmas).pack(pady=(0,6))
    ctk.CTkButton(frame, text='EXCLUIR TURMA', fg_color="#c94a4a", text_color="white", width=360, command=excluir_dados_turmas).pack(pady=(0,6))
    ctk.CTkButton(frame, text='LIMPAR CAMPOS', fg_color="#7a7a7a", text_color="white", width=360, command=limpar_dados_turmas).pack()

    style = ttk.Style(frame); style.theme_use("clam"); style.configure("Treeview", background="white", foreground="#183b7a", fieldbackground="white", rowheight=26, font=("Arial", 12))
    frame_tree = ctk.CTkFrame(frame, corner_radius=8); frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)
    tree = ttk.Treeview(frame_tree, columns=("ID", "Turma", "Professor", "Turno", "Capacidade", "Sala"), show="headings")
    for col,w in [("ID",60),("Turma",220),("Professor",360),("Turno",120),("Capacidade",100),("Sala",120)]: tree.heading(col, text=col); tree.column(col, width=w, anchor="center")
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview); tree.configure(yscrollcommand=scroll.set); scroll.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both", padx=6, pady=6); tree.bind("<<TreeviewSelect>>", ao_selecionar_turmas)
    carregar_dados_turmas()
