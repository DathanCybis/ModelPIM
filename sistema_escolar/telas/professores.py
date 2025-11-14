import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import listar_professores, cadastrar_professor, atualizar_professor, excluir_professor, buscar_professor
from funcao import calcular_idade, verificar_idade


def criar_tela_professores(frame):
    """
    Cria a interface gráfica de gerenciamento de professores.
    Permite cadastrar, editar, excluir e visualizar dados.
    """

    # ========================= FUNÇÃO: Carregar Professores =========================
    def carregar_dados_professores():
        """Limpa a tabela e carrega novamente todos os professores cadastrados."""
        # Limpa tabela
        for item in tree.get_children():
            tree.delete(item)

        # Reinsere os registros
        for professor in listar_professores():
            id_, nome, data_nasc, especialidade, telefone, email = professor

            # Calcula idade (proteção caso o formato esteja incorreto)
            try:
                idade = calcular_idade(data_nasc)
            except:
                idade = "-"

            tree.insert("", "end", values=(id_, nome, idade, especialidade, telefone, email))

    # ========================= FUNÇÃO: Inserir Professor =========================
    def inserir_professor():
        """Lê os campos, valida e insere um novo professor na base de dados."""
        nome = entry_nome.get().strip()
        data_nasc = entry_data_nasc.get().strip()
        especialidade = entry_especialidade.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()

        # Valida data
        try:
            verificar_idade(data_nasc)
        except:
            messagebox.showwarning("Atenção", "Data inválida! Use DD/MM/AAAA")
            return

        # Valida campos obrigatórios
        if not nome or not data_nasc or not especialidade:
            messagebox.showwarning("Atenção", "Preencha corretamente os campos.")
            return

        # Insere no banco
        cadastrar_professor(nome, data_nasc, especialidade, telefone, email)
        carregar_dados_professores()
        limpar_campos()

        messagebox.showinfo("Sucesso", f"Professor {nome} foi cadastrado!")

    # ========================= FUNÇÃO: Editar Professor =========================
    def editar_professor():
        """Edita os dados do professor selecionado na tabela."""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um professor para editar.")
            return

        id_ = tree.item(selecionado[0], "values")[0]

        nome = entry_nome.get().strip()
        data_nasc = entry_data_nasc.get().strip()
        especialidade = entry_especialidade.get().strip()
        telefone = entry_telefone.get().strip()
        email = entry_email.get().strip()

        # Valida data
        try:
            verificar_idade(data_nasc)
        except:
            messagebox.showwarning("Atenção", "Data inválida! Use DD/MM/AAAA")
            return

        # Valida campos obrigatórios
        if not nome or not data_nasc or not especialidade:
            messagebox.showwarning("Atenção", "Preencha corretamente os campos.")
            return

        # Atualiza no banco
        atualizar_professor(id_, nome, data_nasc, especialidade, telefone, email)
        carregar_dados_professores()
        limpar_campos()

        messagebox.showinfo("Sucesso", f"Dados de {nome} foram atualizados!")

    # ========================= FUNÇÃO: Excluir Professor =========================
    def excluir_dados_professor():
        """Exclui um professor selecionado no Treeview."""
        selecionado = tree.selection()
        if not selecionado:
            messagebox.showwarning("Aviso", "Selecione um professor para excluir.")
            return

        id_, nome = tree.item(selecionado[0], "values")[0:2]

        if messagebox.askyesno("Confirmação", f"Excluir {nome}?"):
            excluir_professor(id_)
            carregar_dados_professores()
            limpar_campos()
            messagebox.showinfo("Removido", f"{nome} foi excluído.")

    # ========================= FUNÇÃO: Limpar Campos =========================
    def limpar_campos():
        """Limpa todos os campos de entrada e remove seleções da tabela."""
        entry_nome.delete(0, "end")
        entry_data_nasc.delete(0, "end")
        entry_especialidade.delete(0, "end")
        entry_telefone.delete(0, "end")
        entry_email.delete(0, "end")
        tree.selection_remove(tree.selection())

    # ========================= FUNÇÃO: Selecionar Registro =========================
    def ao_selecionar_professor(event):
        """
        Quando o usuário clica em uma linha da tabela,
        os dados são carregados nos campos de edição.
        """
        sel = tree.selection()
        if sel:
            valores = tree.item(sel[0], "values")
            id_ = valores[0]

            # Busca no banco
            prof = buscar_professor(id_)

            # Limpa campos antes de inserir
            entry_nome.delete(0, "end")
            entry_data_nasc.delete(0, "end")
            entry_especialidade.delete(0, "end")
            entry_telefone.delete(0, "end")
            entry_email.delete(0, "end")

            # Preenche com os dados encontrados
            if prof:
                entry_nome.insert(0, prof[0])
                entry_data_nasc.insert(0, prof[1])
                entry_especialidade.insert(0, prof[2])
                entry_telefone.insert(0, prof[3])
                entry_email.insert(0, prof[4])

    # ========================= CAMPOS DE ENTRADA =========================
    entry_nome = ctk.CTkEntry(frame, placeholder_text="* Nome completo...", width=360)
    entry_nome.pack(pady=(8, 6))

    entry_data_nasc = ctk.CTkEntry(frame, placeholder_text="* Data de Nascimento (DD/MM/AAAA)...", width=360)
    entry_data_nasc.pack(pady=(0, 8))

    entry_especialidade = ctk.CTkEntry(frame, placeholder_text="* Especialidade...", width=360)
    entry_especialidade.pack(pady=(0, 8))

    entry_telefone = ctk.CTkEntry(frame, placeholder_text="Telefone...", width=360)
    entry_telefone.pack(pady=(0, 8))

    entry_email = ctk.CTkEntry(frame, placeholder_text="E-mail...", width=360)
    entry_email.pack(pady=(0, 8))

    # ========================= BOTÕES =========================
    ctk.CTkButton(
        frame, text="CADASTRAR PROFESSOR", fg_color="#1f5aa6",
        text_color="white", width=360, command=inserir_professor
    ).pack(pady=(0, 6))

    ctk.CTkButton(
        frame, text="EDITAR PROFESSOR", fg_color="#1f5aa6",
        text_color="white", width=360, command=editar_professor
    ).pack(pady=(0, 6))

    ctk.CTkButton(
        frame, text="EXCLUIR PROFESSOR", fg_color="#c94a4a",
        text_color="white", width=360, command=excluir_dados_professor
    ).pack(pady=(0, 6))

    ctk.CTkButton(
        frame, text="LIMPAR CAMPOS", fg_color="#7a7a7a",
        text_color="white", width=360, command=limpar_campos
    ).pack()

    # ========================= ESTILO DO TREEVIEW =========================
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

    # Frame da tabela
    frame_tree = ctk.CTkFrame(frame, corner_radius=8)
    frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)

    # ========================= TABELA TREEVIEW =========================
    tree = ttk.Treeview(
        frame_tree,
        columns=("ID", "Nome", "Idade", "Especialidade", "Telefone", "E-mail"),
        show="headings"
    )

    # Configura colunas
    for col, w in [
        ("ID", 60), ("Nome", 360), ("Idade", 80),
        ("Especialidade", 200), ("Telefone", 140), ("E-mail", 220)
    ]:
        tree.heading(col, text=col)
        tree.column(col, width=w, anchor="center")

    # Barra de rolagem
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")

    tree.pack(expand=True, fill="both", padx=6, pady=6)

    # Evento ao selecionar linha
    tree.bind("<<TreeviewSelect>>", ao_selecionar_professor)

    # Carrega dados ao abrir a tela
    carregar_dados_professores()
