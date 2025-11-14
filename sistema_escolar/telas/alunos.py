import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import listar_alunos, cadastrar_alunos, atualizar_alunos, buscar_alunos, excluir_alunos, buscar_nome_turmas
from funcao import calcular_idade, verificar_idade

def criar_tela_alunos(frame):
    def carregar_dados_alunos():
        for item in tree.get_children():
            tree.delete(item)
        for aluno in listar_alunos():
            id_, nome, data_nasc, turma = aluno
            try:
                idade = calcular_idade(data_nasc)
            except Exception:
                idade = "-"
            tree.insert("", "end", values=(id_, nome, idade, turma))

    def inserir_dados():
        nome = entry_nome_alunos.get().strip()
        datanasc = entry_datnasc_alunos.get().strip()
        turma = menu_turma.get()

        try:
            verificar_idade(datanasc)
        except Exception:
            messagebox.showwarning("Atenção", "Data inválida! Use DD/MM/AAAA")
            return

        if not turma or not nome:
            messagebox.showwarning("Atenção", "Preencha corretamente os campos.")
            return

        cadastrar_alunos(nome, datanasc, turma)
        carregar_dados_alunos()
        limpar_dados()
        messagebox.showinfo("Sucesso", f"{nome} foi cadastrado!")

    def editar_dados():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma pessoa para editar.")
            return

        id_ = tree.item(selecionado[0], "values")[0]
        nome = entry_nome_alunos.get().strip()
        datanasc = entry_datnasc_alunos.get().strip()
        turma = menu_turma.get()

        try:
            verificar_idade(datanasc)
        except:
            messagebox.showwarning("Atenção", "Data inválida! Use DD/MM/AAAA")
            return

        if not nome or not turma:
            messagebox.showwarning("Atenção", "Preencha corretamente os campos.")
            return

        atualizar_alunos(id_, nome, datanasc, turma)
        carregar_dados_alunos()
        limpar_dados()
        messagebox.showinfo("Sucesso", f"Dados de {nome} foram atualizados!")

    def excluir_dados():
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma pessoa para excluir.")
            return

        id_, nome = tree.item(selecionado[0], "values")[0:2]

        if messagebox.askyesno("Confirmação", f"Excluir {nome}?"):
            excluir_alunos(id_)
            carregar_dados_alunos()
            limpar_dados()
            messagebox.showinfo("Removido", f"{nome} foi excluído.")

    def limpar_dados():
        entry_nome_alunos.delete(0, "end")
        entry_datnasc_alunos.delete(0, "end")
        menu_turma.set("Selecione uma turma")
        tree.selection_remove(tree.selection())

    def ao_selecionar(event):
        selecionado = tree.selection()
        if selecionado:
            valores = tree.item(selecionado[0], "values")
            id_ = valores[0]
            aluno = buscar_alunos(id_)

            entry_nome_alunos.delete(0, "end")
            entry_datnasc_alunos.delete(0, "end")

            if aluno:
                entry_nome_alunos.insert(0, aluno[0])
                entry_datnasc_alunos.insert(0, aluno[1])
                menu_turma.set(aluno[2])

    entry_nome_alunos = ctk.CTkEntry(frame, placeholder_text='* Nome completo...', width=360)
    entry_nome_alunos.pack(pady=(8,6))

    entry_datnasc_alunos = ctk.CTkEntry(frame, placeholder_text='* Data de Nascimento (DD/MM/AAAA)...', width=360)
    entry_datnasc_alunos.pack(pady=(0,8))

    menu_turma = ctk.CTkOptionMenu(frame, values=buscar_nome_turmas(), width=360)
    menu_turma.pack(pady=(0,8))
    menu_turma.set("Selecione uma turma")

    frame.bind("<Visibility>", lambda e: menu_turma.configure(values=buscar_nome_turmas()))

    ctk.CTkButton(frame, text='CADASTRAR ALUNOS', fg_color="#1f5aa6", text_color="white", width=360, command=inserir_dados).pack(pady=(0,6))
    ctk.CTkButton(frame, text='EDITAR ALUNOS', fg_color="#1f5aa6", text_color="white", width=360, command=editar_dados).pack(pady=(0,6))
    ctk.CTkButton(frame, text='EXCLUIR ALUNOS', fg_color="#c94a4a", text_color="white", width=360, command=excluir_dados).pack(pady=(0,6))
    ctk.CTkButton(frame, text='LIMPAR CAMPOS', fg_color="#7a7a7a", text_color="white", width=360, command=limpar_dados).pack()

    style = ttk.Style(frame)
    style.theme_use("clam")
    style.configure("Treeview", background="white", foreground="#183b7a", fieldbackground="white", rowheight=26, font=("Arial", 12))

    frame_tree = ctk.CTkFrame(frame, corner_radius=8)
    frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)

    tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "Idade", "Turma"), show="headings")
    for col, w in [("ID",60),("Nome",420),("Idade",100),("Turma",140)]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both", padx=6, pady=6)
    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    carregar_dados_alunos()
