import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import buscar_turmas, listar_turmas, excluir_turmas, atualizar_turmas, cadastrar_turmas, buscar_nome_professores


def criar_tela_turmas(frame):
    """
    Monta a interface gráfica para gestão de turmas.
    Inclui funcionalidades de cadastro, edição, exclusão e listagem.
    """

    # ========================= CARREGAR TURMAS =========================
    def carregar_dados_turmas():
        """Limpa o Treeview e recarrega todas as turmas do banco."""
        # Limpa a tabela
        for item in tree.get_children():
            tree.delete(item)

        # Adiciona novamente os registros
        for t in listar_turmas():
            id_, turma, professor, turno, capacidade, sala = t
            tree.insert(
                "",
                "end",
                values=(id_, turma, professor, turno, capacidade, sala)
            )

    # ========================= INSERIR NOVA TURMA =========================
    def inserir_dados_turmas():
        """Valida os campos e cadastra uma nova turma."""
        turma = entry_turma.get().strip()
        professor = menu_professor.get()
        turno = entry_turno.get().strip()
        capacidade = entry_capacidade.get().strip()
        sala = entry_sala.get().strip()

        # Validação dos campos obrigatórios
        if not turma or not turno:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (*).")
            return

        # Validação do professor
        if professor == "Selecione um professor":
            messagebox.showwarning("Atenção", "Selecione um professor válido.")
            return

        # Validação da capacidade numérica
        if capacidade and not capacidade.isdigit():
            messagebox.showwarning("Atenção", "A capacidade deve ser um número.")
            return

        # Inserção no banco de dados
        cadastrar_turmas(turma, professor, turno, capacidade, sala)
        carregar_dados_turmas()
        limpar_dados_turmas()

        messagebox.showinfo(
            "Sucesso",
            f"A turma '{turma}' foi cadastrada com sucesso!"
        )

    # ========================= EDITAR TURMA =========================
    def editar_dados_turmas():
        """Edita os dados da turma atualmente selecionada no Treeview."""
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma turma para editar.")
            return

        id_ = tree.item(selecionado[0], "values")[0]

        turma = entry_turma.get().strip()
        professor = menu_professor.get()
        turno = entry_turno.get().strip()
        capacidade = entry_capacidade.get().strip()
        sala = entry_sala.get().strip()

        # Validação dos campos obrigatórios
        if not turma or not turno:
            messagebox.showwarning("Atenção", "Preencha os campos obrigatórios (*).")
            return

        # Validação do professor
        if professor == "Selecione um professor":
            messagebox.showwarning("Atenção", "Selecione um professor válido.")
            return

        # Validação da capacidade numérica
        if capacidade and not capacidade.isdigit():
            messagebox.showwarning("Atenção", "A capacidade deve ser um número.")
            return

        # Atualização no banco
        atualizar_turmas(id_, turma, professor, turno, capacidade, sala)
        carregar_dados_turmas()
        limpar_dados_turmas()

        messagebox.showinfo(
            "Sucesso",
            f"Dados da turma '{turma}' foram atualizados!"
        )

    # ========================= EXCLUIR TURMA =========================
    def excluir_dados_turmas():
        """Exclui a turma selecionada, mediante confirmação do usuário."""
        selecionado = tree.selection()

        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione uma turma para excluir.")
            return

        id_, turma = tree.item(selecionado[0], "values")[0:2]

        confirmar = messagebox.askyesno(
            "Confirmação",
            f"Tem certeza que deseja excluir a turma '{turma}'?"
        )

        if confirmar:
            excluir_turmas(id_)
            carregar_dados_turmas()
            limpar_dados_turmas()

            messagebox.showinfo(
                "Removido",
                f"A turma '{turma}' foi excluída com sucesso."
            )

    # ========================= LIMPAR CAMPOS =========================
    def limpar_dados_turmas():
        """Limpa todos os campos de entrada e reseta a seleção."""
        entry_turma.delete(0, "end")
        menu_professor.set("Selecione um professor")
        entry_turno.delete(0, "end")
        entry_capacidade.delete(0, "end")
        entry_sala.delete(0, "end")

        tree.selection_remove(tree.selection())

        # Atualiza menu de professores sempre que for limpar
        atualizar_menu_professores()

    # ========================= SELECIONAR ITEM DO TREEVIEW =========================
    def ao_selecionar_turmas(event):
        """Carrega os dados da turma selecionada nos campos de edição."""
        selecionado = tree.selection()

        if selecionado:
            valores = tree.item(selecionado[0], "values")
            id_ = valores[0]

            turma = buscar_turmas(id_)

            if turma:
                # Limpa os campos antes de preencher
                entry_turma.delete(0, "end")
                entry_turno.delete(0, "end")
                entry_capacidade.delete(0, "end")
                entry_sala.delete(0, "end")

                # Insere os valores correspondentes
                entry_turma.insert(0, turma[0])
                menu_professor.set(turma[1])
                entry_turno.insert(0, turma[2])
                entry_capacidade.insert(0, turma[3])
                entry_sala.insert(0, turma[4])

    # ========================= ATUALIZAR MENU DE PROFESSORES =========================
    def atualizar_menu_professores(event=None):
        """
        Atualiza a lista de professores no OptionMenu.
        É chamado ao abrir a aba e ao limpar os campos.
        """
        professores = buscar_nome_professores()
        menu_professor.configure(values=professores)

        if professores:
            menu_professor.set("Selecione um professor")

    # ========================= CAMPOS DE ENTRADA =========================
    entry_turma = ctk.CTkEntry(frame, placeholder_text='* Turma...', width=360)
    entry_turma.pack(pady=(8, 6))

    entry_turno = ctk.CTkEntry(frame, placeholder_text='* Turno...', width=360)
    entry_turno.pack(pady=(0, 8))

    entry_capacidade = ctk.CTkEntry(frame, placeholder_text='Capacidade...', width=360)
    entry_capacidade.pack(pady=(0, 8))

    entry_sala = ctk.CTkEntry(frame, placeholder_text='Sala...', width=360)
    entry_sala.pack(pady=(0, 8))

    menu_professor = ctk.CTkOptionMenu(
        frame,
        values=buscar_nome_professores(),
        width=360
    )
    menu_professor.pack(pady=(0, 8))
    menu_professor.set("Selecione um professor")

    # Atualiza a lista sempre que a aba for exibida
    frame.bind("<Visibility>", atualizar_menu_professores)

    # ========================= BOTÕES =========================
    ctk.CTkButton(
        frame, text='CADASTRAR TURMA',
        fg_color="#1f5aa6", text_color="white",
        width=360, command=inserir_dados_turmas
    ).pack(pady=(0, 6))

    ctk.CTkButton(
        frame, text='EDITAR TURMA',
        fg_color="#1f5aa6", text_color="white",
        width=360, command=editar_dados_turmas
    ).pack(pady=(0, 6))

    ctk.CTkButton(
        frame, text='EXCLUIR TURMA',
        fg_color="#c94a4a", text_color="white",
        width=360, command=excluir_dados_turmas
    ).pack(pady=(0, 6))

    ctk.CTkButton(
        frame, text='LIMPAR CAMPOS',
        fg_color="#7a7a7a", text_color="white",
        width=360, command=limpar_dados_turmas
    ).pack()

    # ========================= TREEVIEW (TABELA) =========================
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

    frame_tree = ctk.CTkFrame(frame, corner_radius=8)
    frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)

    # Configuração do Treeview
    tree = ttk.Treeview(
        frame_tree,
        columns=("ID", "Turma", "Professor", "Turno", "Capacidade", "Sala"),
        show="headings"
    )

    colunas = [
        ("ID", 60),
        ("Turma", 220),
        ("Professor", 360),
        ("Turno", 120),
        ("Capacidade", 100),
        ("Sala", 120),
    ]

    # Cabeçalhos e largura das colunas
    for col, w in colunas:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    # Scrollbar vertical
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both", padx=6, pady=6)

    # Evento ao selecionar uma linha
    tree.bind("<<TreeviewSelect>>", ao_selecionar_turmas)

    # Carrega dados ao abrir a tela
    carregar_dados_turmas()
