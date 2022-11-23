from sqlite3 import connect
from textwrap import fill
from tkinter import *
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import askyesno
import requests
import json
import tkinter
from tkinter import*
from tkinter import ttk
from 

# Variáveis globais
global hostX
global userX
global passwordX
global databaseX
global cursorX
global comando_sql_criar_database
global comando_sql_criar_table 
global comando_sql_inserir
global comando_sql_select
global comando_sql_seguranca
global comando_sql_deletar
global caixa_combo_diasX
global caixa_combo_mesesX
global caixa_combo_anosX
global caixa_combo_TurnoX
 
# Janela principal
janela = Tk()
janela.title('Consumindo uma API de CEP')
janela.geometry('890x385') #Define o tamanho da tela

janela.configure(bg='white')
janela.resizable(width=FALSE, height=FALSE)

frame1 = Frame(janela, bg='#aeb3b5', width=1000, height=385 )
frame1.place(x=0, y=0)

# JANELA 
label_cep_api = Label(janela, text='Consumindo uma API de CEP', fg='#011117', bg='#aeb3b5', font=('Arial','18'), justify='center')
label_cep_api.pack(side=TOP)

# FRAME 1 
label_cep = Label(text='CEP', fg='black', bg='#aeb3b5', font=('Arial','12'))
label_cep.place(x=120,y=80)

entry_cep = Entry(font=('Arial','12'), relief='solid')
entry_cep.place(x=175, y=80, height=28, width=150)

label_endereco = Label(text='Endereço', fg='black', bg='#aeb3b5', font=('Arial','12'))
label_endereco.place(x=85,y=120)

entry_endereco = Entry(font=('Arial','12'), relief='solid')
entry_endereco.place(x=175, y=120, height=28, width=400)

label_complemento = Label(text='Complemento', fg='black', bg='#aeb3b5', font=('Arial','12'))
label_complemento.place(x=60,y=160)

entry_complemento = Entry(font=('Arial','12'), relief='solid')
entry_complemento.place(x=175, y=160, height=28, width=400)

label_bairro = Label(text='Bairro', fg='black', bg='#aeb3b5', font=('Arial','12'))
label_bairro.place(x=110,y=200)

entry_bairro = Entry(font=('Arial','12'), relief='solid')
entry_bairro.place(x=175, y=200,height=28, width=400)

label_cidade = Label(text='Cidade', fg='black', bg='#aeb3b5', font=('Arial','12'))
label_cidade.place(x=105,y=250)

entry_cidade= Entry(font=('Arial','12'), relief='solid')
entry_cidade.place(x=175, y=250,height=28, width=400)

label_uf = Label(text='UF', fg='black', bg='#aeb3b5', font=('Arial','12'))
label_uf.place(x=130,y=300)

entry_uf= Entry(font=('Arial','12'), relief='solid')
entry_uf.place(x=175, y=300,height=28, width=150)

style_ferramentas = ttk.Style()
style_ferramentas.theme_use("vista")

# Grid de registros do banco

# Botões
botao_pesquisar = Button(frame_principal, command=consultarcep, text='Buscar',relief='groove',font=('','10'), fg='black',activeforeground='blue')
botao_pesquisar.place(x=340,y=82,width=70,height=25)

botao_limpar = Button(text='Limpar',font=('','10'),relief='groove', fg='black', activeforeground='blue')
botao_limpar.place(x=600,y=320,width=80,height=30)

botao_sair = Button(text='Sair',font=('','10'),relief='groove', fg='black', activeforeground='blue')
botao_sair.place(x=700,y=320,width=80,height=30)

#botao_inserir = Button(text='Inserir',relief='groove',command=inserir_novo_aluno,font=('','12'), fg='black', activeforeground='orange')
#botao_inserir.place(x=700,y=320,width=80,height=30)

#botao_excluir = Button(text='Excluir',command=deletar_registro,font=('','10'),relief='groove', fg='black', activeforeground='blue')
#botao_excluir.place(x=600,y=320,width=80,height=30)

# Funções
#conectar()
#criar_database()
#criar_tabela()

janela.mainloop()