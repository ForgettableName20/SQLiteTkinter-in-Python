# -*- coding: utf-8 -*-

from email import message
import sqlite3
import atexit
import tkinter as tk
from tkinter import ttk, messagebox

con = sqlite3.connect("mercearia.db")
atexit.register(con.close)
cursor = con.cursor()

cursor.execute("""
    Create table if not exists produtos(
    id integer primary key autoincrement,
    nome TEXT NOT NULL,
    categoria TEXT NOT NULL,
    preco REAL NOT NULL,
    unid_medida TEXT NOT NULL)
    """)

con.commit()

def adicionar_produto():
    if not validar_campos():
        return
    try:
        nome = entrada_nome.get()
        categoria = entrada_categoria.get()
        preco = float(entrada_preco.get())
        unid_medida = entrada_unid_medida.get()

        cursor.execute("insert into produtos (nome, categoria, preco, unid_medida) values (?, ?, ?, ?)", (nome, categoria, preco, unid_medida))
        con.commit()
        messagebox.showinfo ("Sucesso", "Inserido com sucesso!")

        listar_produtos()
        limpar_campos()
    except:
        messagebox.showerror("Erro", f"Erro ao adicionar produto : {Exception}")

def listar_produtos(filtro_nome="", filtro_categoria=""):
    parte_nome = f"%{filtro_nome}%"
    parte_categoria = f"%{filtro_categoria}%"

    tree.delete(*tree.get_children())

    cursor.execute("select * from produtos where nome like ? and categoria like ?", ("%" + parte_nome + "%", "%" + parte_categoria + "%",))

    dados = cursor.fetchall()
    if dados:
        for row in dados:
            tree.insert("", "end", values=row)
    else:
        messagebox.showinfo("Aviso", "Nenhum resultado encontrado")

def atualizar_produtos():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um produto para atualizar")
        return
    if not validar_campos():
        return
    id_prod = tree.item(selected)["values"][0]
    try:
        cursor.execute("update produtos set nome=?, categoria=?, preco=?, unid_medida=? where id=?", (entrada_nome.get(), entrada_categoria.get(), entrada_preco.get(), entrada_unid_medida.get(), id_prod))
        con.commit()
        listar_produtos()
        limpar_campos()
        messagebox.showinfo("Sucesso", "Produto atualizado com sucesso")
    except:
        messagebox.showerror("Error", f"Erro ao atualizar o produto: {Exception}")

def remover_produto():
    selected = tree.focus()
    if not selected:
        messagebox.showwarning("Aviso", "Selecione um produto para remover")
        return
    id_prod = tree.item(selected)["values"][0]
    if messagebox.askyesno("Confirmar", "Tem a certeza que deseja remover este produto?"):
        try:
            cursor.execute("delete from produtos where id=?", (id_prod,))
            con.commit()
            listar_produtos()
            limpar_campos()
            messagebox.showinfo("Sucesso", "Produto removido com sucesso")
        except:
            messagebox.showerror("Erro", f"Erro ao remover o produto: {Exception}")

def validar_campos():
    if not entrada_nome.get().strip() or not entrada_categoria.get().strip() or not entrada_preco.get().strip() or not entrada_unid_medida.get().strip():
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return False
    try:
        float(entrada_preco.get())
    except ValueError:
        messagebox.showerror("Erro", "Preço deve ser um número válido")
        return False
    return True

def on_tree_select(event):
    selected = tree.focus()
    if not selected:
        return

    values = tree.item(selected, "values")
    entrada_nome.delete(0, tk.END)
    entrada_categoria.delete(0, tk.END)
    entrada_preco.delete(0, tk.END)
    entrada_unid_medida.delete(0, tk.END)

    entrada_nome.insert(0, values[1])
    entrada_categoria.insert(0, values[2])
    entrada_preco.insert(0, values[3])
    entrada_unid_medida.insert(0, values[4])

def limpar_campos():
    entrada_nome.delete(0, tk.END)
    entrada_categoria.delete(0, tk.END)
    entrada_preco.delete(0, tk.END)
    entrada_unid_medida.delete(0, tk.END)
    filtro_nome.delete(0, tk.END)
    filtro_categoria.delete(0, tk.END)

def aplicar_filtro():
    listar_produtos(filtro_nome.get(), filtro_categoria.get())


janela = tk.Tk()
janela.title("Produtos Mercearia")
janela.geometry("1100x600")

entrada = tk.Frame(janela)
entrada.pack()

tk.Label(entrada, text="Nome").grid(row=0, column=0)
tk.Label(entrada, text="Categoria").grid(row=1, column=0)
tk.Label(entrada, text="Preço").grid(row=2, column=0)
tk.Label(entrada, text="Unidade de medida").grid(row=3, column=0)

entrada_nome = tk.Entry(entrada)
entrada_categoria = tk.Entry(entrada)
entrada_preco = tk.Entry(entrada)
entrada_unid_medida = tk.Entry(entrada)

entrada_nome.grid(row=0, column=1)
entrada_categoria.grid(row=1, column=1)
entrada_preco.grid(row=2, column=1)
entrada_unid_medida.grid(row=3, column=1)

botao = tk.Frame(janela)
botao.pack(pady=10)

tk.Button(botao, text="Inserir", command=adicionar_produto).grid(row=0, column=0, padx=5)
tk.Button(botao, text="Atualizar", command=atualizar_produtos).grid(row=0, column=1, padx=5)
tk.Button(botao, text="Remover", command=remover_produto).grid(row=0, column=2, padx=5)
tk.Button(botao, text="Limpar Campos", command=limpar_campos).grid(row=0, column=3, padx=5)

filtro = tk.Frame(janela)
filtro.pack(pady=10)

tk.Label(filtro, text="Filtrar por nome:").grid(row=0, column=0, padx=5)
filtro_nome = tk.Entry(filtro)
filtro_nome.grid(row=0, column=1)

tk.Label(filtro, text="Filtrar por categoria:").grid(row=0, column=4, padx=5)
filtro_categoria = tk.Entry(filtro)
filtro_categoria.grid(row=0, column=5)

tk.Button(filtro, text="Aplicar Filtro", command=aplicar_filtro).grid(row=0, column=7, padx=10)

columns = ("ID", "Nome", "Categoria", "Preço", "Unidade")
tree = ttk.Treeview(janela, columns = columns, show = "headings")
tree.heading("ID", text = "ID")
tree.heading("Nome", text = "Nome")
tree.heading("Categoria", text = "Categoria")
tree.heading("Preço", text = "Preço")
tree.heading("Unidade", text = "Unidade")
tree.pack(fill=tk.BOTH, expand=True, padx = 20, pady = 10)
tree.bind("<<TreeviewSelect>>", on_tree_select)

listar_produtos()

janela.mainloop()