import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import listar_aulas, atualizar_aula, excluir_aula, cadastrar_aula, buscar_nome_turmas, buscar_nome_professores

def criar_tela_aulas(frame):
    """
    Cria a interface gráfica da aba 'Aulas' dentro do sistema acadêmico.
    Inclui cadastro, edição, exclusão e listagem de aulas.
    """

    # ------------------------------------------------------------
    # Função: carregar_dados_aulas
    # Atualiza o Treeview com os dados das aulas cadastradas
    # ------------------------------------------------------------
    def carregar_dados_aulas():
        # limpa lista
        for item in tree.get_children():
            tree.delete(item)

        # insere novamente
        for aula in listar_aulas():
            tree.insert("", "end", values=aula)

    # ------------------------------------------------------------
    # Função: inserir_aula
    # Cadastra uma nova aula no banco
    # ------------------------------------------------------------
    def inserir_aula():
        disciplina = entry_disciplina.get().strip()
        professor = menu_professor.get()
        turma = menu_turma.get()
        horario = entry_horario.get().strip()
        sala = entry_sala.get().strip()

        # valida campos obrigatórios
        if not all([disciplina, professor, turma, horario]):
            messagebox.showwarning("Aviso", "Preencha todos os campos obrigatórios!")
            return

        # insere no banco
        cadastrar_aula(disciplina, professor, turma, horario, sala)

        # atualiza interface
        carregar_dados_aulas()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Aula cadastrada com sucesso!")

    # ------------------------------------------------------------
    # Função: editar_aula
    # Edita a aula selecionada no Treeview
    # ------------------------------------------------------------
    def editar_aula():
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma aula para editar.")
            return

        # pega ID da aula
        id_ = tree.item(selecionado[0], "values")[0]

        # coleta valores editados
        disciplina = entry_disciplina.get().strip()
        professor = menu_professor.get()
        turma = menu_turma.get()
        horario = entry_horario.get().strip()
        sala = entry_sala.get().strip()

        # atualiza no banco
        atualizar_aula(id_, disciplina, professor, turma, horario, sala)

        carregar_dados_aulas()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Aula atualizada!")

    # ------------------------------------------------------------
    # Função: excluir_aula_tree
    # Exclui a aula selecionada após confirmação
    # ------------------------------------------------------------
    def excluir_aula_tree():
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma aula para excluir.")
            return

        id_, disciplina = tree.item(selecionado[0], "values")[0:2]

        # confirmação do usuário
        if messagebox.askyesno("Confirmação", f"Excluir aula de {disciplina}?"):
            excluir_aula(id_)
            carregar_dados_aulas()
            limpar_campos()
            messagebox.showinfo("Removido", f"Aula de {disciplina} excluída!")

    # ------------------------------------------------------------
    # Função: limpar_campos
    # Limpa todos os inputs e reseta seleção
    # ------------------------------------------------------------
    def limpar_campos():
        entry_disciplina.delete(0, "end")
        menu_professor.set("Selecione um professor")
        menu_turma.set("Selecione uma turma")
        entry_horario.delete(0, "end")
        entry_sala.delete(0, "end")
        tree.selection_remove(tree.selection())

    # ------------------------------------------------------------
    # Função: ao_selecionar
    # Preenche os campos com os dados da linha clicada no Treeview
    # ------------------------------------------------------------
    def ao_selecionar(event):
        selecionado = tree.selection()

        if selecionado:
            valores = tree.item(selecionado[0], "values")

            # limpa campos
            entry_disciplina.delete(0, "end")
            entry_horario.delete(0, "end")
            entry_sala.delete(0, "end")

            # preenche com os valores da aula selecionada
            entry_disciplina.insert(0, valores[1])
            menu_professor.set(valores[2])
            menu_turma.set(valores[3])
            entry_horario.insert(0, valores[4])
            entry_sala.insert(0, valores[5])

    # ------------------------------------------------------------
    # Widgets de Entrada (Inputs)
    # ------------------------------------------------------------

    entry_disciplina = ctk.CTkEntry(frame, placeholder_text="* Disciplina...", width=360)
    entry_disciplina.pack(pady=(8,6))

    entry_horario = ctk.CTkEntry(frame, placeholder_text="* Horário...", width=360)
    entry_horario.pack(pady=(0,8))

    entry_sala = ctk.CTkEntry(frame, placeholder_text="Sala...", width=360)
    entry_sala.pack(pady=(0,8))

    # Menu de professores
    menu_professor = ctk.CTkOptionMenu(frame, values=buscar_nome_professores(), width=360)
    menu_professor.pack(pady=(0,8))
    menu_professor.set("Selecione um professor")

    # Menu de turmas
    menu_turma = ctk.CTkOptionMenu(frame, values=buscar_nome_turmas(), width=360)
    menu_turma.pack(pady=(0,8))
    menu_turma.set("Selecione uma turma")

    # Atualiza listas ao entrar na aba
    frame.bind("<Visibility>", lambda e: (
        menu_professor.configure(values=buscar_nome_professores()),
        menu_turma.configure(values=buscar_nome_turmas())
    ))

    # ------------------------------------------------------------
    # Botões da tela
    # ------------------------------------------------------------

    ctk.CTkButton(frame, text="CADASTRAR AULA", fg_color="#1f5aa6", text_color="white",
                  width=360, command=inserir_aula).pack(pady=(0,6))

    ctk.CTkButton(frame, text="EDITAR AULA", fg_color="#1f5aa6", text_color="white",
                  width=360, command=editar_aula).pack(pady=(0,6))

    ctk.CTkButton(frame, text="EXCLUIR AULA", fg_color="#c94a4a", text_color="white",
                  width=360, command=excluir_aula_tree).pack(pady=(0,6))

    ctk.CTkButton(frame, text="LIMPAR CAMPOS", fg_color="#7a7a7a", text_color="white",
                  width=360, command=limpar_campos).pack()

    # ------------------------------------------------------------
    # Tabela (Treeview)
    # ------------------------------------------------------------

    frame_tree = ctk.CTkFrame(frame, corner_radius=8)
    frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)

    tree = ttk.Treeview(
        frame_tree,
        columns=("ID", "Disciplina", "Professor", "Turma", "Horário", "Sala"),
        show="headings"
    )

    # configura largura e título das colunas
    for col, w in [
        ("ID",60), ("Disciplina",300), ("Professor",360),
        ("Turma",140), ("Horário",120), ("Sala",120)
    ]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    # barra de rolagem
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both", padx=6, pady=6)

    # evento de seleção
    tree.bind("<<TreeviewSelect>>", ao_selecionar)

    # carrega dados iniciais
    carregar_dados_aulas()
