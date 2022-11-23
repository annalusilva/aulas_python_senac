import glob
import os
from tkinter import font
import mysql.connector
from mysql.connector import Error
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter.messagebox import askyesno
from tkinter.tix import *

# Variáveis globais
global hostX, userX, passwordX, databaseX, cursorX
global comando_sql_criar_database, comando_sql_criar_table,  comando_sql_inserir, comando_sql_select, comando_sql_seguranca, comando_sql_deletar
global caixa_combo_diasX, caixa_combo_mesesX, caixa_combo_anosX

global fonte_tela, fonte_label
global path_foto, img_bt_inserir, img_bt_excluir
 
# Dados para conexão com o banco de dados
hostX = 'localhost'
userX = 'root'
passwordX = 'acesso123'
databaseX = 'academico'

fonte_tela = 'Roboto'
fonte_label = 'Roboto'

# Instruções SQL (não mexer)
comando_sql_criar_database = "CREATE DATABASE IF NOT EXISTS academico"

# Alterar conforme dados do banco de dados
comando_sql_criar_table = "CREATE TABLE IF NOT EXISTS `usuarios` (`id_user` INT NOT NULL AUTO_INCREMENT, `nome_user` VARCHAR(50) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL, `path_foto_user` VARCHAR(200) CHARACTER SET 'utf8' COLLATE 'utf8_general_ci' NOT NULL, `data_user` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,`senha_user` VARCHAR(30) NOT NULL, PRIMARY KEY (`id_user`))"

# Alterar conforme dados do banco de dados
comando_sql_inserir = "INSERT INTO usuarios (nome_user, path_foto_user, data_user, senha_user) VALUES(%s, %s, %s, %s)"
comando_sql_select = "SELECT * FROM usuarios;"
comando_sql_seguranca = "SET SQL_SAFE_UPDATES = 0;"
comando_sql_deletar = "DELETE FROM usuarios WHERE id_user = %s;"

caixa_combo_diasX = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
caixa_combo_mesesX = ['01','02','03','04','05','06','07','08','09','10','11','12']
caixa_combo_anosX = ["2017","2018","2019","2020","2021","2022","2023","2024","2025","2026","2027","2028","2029","2030"]
caixa_combo_TutorX = ["Pai","Mãe","Avó","Avô","Outros"]
caixa_combo_TipoX = ["Celular","Residencial","Comercial","Outros"]

# Lista de mensagens
mensagem_bd = ['Erro de Conexão ao banco de dados.',
               'Erro ao criar banco de dados.',
               'Erro ao criar tabela no banco de dados.',
               'Registro cadastrado com sucesso',
               'Erro ao cadastrar o registro',
               'Erro ao deletar o cadastro',
               'Deseja deletar o registro selecionado?']

# Função para conectar o banco de dados.
def conectar():
    global banco
    try:
        banco = mysql.connector.connect(
            host = hostX, 
            user = userX,
            password = passwordX)
        #print('Conexão 0: ', banco)
    except Error as erro:
        print(mensagem_bd[0])
            
# Função para criar o banco de dados
def criar_database():
    global banco
    try:
        conectar()
        cursorX = banco.cursor()
        cursorX.execute(comando_sql_criar_database)        
    except Error as erro:
        print(mensagem_bd[1])
        
    if banco.is_connected():
        cursorX.close()

# Função para criar tabela
def criar_tabela():
    global banco
    try:
        banco = mysql.connector.connect(
            host = hostX,
            user = userX,
            password = passwordX,
            database = databaseX
        )

        cursorX = banco.cursor()
        cursorX.execute(comando_sql_criar_table)
        print(banco)
    except Error as erro:
        print(mensagem_bd[2])
        
    if banco.is_connected():
            banco.close()
    
# Inserir novo registro
def inserir_novo_registro():
    global banco
    entry_01['state'] = 'normal'
    entry_01.delete(0,'end')
    entry_01['state'] = 'disabled'
    
    banco = mysql.connector.connect(
        host=hostX,
        user=userX,
        password=passwordX,
        database=databaseX
    )
    
    cursorX = banco.cursor()
    cursorX.execute(comando_sql_criar_table)
    try:
        if banco.is_connected():
            agrupa_data = str(caixa_combo_anos.get() + '-' + caixa_combo_meses.get() + '-'+ caixa_combo_dias.get())
            # Alterar os nomes das caixas
            dados = (str(entry_nome.get()), str(entry_foto.get()), str(agrupa_data), str(entry_senha.get()))
            cursorX.execute(comando_sql_inserir, dados)
            banco.commit()
            messagebox.showinfo('AVISO', mensagem_bd[3])
    except:
        messagebox.showerror('ERRO', mensagem_bd[4])
    
    # Para apagar o conteúdo das caixa
    # Alterar os nomes das caixas (entry)
    entry_01['state'] = 'normal'
    entry_01.delete(0,'end')
    entry_01['state'] = 'disabled'
    entry_nome.delete(0,'end')
    entry_foto.delete(0,'end')
    entry_senha.delete(0,'end')
    caixa_combo_dias.delete(0,'end')
    caixa_combo_meses.delete(0,'end')
    caixa_combo_anos.delete(0,'end')

    desconecta_banco()
    
# Exibe os registros do banco de dados
def mostrar_todos_registros():
    banco = mysql.connector.connect(
        host=hostX,
        user=userX,
        password=passwordX,
        database=databaseX
    )
 
    if banco.is_connected():
        grid_reg.delete(*grid_reg.get_children(None))
        cursorX = banco.cursor()
        cursorX.execute(comando_sql_select)
        dados_tabela = cursorX.fetchall()
        #print(dados_tabela)
        for i in range(0, len(dados_tabela)):
            grid_reg.insert(parent='', index=i, values=dados_tabela[i])

# Deletar o registro selecionado no Grid            
def deletar_registro():
    deletar_reg = messagebox.askyesno('ATENÇÃO', mensagem_bd[6])

    curItem = grid_reg.focus()
    valor = grid_reg.item(curItem)
    lista_valores = valor['values']
    
    try:
        if deletar_reg:
            banco = mysql.connector.connect(
                host=hostX,
                user=userX,
                password=passwordX,
                database=databaseX
            )
            if banco.is_connected():
                grid_reg.delete(curItem)
                cursorX = banco.cursor()
                dados = [(lista_valores[0])]
                cursorX.execute(comando_sql_seguranca)
                cursorX.execute(comando_sql_deletar, dados)
                banco.commit()
    except:
        messagebox.showerror('ERRO', mensagem_bd[5])
        
# Mostrar o registro selecionado no Grid           
def mostrar_registro_selecionado(event):
    curItem = grid_reg.focus()
    valor = grid_reg.item(curItem)
    lista_valores = valor['values']
    print('Lista: ', lista_valores)
    
    # Alterar nomes das caixas (entry)
    entry_01.config(state="normal")
    entry_01.insert(0, lista_valores[0])
    entry_01.config(state="disabled")

    entry_nome.insert(0, lista_valores[1])
    entry_foto.insert(0, lista_valores[2])
    caixa_combo_dias.insert(0, lista_valores[3][8:10])
    caixa_combo_meses.insert(0, lista_valores[3][5:7])    
    caixa_combo_anos.insert(0, lista_valores[3][:4])    
    entry_senha.insert(0, lista_valores[4])
    
# Desconecta banco
def desconecta_banco():
    if banco.is_connected():
        banco.close()
 
# Função para mostrar o conteúdo do campo de senha
def exibe_senha():
    senha1 = str(entry_senha.get())
    messagebox.showinfo(title="Menssagem",message=senha1,parent=janela)

# Mostrar a foto do usuário - Não está funcionando
'''
def mostra_foto(path_foto):
    #  Imagem
    print(path_foto)
    foto=PhotoImage(file=path_foto)
    Label(frame2,image=foto,bg='grey',).pack()
    
def carrega_foto(event):
    path_foto = entry_foto.get()
    foto=PhotoImage(file=path_foto)
    Label(janela,image=foto,).place(x=0,y=0)
'''
      
# Janela principal
janela = Tk()
janela.title('Sistema acadêmico')
janela.geometry('1000x385') #Define o tamanho da tela

janela.configure(bg='white')
janela.resizable(width=FALSE, height=FALSE)

frame1 = Frame(janela, bg='white', width=1000, height=385)
frame1.place(x=0, y=0)
frame2= Frame(janela, bg='white', width=50, height=50)
frame2.place(x=910, y=30)
frame3 = Frame(janela, bg='gray', width=295, height=220)
frame3.place(x=525,y=80)

#frame4 = Frame(janela, bg='white', width=1000, height=60)
#frame4.place(x=0,y=325)

# JANELA 
# ToolBar
toolbar = Frame(janela)
toolbar.pack(side=TOP, fill=X)
b1 = Button(
    toolbar,
    background='orange',
    relief=FLAT,
    compound = LEFT,
    text="                                    Mostrar  registros                                                                                                                                                                                                                                                                                                           ",
    command=mostrar_todos_registros,
    #image=imgs["notepad"]
    )

b1.pack(side=LEFT, padx=0, pady=0)
# Menubar
menubar = tk.Menu(janela)
filemenu = tk.Menu(menubar)
filemenu.add_command(label="Mostrar reistros", command=mostrar_todos_registros)
filemenu.add_command(label="Sair", command=janela.quit)
menubar.add_cascade(label="Arquivos", menu=filemenu)
janela.config(menu=menubar)

# StatusBar
barrastatus = tk.Label(janela, text="Usuários", bd=1, relief=tk.SUNKEN, anchor=tk.W)
barrastatus.pack(side=tk.BOTTOM, fill=tk.X)

# Começa a tela - deve ser alterada conforme modelo do banco de dados
label_cadastro = Label(janela, text='Cidade', fg='orange', bg='white', font=(fonte_tela,'30'), justify='center')
label_cadastro.pack(side=TOP)

# FRAME 1
label_idcidade = Label(frame1, text='Id cidade', fg='blue', bg='white', font=(fonte_label,'12'))
label_idcidade.place(x=95,y=83)
entry_idcidade = Entry(frame1, font=(fonte_label,'12'), relief='solid')
entry_idcidade.place(x=175, y=82, height=25,width=150)
entry_idcidade['state'] = 'disabled'

label_nome = Label(frame1, text='Nome da cidade', fg='blue', bg='white', font=(fonte_tela,'12'))
label_nome.place(x=45, y=120)
entry_nome = Entry(frame1, font=(fonte_label,'12'), relief='solid')
entry_nome.place(x=175,y=122,height=25, width=300)

label_ufcidade = Label(text='UF da cidade ', fg='blue', bg='white', font=(fonte_tela,'12'))
label_ufcidade .place(x=65,y=153,height=25, width=100)
entry_ufcidade  = Entry(frame1, font=(fonte_label,'12'), relief='solid')
entry_ufcidade .place(x=175,y=155,height=25, width=150)


#entry_foto.bind("<FocusOut>",carrega_foto)

#imagem = tk.PhotoImage(file="img.png")
#w = tk.Label(frame2, image= imagem)
#w.imagem = imagem
#w.pack()

#foto=PhotoImage('img.png')
#Label(frame2, image=foto)

# Grid de registros do banco
colunas_grid = ('Cod','Usuário')
grid_reg = ttk.Treeview(frame3, columns=colunas_grid, show='headings')

grid_reg.column("Cod", width=55, anchor=CENTER, minwidth=55, stretch=NO)
grid_reg.column("Usuário", width=230, anchor=CENTER, minwidth=150, stretch=NO)

grid_reg.heading('Cod', text='Cod')
grid_reg.heading('Usuário', text='Usuario')
grid_reg.place(x=0, y=0, width=295, height=220)

grid_reg.bind("<Button>", mostrar_registro_selecionado)

#scrollbar_x = ttk.Scrollbar(frame3, orient='horizontal', command=grid_reg.xview)
#grid_reg.configure(xscrollcommand=scrollbar_x.set)
#scrollbar_x.place(x=0,y=200,width=300)

scrollbar_y = ttk.Scrollbar(frame3,orient='vertical', command=grid_reg.yview)
grid_reg.configure(yscrollcommand=scrollbar_y.set)
scrollbar_y.place(x=396,y=71,height=240)

# Botões
img_bt_inserir=PhotoImage(file = r"salvar.png") 
img_bt_excluir=PhotoImage(file = r"excluir.png")

tip = Balloon(janela)

botao_inserir = Button(frame1,text='', image=img_bt_inserir, compound = LEFT,relief='groove', command=inserir_novo_registro, font=(fonte_label,'14'), fg='black', activeforeground='orange')
botao_inserir.place(x=10,y=335,width=80,height=30)
tip.bind_widget(botao_inserir, balloonmsg="Salvar o registro na base de dados")

botao_excluir = Button(frame1,text='', image=img_bt_excluir, compound = LEFT, command=deletar_registro,font=(fonte_label,'14'), relief='groove', fg='black', activeforeground='orange')
botao_excluir.place(x=100,y=335,width=80,height=30)
tip.bind_widget(botao_excluir, balloonmsg="Excluir o registro selecionado da base de dados")

#botao_mostrar_grid = Button(frame1, text='Registros',command=mostrar_todos_registros,font=(fonte_label,#'14'),relief='groove',fg='black', activeforeground='orange')
#botao_mostrar_grid.place(x=700,y=345,width=100,height=30)

# Incio do programa. As funções serão chamadas e executadas
#conectar()
#criar_database()
#criar_tabela()

janela.mainloop()