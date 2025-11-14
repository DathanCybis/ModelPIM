import customtkinter as ctk
from tkinter import ttk, messagebox
from banco import listar_atividades, atualizar_atividade, excluir_atividade, cadastrar_atividade, buscar_nome_turmas
from ia import classificar_dificuldade, recomendar_data_entrega
from datetime import datetime

def criar_tela_atividades(frame):
    def carregar_atividades():
        for item in tree.get_children(): tree.delete(item)
        for at in listar_atividades():
            # Converte datas para DD/MM/AAAA antes de mostrar
            criado = datetime.strptime(at[3], "%Y-%m-%d").strftime("%d/%m/%Y") if at[3] else ""
            entrega = datetime.strptime(at[4], "%Y-%m-%d").strftime("%d/%m/%Y") if at[4] else ""
            tree.insert("", "end", values=(at[0], at[1], at[2], criado, entrega, at[5], at[6]))

    def limpar_campos():
        entry_titulo.delete(0, "end")
        text_descricao.delete("1.0", "end")
        menu_turma.set("Selecione uma turma")
        entry_data_entrega.delete(0, "end")
        combo_dificuldade.set("")

    def formatar_data_entrada(data_str):
        """Converte DD/MM/AAAA para YYYY-MM-DD para o banco"""
        try:
            return datetime.strptime(data_str, "%d/%m/%Y").date().isoformat()
        except Exception:
            return None

    def inserir_atividade():
        titulo = entry_titulo.get().strip()
        descricao = text_descricao.get("1.0", "end").strip()
        turma = menu_turma.get()
        data_criacao = datetime.today().date().isoformat()
        dificuldade = combo_dificuldade.get().strip() or classificar_dificuldade(titulo, descricao)
        
        # Trata data de entrega
        data_entrega_input = entry_data_entrega.get().strip()
        data_entrega = formatar_data_entrada(data_entrega_input) or recomendar_data_entrega(data_criacao, dificuldade)
        
        if not titulo:
            messagebox.showwarning("Atenção", "Título é obrigatório.")
            return
        
        cadastrar_atividade(
            titulo, descricao, data_criacao, data_entrega,
            dificuldade, turma if turma != "Selecione uma turma" else None
        )
        carregar_atividades()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Atividade cadastrada!")

    def ao_selecionar(event):
        sel = tree.selection()
        if sel:
            vals = tree.item(sel[0], "values")
            entry_titulo.delete(0, "end"); entry_titulo.insert(0, vals[1])
            text_descricao.delete("1.0", "end"); text_descricao.insert("1.0", vals[2] or "")
            # Converte data do banco (YYYY-MM-DD) para DD/MM/AAAA
            entry_data_entrega.delete(0, "end")
            if vals[4]:
                dt = datetime.strptime(vals[4], "%d/%m/%Y").strftime("%d/%m/%Y")  # já está no formato DD/MM/AAAA
                entry_data_entrega.insert(0, dt)
            combo_dificuldade.set(vals[5] or ""); menu_turma.set(vals[6] or "Selecione uma turma")

    def editar_atividade():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma atividade para editar.")
            return
        id_ = tree.item(sel[0], "values")[0]
        titulo = entry_titulo.get().strip()
        descricao = text_descricao.get("1.0", "end").strip()
        dificuldade = combo_dificuldade.get().strip() or classificar_dificuldade(titulo, descricao)
        
        data_entrega_input = entry_data_entrega.get().strip()
        data_entrega = formatar_data_entrada(data_entrega_input)
        
        turma = menu_turma.get()
        atualizar_atividade(
            id_, titulo, descricao, data_entrega, dificuldade,
            turma if turma != "Selecione uma turma" else None
        )
        carregar_atividades()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Atividade atualizada.")

    def excluir_atividade_tree():
        sel = tree.selection()
        if not sel:
            messagebox.showwarning("Aviso", "Selecione uma atividade para excluir.")
            return
        id_, titulo = tree.item(sel[0], "values")[0:2]
        if messagebox.askyesno("Confirmação", f"Excluir atividade '{titulo}'?"):
            excluir_atividade(id_)
            carregar_atividades()
            limpar_campos()
            messagebox.showinfo("Removido", "Atividade excluída.")

    entry_titulo = ctk.CTkEntry(frame, placeholder_text="* Título...", width=360)
    entry_titulo.pack(pady=(8,6))
    text_descricao = ctk.CTkTextbox(frame, width=360, height=120)
    text_descricao.pack(pady=(0,8))
    entry_data_entrega = ctk.CTkEntry(frame, placeholder_text="Data entrega (DD/MM/AAAA) - opcional", width=360)
    entry_data_entrega.pack(pady=(0,8))
    
    menu_turma = ctk.CTkOptionMenu(frame, values=buscar_nome_turmas(), width=360)
    menu_turma.pack(pady=(0,8))
    menu_turma.set("Selecione uma turma")
    frame.bind("<Visibility>", lambda e: menu_turma.configure(values=buscar_nome_turmas()))
    
    combo_dificuldade = ctk.CTkOptionMenu(frame, values=["Alta", "Média", "Baixa"], width=360)
    combo_dificuldade.pack(pady=(0,8))
    combo_dificuldade.set("Selecionar dificuldade")

    ctk.CTkButton(frame, text="CADASTRAR", fg_color="#1f5aa6", text_color="white", width=360, command=inserir_atividade).pack(pady=(0,6))
    ctk.CTkButton(frame, text="EDITAR", fg_color="#1f5aa6", text_color="white", width=360, command=editar_atividade).pack(pady=(0,6))
    ctk.CTkButton(frame, text="EXCLUIR", fg_color="#c94a4a", text_color="white", width=360, command=excluir_atividade_tree).pack(pady=(0,6))
    ctk.CTkButton(frame, text="LIMPAR", fg_color="#7a7a7a", text_color="white", width=360, command=limpar_campos).pack(pady=(0,6))

    frame_tree = ctk.CTkFrame(frame, corner_radius=8)
    frame_tree.pack(side="bottom", expand=True, fill="both", padx=10, pady=10)
    
    cols = ("ID", "Título", "Descrição", "Criado em", "Entrega", "Dificuldade", "Turma")
    tree = ttk.Treeview(frame_tree, columns=cols, show="headings")
    for c,w in [("ID",60),("Título",260),("Descrição",360),("Criado em",120),("Entrega",120),("Dificuldade",100),("Turma",140)]:
        tree.heading(c, text=c)
        tree.column(c, width=w, anchor="center")
    scroll = ttk.Scrollbar(frame_tree, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scroll.set)
    scroll.pack(side="right", fill="y")
    tree.pack(expand=True, fill="both", padx=6, pady=6)
    tree.bind("<<TreeviewSelect>>", ao_selecionar)
    
    carregar_atividades()
