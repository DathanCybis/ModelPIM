import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import (
    listar_alunos, cadastrar_alunos, atualizar_alunos,
    buscar_alunos, excluir_alunos, buscar_nome_turmas
)
from funcao import calcular_idade, verificar_idade


def criar_tela_alunos(frame):
    """
    Monta a interface gráfica da tela de alunos dentro do frame recebido.
    Configura inputs, botões e tabela (Treeview), e faz integração com o banco.
    """

    # ---------------------------
    # Função: Carregar registros na Tabela
    # ---------------------------
    def carregar_dados_alunos():
        """Limpa e recarrega os dados dos alunos no Treeview."""
        for item in tree.get_children():
            tree.delete(item)

        for aluno in listar_alunos():
            id_, nome, data_nasc, turma = aluno

            # Calcula idade com segurança
            try:
                idade = calcular_idade(data_nasc)
            except Exception:
                idade = "-"

            tree.insert("", "end", values=(id_, nome, idade, turma))

    # ---------------------------
    # Função: Inserir novo aluno
    # ---------------------------
    def inserir_dados():
        nome = entry_nome_alunos.get().strip()
        datanasc = entry_datnasc_alunos.get().strip()
        turma = menu_turma.get()

        # Valida data de nascimento
        try:
            verificar_idade(datanasc)
        except Exception:
            messagebox.showwarning("Atenção", "Data inválida! Use DD/MM/AAAA")
            return

        # Verifica campos
        if not turma or not nome:
            messagebox.showwarning("Atenção", "Preencha corretamente os campos.")
            return

        # Salva no banco
        cadastrar_alunos(nome, datanasc, turma)

        # Atualiza interface
        carregar_dados_alunos()
        limpar_dados()

        messagebox.showinfo("Sucesso", f"{nome} foi cadastrado!")

    # ---------------------------
    # Função: Editar aluno selecionado
    # ---------------------------
    def editar_dados():
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma pessoa para editar.")
            return

        id_ = tree.item(selecionado[0], "values")[0]
        nome = entry_nome_alunos.get().strip()
        datanasc = entry_datnasc_alunos.get().strip()
        turma = menu_turma.get()

        # Valida data
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

    # ---------------------------
    # Função: Excluir aluno selecionado
    # ---------------------------
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

    # ---------------------------
    # Função: Limpar campos de entrada
    # ---------------------------
    def limpar_dados():
        entry_nome_alunos.delete(0, "end")
        entry_datnasc_alunos.delete(0, "end")
        menu_turma.set("Selecione uma turma")

        # Remove seleção da linha
        tree.selection_remove(tree.selection())

    # ---------------------------
    # Ao clicar em um item da tabela, preencher os campos
    # ---------------------------
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

    # ---------------------------------------
    # Campos de entrada
    # ---------------------------------------
    entry_nome_alunos = ctk.CTkEntry(frame, placeholder_text='* Nome completo...', width=360)
    entry_nome_alunos.pack(pady=(8,6))

    entry_datnasc_alunos = ctk.CTkEntry(frame, placeholder_text='* Data de Nascimento (DD/MM/AAAA)...', width=360)
    entry_datnasc_alunos.pack(pady=(0,8))

    menu_turma = ctk.CTkOptionMenu(frame, values=buscar_nome_turmas(), width=360)
    menu_turma.pack(pady=(0,8))
    menu_turma.set("Selecione uma turma")

    # Atualiza automaticamente o dropdown quando a aba é aberta
    frame.bind("<Visibility>", lambda e: menu_turma.configure(values=buscar_nome_turmas()))

    # ---------------------------------------
    # Botões de Ação
    # ---------------------------------------
    ctk.CTkButton(frame, text='CADASTRAR ALUNOS', fg_color="#1f5aa6", text_color="white",
                  width=360, command=inserir_dados).pack(pady=(0,6))

    ctk.CTkButton(frame, text='EDITAR ALUNOS', fg_color="#1f5aa6", text_color="white",
                  width=360, command=editar_dados).pack(pady=(0,6))

    ctk.CTkButton(frame, text='EXCLUIR ALUNOS', fg_color="#c94a4a", text_color="white",
                  width=360, command=excluir_dados).pack(pady=(0,6))

    ctk.CTkButton(frame, text='LIMPAR CAMPOS', fg_color="#7a7a7a", text_color="white",
                  width=360, command=limpar_dados).pack()

    # ---------------------------------------
    # Estilo da Tabela
    # ---------------------------------------
    style = ttk.Style(frame)
    style.theme_use("clam")
    style.configure(
        "Treeview",
        background="white",
        foreground="#183b7a",
        fieldbackground="white",
        rowheight=26,
        font=("Arial", 12)
    )

    # ---------------------------------------
    # Frame do Treeview
    # ---------------------------------------
    frame_tree = ctk.CTkFrame(frame, corner_radius=8)
    frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)

    # Tabela principal
    tree = ttk.Treeview(frame_tree, columns=("ID", "Nome", "Idade", "Turma"), show="headings")

    # Configuração das colunas
    for col, w in [("ID",60),("Nome",420),("Idade",100),("Turma",140)]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    # Scrollbar vertical
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both", padx=6, pady=6)
    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    # Carrega dados iniciais
    carregar_dados_alunos()
