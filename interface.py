import os
import tkinter as tk
from tkinter import END, ttk,font 
from tkinter import messagebox
from tkinter import Tk, filedialog
from ttkthemes import ThemedTk
import sqlite3
import sqlite3
import pandas as pd
import openpyxl
import xlsxwriter



id_int_sod = 0
id_interno = 0
id_int_perfil = 0
id_int_user = 0
""" 
~-----------SUMÁRIO---------------SUMÁRIO-------------SUMÁRIO----------SUMÁRIO-------------SUMÁRIO-----------------!

    TODO // SEPARAÇÃO DE BUTTONS/ENTRYS/BASES/LABELS
    & COMENTARIOS EXPLICATIVOS
    ! !!!! IMPORTATES LEIA TODOS EM VERMELHO COM BASTANTE ATENÇÃO !!!!!
    ~ DIVISÕES
    ^ FONTES
    * TITULOS
    ? IMAGENS
    
~-----------SUMÁRIO---------------SUMÁRIO-------------SUMÁRIO----------SUMÁRIO-------------SUMÁRIO-----------------!
"""
#& Funcção que seleciona o arquivo XLSX
def selecionar_arquivo():
    root = Tk()
    root.withdraw()  # Para ocultar a janela principal

    caminho_arquivo = filedialog.askopenfilename(
        title="Selecionar arquivo",
        filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
    )

    return caminho_arquivo
#& Funcção que faz a leitura do arquivo XLSX
def ler_arquivo_xlsx():
    try:
        # Obtém o caminho do arquivo selecionado
        caminho_arquivo = selecionar_arquivo()

        if not caminho_arquivo:
            return None

        # Carrega o arquivo Excel
        df1 = pd.read_excel(caminho_arquivo, sheet_name= 0)
        df2 = pd.read_excel(caminho_arquivo, sheet_name= 1)
        df3 = pd.read_excel(caminho_arquivo, sheet_name= 2)
        df4 = pd.read_excel(caminho_arquivo, sheet_name= 3)

        # Retorna o DataFrame para mais manipulações, se necessário
        return df1 ,df2, df3, df4
    except Exception as e:
        return None
#& Funcção que cadasta os dados do arquivo XLSX
def cadArquivo():
    arquivo = ler_arquivo_xlsx()
    def cadAqrquivoSistemas():
        def iserirsistema():
            cursor.execute("""
                INSERT INTO sistemas(id, nome)
                VALUES (?, ?)
            """, (cod, nam))
            bd.commit()

        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()

        codigo = arquivo[0].iloc[:, 0].tolist()
        nome = arquivo[0].iloc[:, 1].tolist()

        index = []
        contador = 0
        for i in codigo:
            if not isinstance(i, int):
                index.append(contador)
            contador += 1

        indice = 0
        for i in range(len(codigo)):

            cursor.execute("""SELECT nome FROM sistemas;""")
            verificaSeExistenome = [item[0] for item in cursor.fetchall()]
            cursor.execute("""SELECT id FROM sistemas;""")
            verificaSeExisteid = [item[0] for item in cursor.fetchall()]
            
            cod = codigo[indice]
            nam = nome[indice]

            if indice in index and nam not in verificaSeExistenome:
                cod = 1 if not verificaSeExisteid else verificaSeExisteid[-1] + 1
                iserirsistema()
                indice += 1
            elif nam in verificaSeExistenome:
                indice += 1
            elif cod in verificaSeExisteid and nam not in verificaSeExistenome:
                cod = 1 if not verificaSeExisteid else verificaSeExisteid[-1] + 1
                iserirsistema()
                indice += 1
            else:
                iserirsistema()
                indice += 1

        bd.close()
    def cadAqrquivoPerfils():
        def iserirperfil():
            cursor.execute("""
                INSERT INTO perfil(nome, descricao,id_sistema)
                VALUES (?, ?, ?)
            """, (nam, desc, cod))
            bd.commit()
            
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()

        nome = arquivo[1].iloc[:, 0].tolist()
        descricao = arquivo[1].iloc[:, 1].tolist()
        codigoSistema = arquivo[1].iloc[:, 2].tolist()


        index = []
        contador = 0
        for i in codigoSistema:
            if not isinstance(i, int):
                index.append(contador)
            contador += 1

        indice = 0
        for i in range(len(codigoSistema)):
            cursor.execute("""SELECT id FROM sistemas;""")
            verificaSeExisteid = [item[0] for item in cursor.fetchall()]

            cod = codigoSistema[indice]
            nam = nome[indice]
            desc = descricao[indice]

            if indice in index or nam == 'nan' or desc == 'nan':
                indice += 1
            elif cod not in verificaSeExisteid:
                indice += 1
            else:
                iserirperfil()
                indice += 1
        bd.close()
    def cadAqrquivoUsuario():
        def iserirusuario():
            cursor.execute("""
                INSERT INTO usuarios(nome, descricao,cpf)
                VALUES (?, ?, ?)
            """, (nam, desc, pf))
            bd.commit()
            
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()

        nome = arquivo[2].iloc[:, 0].tolist()
        cpf = arquivo[2].iloc[:, 1].tolist()
        descricao = arquivo[2].iloc[:, 2].tolist()

        indice = 0
        for i in range(len(cpf)):
            cursor.execute("""SELECT cpf FROM usuarios;""")
            verificacpf = [item[0] for item in cursor.fetchall()]

            pf = str(cpf[indice])
            nam = nome[indice]
            desc = descricao[indice]

            if pf == 'nan' or nam == 'nan' or desc == 'nan':
                indice += 1
            elif pf in verificacpf:
                indice += 1
            else:
                iserirusuario()
                indice += 1
        bd.close()
    def cadAqrquivoMsod():
        def iserirMsod():
            cursor.execute("""
                                INSERT INTO MatrizSod(id_sistema_1,nome_perfil_1,id_sistema_2,nome_perfil_2)
                                VALUES (?,?,?,?)
                        """, (codS1,namP1,codS2,namP2))
            bd.commit()
            
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()

        s1 = arquivo[3].iloc[:, 0].tolist()
        p1 = arquivo[3].iloc[:, 1].tolist()
        s2 = arquivo[3].iloc[:, 2].tolist()
        p2 = arquivo[3].iloc[:, 3].tolist()

        indice = 0
        for i in range(len(s1)):
            cursor.execute("""SELECT id FROM sistemas;""")
            verificaSeExisteid = [item[0] for item in cursor.fetchall()]
            cursor.execute("""SELECT nome FROM perfil;""")
            verificaNome = [item[0] for item in cursor.fetchall()]

            codS1 = s1[indice]
            namP1 = p1[indice]
            codS2 = s2[indice]
            namP2 = p2[indice]

            if codS1 == 'nan' or codS2 == 'nan' or namP1 == 'nan' or namP2 == 'nan':
                indice += 1
            elif codS1 not in verificaSeExisteid or codS2 not in verificaSeExisteid:
                indice += 1
            elif namP1 not in verificaNome or namP2 not in verificaNome:
                indice += 1
            else:
                iserirMsod()
                indice += 1
        bd.close()

    cadAqrquivoSistemas()
    cadAqrquivoPerfils()
    cadAqrquivoUsuario()
    cadAqrquivoMsod()
#& Funcção que exporta o arquivo XLSX
def exportar_tabelas_sqlite_para_excel(caminho_destino=None):
    tabelas = ['sistemas', 'perfil','usuarios','MatrizSod','perfil_usuarios']
    conexao = bd = sqlite3.connect('SOD_DB.db')
    try:
        # Se o caminho_destino não for fornecido, abre uma janela para escolher o local
        if caminho_destino is None:
            root = Tk()
            root.withdraw()
            caminho_destino = filedialog.asksaveasfilename(
                defaultextension=".xlsx",
                filetypes=[("Arquivos Excel", "*.xlsx"), ("Todos os arquivos", "*.*")]
            )
            root.destroy()

        # Cria um objeto ExcelWriter para escrever em várias sheets no arquivo Excel
        with pd.ExcelWriter(caminho_destino, engine='xlsxwriter') as writer:
            # Itera sobre as tabelas especificadas e escreve cada uma em uma sheet separada
            for tabela in tabelas:
                consulta_sql = f"SELECT * FROM {tabela};"
                dados_do_banco = pd.read_sql_query(consulta_sql, conexao)
                dados_do_banco.to_excel(writer, sheet_name=tabela, index=False)

        print(f"As tabelas foram exportadas para {caminho_destino}")
        return True
    except Exception as e:
        print(f"Erro ao exportar para o arquivo Excel: {e}")
        return False
    finally:
        if conexao:
            conexao.close()

#& valida o CNPJ.
def valida_cnpj(cnpj):
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Verifica se o CNPJ tem 14 dígitos e não contém letras
    if len(cnpj) == 14 and cnpj.isdigit():
        return True
    else:
        return False
#& formata o CNPJ.
def formata_cnpj(cnpj):
    # Remove caracteres não numéricos
    cnpj = ''.join(filter(str.isdigit, cnpj))

    # Formata o CNPJ
    cnpj_formatado = f'{cnpj[:2]}.{cnpj[2:5]}.{cnpj[5:8]}/{cnpj[8:12]}-{cnpj[12:]}'

    return cnpj_formatado
#& valida o CPF.
def valida_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Verifica se o CPF tem 11 dígitos
    if len(cpf) != 11:
        return False

    # Verifica se todos os dígitos são iguais
    if cpf == cpf[0] * 11:
        return False

    # Calcula o primeiro dígito verificador
    total = 0
    for i in range(9):
        total += int(cpf[i]) * (10 - i)
    resto = total % 11
    digito1 = 11 - resto if resto >= 2 else 0

    # Verifica o primeiro dígito verificador
    if digito1 != int(cpf[9]):
        return False

    # Calcula o segundo dígito verificador
    total = 0
    for i in range(10):
        total += int(cpf[i]) * (11 - i)
    resto = total % 11
    digito2 = 11 - resto if resto >= 2 else 0

    # Verifica o segundo dígito verificador
    if digito2 != int(cpf[10]):
        return False

    # Se chegou até aqui, o CPF é válido
    return True
#& formata o CNPJ.
def formata_cpf(cpf):
    # Remove caracteres não numéricos
    cpf = ''.join(filter(str.isdigit, cpf))

    # Formata o CPF
    cpf_formatado = f'{cpf[:3]}.{cpf[3:6]}.{cpf[6:9]}-{cpf[9:]}'

    return cpf_formatado
#& Funcção atribuida ao botao F1
def funcaoF1(event):
    cadArquivo()
#& Funcção atribuida ao botao F2
def funcaoF2(event):
    exportar_tabelas_sqlite_para_excel()


#~ CODE
def AbrirCadastro(janela_login):
        
    #* Janela de Cadastro
    
    #TODO // BASES abrircadastro 
    janela_cadastro = tk.Toplevel(janela_login)#& cria a janela secundaria(pop-up) para cadastro herdando o tema da janela login
    janela_cadastro.configure(background="lightgrey")#& Edita o background da janela cadastro
    janela_cadastro.geometry("800x300")#& cria um tamanho fixo para a janela de cadastro comercial
    janela_cadastro.resizable(0,0) #& Bloqueia o redimensionamento da aplicação
    janela_cadastro.title('Cadastro Comercial') #& da o nome para a janela de cadastro comercial
    
    #? IMAGENS
    diretorio_script = os.path.dirname(os.path.realpath(__file__))
    janela_cadastro.iconbitmap(os.path.join(diretorio_script, 'Assets', 'icon.ico')) #& icone da janela de cadastro
    
    #^FONTES
    fonte_negrito2entry = font.Font(family="Helvetica", size=13) #& fonte 13 para as entrys
    fonte_negrito2 = font.Font(family="Helvetica", size=16) #& fonte 16 para as labels

    
    #TODO //  ENTRYS Cadastrar Empresa
    entry_cad_cnpj = ttk.Entry(janela_cadastro,font=fonte_negrito2entry)#& label usando font editada
    entry_cad_cnpj.place(x=230,y=60,width=500,height=40) #& configura a entry
    
    entry_cad_senha = ttk.Entry(janela_cadastro,font=fonte_negrito2entry,show="*")#& label usando font editada
    entry_cad_senha.place(x=230,y=110,width=500,height=40) #& configura a entry
    
    
    #TODO //  LABELS Cadastrar Empresa
    label_cad_cnpj = ttk.Label(janela_cadastro,text="CNPJ : ",font=fonte_negrito2)#& label usando font editada
    label_cad_cnpj.configure(background="lightgrey")#& configura a label
    label_cad_cnpj.place(x=133,y=65)#& configura a label
    
    label_cad_senha = ttk.Label(janela_cadastro,text="Senha : ",font=fonte_negrito2)#& label usando font editada
    label_cad_senha.configure(background="lightgrey")#& configura a label
    label_cad_senha.place(x=128,y=115)#& configura a label
    
    def cadastrar(): #! !!!ATENÇÃO!!! EDITAR PARA A FUNÇÃO DESEJADA POREM APROVEITE O DESTROY()
        cnpj = entry_cad_cnpj.get()
        senha = entry_cad_senha.get()
        if valida_cnpj(cnpj) == False:
            messagebox.showerror("ERRO","Por favor digite o CNPJ corretamente!")
        else:
            if len(cnpj) == 14:
                cnpj = formata_cnpj(cnpj) 
            if len(senha) == 0:
                messagebox.showerror("ERRO","O campo senha não pode ficar vazio!")
            else:
                bd = sqlite3.connect('SOD_DB.db')
                cursor = bd.cursor()
                cursor.execute("""INSERT INTO login(user,senha) VALUES (?,?) """,(cnpj,senha))
                bd.commit()
                bd.close()
                messagebox.showinfo("sucesso","Cadastro realizado com sucesso!")    
        janela_cadastro.destroy() #& Fecha a tela de cadastro


    #TODO //  BUTTONS Cadastrar Empresa
    button_cadastrar = ttk.Button(janela_cadastro, text="Cadastrar Empresa",style="MeuBotao.TButton",command=cadastrar) #& botão cadastrar
    button_cadastrar.place(x=230, y=180,width=450,height=70) #& Configura o botão

    janela_cadastro.mainloop()


#~###################################################################################################

def tela_de_login():
    
    def abrir_tela_principal():  #! !!!ATENÇÃO!!! EDITAR ESSA FUNÇÃO PARA TER VERIFICAÇÃO PARA O LOGIN
        janela_login.destroy() #& fecha a tela de login
        tela_principal() #& abre a tela inicial
    
    #* Janela de Login
    
    #TODO // BASES Janela de login  
    janela_login = ThemedTk(theme="clam") #& cria a tela de login e da um tema para ela
    janela_login.title("Tela de Login")#& da o nome para a tela de  login
    janela_login.resizable(0,0) #& bloqueia o redimensionamento de janela
    
    #^ FONTES
    fonte_negrito_login = font.Font(family='Arial Black', size=10) #& cria uma font para ser usada nos estilos das labels cnpj e senha
    
    #? IMAGENS
    diretorio_script = os.path.dirname(os.path.realpath(__file__))
    img = tk.PhotoImage(file = os.path.join(diretorio_script, 'Assets', 'tela-login.png')) #& imagem de fundo (background) da pagina login
    limg = tk.Label(janela_login, i=img) #& insere a imagem em uma label para ser inserida dentro da janela login
    limg.grid(row=5, column=2) #& configura a imagem de fundo
    janela_login.iconbitmap(os.path.join(diretorio_script, 'Assets', 'icon.ico')) #& icone da janela login
    
    #TODO //  ENTRYS | TELA DE LOGIN    
    entry_cnpj = ttk.Entry(janela_login) #& entry cnpj
    entry_cnpj.place(x = 113,y = 280, width=200,height=30) #& configura a entry
    
    entry_senha = ttk.Entry(janela_login,show="*") #& entry senha
    entry_senha.place(x = 113,y = 360,width=200,height=30) #& configura a entry
    
    #TODO //  LABELS | TELA DE LOGIN      
    label_cnpj = ttk.Label(janela_login,text="INSIRA SEU CNPJ",background="blue") #& label cnpj
    label_cnpj.place(x = 145,y = 250) #& Configura a label
    label_cnpj.configure(font=fonte_negrito_login,foreground="White",background="dodgerblue2")#&  Estiliza a label cnpj
    
    label_senha = ttk.Label(janela_login,text="INSIRA SUA SENHA") #& label senha
    label_senha.place(x = 140,y = 330) #& Configura a label
    label_senha.configure(font=fonte_negrito_login,foreground="White",background="dodgerblue2") #& Estiliza a label senha

    def abrir_tela_principal():  #! !!!ATENÇÃO!!! EDITAR ESSA FUNÇÃO PARA TER VERIFICAÇÃO PARA O LOGIN
        cnpj = entry_cnpj.get()
        senha = entry_senha.get()
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        cursor.execute("""SELECT user FROM login """)
        verificaCnpj = [item[0] for item in cursor.fetchall()]
        if cnpj not in verificaCnpj:
            messagebox.showerror("ERRO","CNPJ invalido!")
        else:
            cursor.execute(""" SELECT senha FROM login WHERE user = ?""",(cnpj,))
            verificasenha = [item[0] for item in cursor.fetchall()]
            if senha not in verificasenha:
                messagebox.showerror("ERRO","Senha incorreta!")
            else:
                janela_login.destroy() #& fecha a tela de login
                #tela_info() #& abre a tela inicial
                tela_principal()
        bd.close()
        

    def valida_se_Tem_login():
        cnpj = entry_cnpj.get()
        senha = entry_senha.get()
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        cursor.execute("""SELECT user FROM login """)
        verificaCnpj = [item[0] for item in cursor.fetchall()]
        if len(verificaCnpj) == 0:
            AbrirCadastro(janela_login)
        else:    
            if cnpj not in verificaCnpj:
                messagebox.showerror("ERRO","CNPJ invalido!")
            else:
                cursor.execute(""" SELECT senha FROM login WHERE user = ?""",(cnpj,))
                verificasenha = [item[0] for item in cursor.fetchall()]
                if senha not in verificasenha:
                    messagebox.showerror("ERRO","Senha incorreta!")
                else:
                    AbrirCadastro(janela_login)
            bd.close()
    
    #TODO //  BUTTONS | TELA DE LOGIN      
    botao_login = ttk.Button(janela_login, text="Login",command=abrir_tela_principal) #& botão login
    botao_login.place(x = 220,y = 420) #& Configura o botão login
    
    botao_cadastro = ttk.Button(janela_login, text="Registrar",command= valida_se_Tem_login) #& botão cadastro
    botao_cadastro.place(x = 120,y = 420) #& Configura o botão cadastro
    
    
    janela_login.mainloop()
    
    
#~###################################################################################################
def tela_info():
    janela_principal = ThemedTk(theme="adapta")  # cria a janela principal e dá um tema para ela
    janela_principal.title("SoD Solutions")  # dá o nome para a janela principal
    janela_principal.geometry('500x700')  # cria um tamanho fixo para a janela principal
    janela_principal.resizable(0, 0)  # Bloqueia o redimensionamento da aplicação

    fonte_negrito = ("Arial", 12, "bold")  # exemplo de definição de uma fonte negrito

    label_ver_cpf = ttk.Label(janela_principal, text="Teste:", font=fonte_negrito)  # label usando font editada
    label_ver_cpf.place(x=258, y=45)  # configura a label

    janela_principal.mainloop()

def tela_principal():
    messagebox.showinfo("SOBRE","Antes de usar os sitema aqui uma breve explicação de como usar.\nToda aba tem uma sub aba chamada de 'cadastro', onde fazemos a alimentação das tabelas.\nSe quiser importar os dados atraves de um arquivo XLSX é so apertar 'F1'\n Se quiser exportar os dados do sistema para um arquivo XLSX aperte 'F2'.\nE neste link '' um video sobre como usar o sistema.")
    #& Funcção que atualiza as tabelas do frontend
    def atualizar_tabelas():
        atualizar_tabela_SOD()
        atualizar_tabela_de_perfis()
        atualizar_tabela_de_sistemas()
        atualizar_tabela_de_usuarios()
        atualizar_tabela_perfil_usuarios()
    
    #* janela principal
    
    #TODO // BASES JANELA PRINCIPAL
    janela_principal = ThemedTk(theme="adapta") #& cria a janela principal e da um tema para ela
    janela_principal.title("SoD Solutions") #& da o nome para a janela principal
    janela_principal.geometry('1000x700') #& cria um tamanho fixo para a janela principal
    janela_principal.resizable(0,0) #& Bloqueia o redimensionamento da aplicação
    
    #? IMAGENS
    #janela_principal.iconbitmap("venv/Grupo Faculdade/Assets/icon.ico") #& icone da janela
    
    #TODO // NOTEBOOKS MAINs
    #* Cria um Notebook (abas)
    notebook = ttk.Notebook(janela_principal) #& Cria uma notebook main
    notebook.place(x=0, y=0, width=1000, height=700) #& da uma proporção para as notebooks
    
    #* Aba (1)
    aba_sistemas = ttk.Frame(notebook)#& Cria uma notebook dentro da main para receber as sub abas
    notebook.add(aba_sistemas, text="Sistemas") #& adiciona a aba dentro da main e da um nome
    
    #* Aba (2)
    aba_perfis = ttk.Frame(notebook)#& Cria uma notebook dentro da main para receber as sub abas
    notebook.add(aba_perfis, text="Perfis") #& adiciona a aba dentro da main e da um nome
    
    #* Aba (3)
    aba_users = ttk.Frame(notebook)#& Cria uma notebook dentro da main para receber as sub abas
    notebook.add(aba_users, text="Usuários") #& adiciona a aba dentro da main e da um nome
    
    #* Aba (4)
    aba_msod = ttk.Frame(notebook)#& Cria uma notebook dentro da main para receber as sub abas
    notebook.add(aba_msod, text="M.SoD") #& adiciona a aba dentro da main e da um nome
    
    #^ FONTES
    fonte_negrito = font.Font(family="Helvetica", size=12, weight="bold") #& cria uma fonte negrito tamanho 12
    fonte_negrito2 = font.Font(family="Helvetica", size=16, weight="bold") #& cria uma fonte negrito tamanho 16
    fonte_negrito2entry = font.Font(family="Helvetica", size=13) #& cria uma fonte para dentro das entrys
    
    
    estilo = ttk.Style() #& Abrindo o .Style
    estilo.configure("MeuBotao.TButton", font=fonte_negrito2entry,background="grey") #& Configurando uma "Familia" de botões (style)
            
    #~###################################################################################################
    #! >>>>> [1] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 1 (SISTEMAS)
    #*Sub Abas (1) SISTEMAS Sistemas Cadastrados
    
    #TODO //  BASES DO NOTEBOOK sistemas | Sistemas Cadastrados (1)
    sub_aba_sistemas = ttk.Notebook(aba_sistemas)#& Cria um notebook
    sub_aba_sistemas.place(x=0, y=0, width=1000, height=700)#& Configura a proporção da notebook
        
    sub_aba_sistemas_ver = ttk.Frame(sub_aba_sistemas) #& Criação da nova aba
    sub_aba_sistemas.add(sub_aba_sistemas_ver, text="Sistemas Cadastrados") #& adicionando a aba nova na aba principal e dando um nome
    
    #TODO //  ENTRYS sistemas | Sistemas Cadastrados (1) 
    entry_sistemas_ver_codigo = ttk.Entry(sub_aba_sistemas_ver) #& Cria uma Entry codigo
    entry_sistemas_ver_codigo.place(x=330,y=40,width=500) #& configura a entry
    
    entry_sistemas_ver_nome = ttk.Entry(sub_aba_sistemas_ver) #& Cria uma Entry nome
    entry_sistemas_ver_nome.place(x=330,y=80,width=500) #& configura a entry
    
    #TODO //  LABELS sistemas | Sistemas Cadastrados (1) 
    label_ver_cpf = ttk.Label(sub_aba_sistemas_ver,text="Código : ",font=fonte_negrito)#& label usando font editada
    label_ver_cpf.place(x=258,y=45)#& configura a label
    
    label_ver_nome = ttk.Label(sub_aba_sistemas_ver,text="Nome : ",font=fonte_negrito)#& label usando font editada
    label_ver_nome.place(x=265,y=85)#& configura a label

    label_info_S1 = ttk.Label(sub_aba_sistemas_ver,text="(F1) para importar um documento xlsx ou (F2) para exportar dados para um arquivo xlsx. \n(F5) para atualizar as tabelas",font=fonte_negrito)#& label usando font editada
    label_info_S1.place(x=200, y=596)#& configura a label
    
    #TODO // Lista (TREE) Sistemas (1)
    list_sistemas_ver = ttk.Treeview(sub_aba_sistemas_ver, columns=("Nome"))#& Cria as Colunas
    list_sistemas_ver.heading("#0", text="Código")#& Nomeia uma Coluna
    list_sistemas_ver.heading("#1", text="Nome")#& Nomeia uma Coluna
    list_sistemas_ver.place(x=130,y=200,width=800,height=400)#& Configura as Colunas
    
    #Conecta no banco de dados e alimenta a tabela.
    def atualizar_tabela_de_sistemas():
        list_sistemas_ver.delete(*list_sistemas_ver.get_children())
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        itens = cursor.execute("""
                SELECT * FROM sistemas 
        """)

        for item in itens:
            x = list_sistemas_ver.insert("","end",text=item[0],values=(item[1],item[0], item[2])) #& Lista ficticia
        bd.close()
        entry_sistemas_ver_codigo.delete(0, END)
        entry_sistemas_ver_nome.delete(0, END)
    atualizar_tabela_de_sistemas()
    
    #Seleciona o sistema da tabela dando dois cliques e mostra os valores nas ENTRYS.
    
    def selecionar_sistema(event):
        global id_interno
        selecionar_item = list_sistemas_ver.selection()
        for x in selecionar_item:
             nome, codigo, id = list_sistemas_ver.item(x,'values')
             entry_sistemas_ver_codigo.delete(0, END)
             entry_sistemas_ver_nome.delete(0, END)
             entry_sistemas_ver_codigo.insert(END, codigo)
             entry_sistemas_ver_nome.insert(END, nome)
             id_interno = id
    list_sistemas_ver.bind("<Double-1>", selecionar_sistema)
    
    #Deleta o item selecinado na tabela.
    def deletar_sistema():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()
            id = int(entry_sistemas_ver_codigo.get())
            cursor.execute("""DELETE FROM sistemas WHERE id = ?""", (id,))
            cursor.execute("""DELETE FROM perfil WHERE id_sistema = ?""", (id,))
            cursor.execute("""DELETE FROM MatrizSod WHERE id_sistema_1 = ? OR id_sistema_2 =? """, (id,id,))
            cursor.execute("""DELETE FROM perfil_usuarios WHERE id_sistema = ?""", (id,))
            bd.commit()
            bd.close()
            atualizar_tabelas()
        except ValueError:
            messagebox.showerror("Erro","Por favor digite um código válido, ou selecione um item clicando duas vezes na tabela!")
        except:
            messagebox.showerror("Erro","Algum erro inesperado aconteceu!")
            
    #TODO //  BUTTONS sistemas | Sistemas Cadastrados  (1)
    
    button_excluir_sistemas = ttk.Button(sub_aba_sistemas_ver, text="Excluir",style="MeuBotao.TButton", command= deletar_sistema) #& botão com style
    button_excluir_sistemas.place(x=15, y=590) #& configura o botão


    #~###################################################################################################
    #! >>>>> [2] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 1 (SISTEMAS)
    #*Sub Abas (1) SISTEMAS Perfis do Usuário
    
    #TODO //  BASES DO NOTEBOOK sistemas |  Perfis do Usuário (1)
    sub_aba_sistemas_ver_perfis = ttk.Frame(sub_aba_sistemas) #& Criação da nova aba
    sub_aba_sistemas.add(sub_aba_sistemas_ver_perfis, text="Perfis do Usuário")#& adicionando a aba nova na aba principal e dando um nome
    
    #TODO //  BUTTONS sistemas | Perfis do Usuário (1)
    #button_editar_sistemas_perfis = ttk.Button(sub_aba_sistemas_ver_perfis, text="Editar",style="MeuBotao.TButton") #& botão com style
    #button_editar_sistemas_perfis.place(x=15, y=540) #& configura o botão
    
    
    #TODO //  ENTRYS sistemas | Perfis do Usuário (1) 
    entry_sistemas_ver_codigo_perfis = ttk.Entry(sub_aba_sistemas_ver_perfis)#& Cria uma Entry codigo
    entry_sistemas_ver_codigo_perfis.place(x=330,y=40,width=500) #& configura a entry
    
    entry_sistemas_ver_cpf_perfis = ttk.Entry(sub_aba_sistemas_ver_perfis)#& Cria uma Entry cpf
    entry_sistemas_ver_cpf_perfis.place(x=330,y=80,width=500) #& configura a entry
    
    entry_sistemas_ver_nome_perfis = ttk.Entry(sub_aba_sistemas_ver_perfis)#& Cria uma Entry nome
    entry_sistemas_ver_nome_perfis.place(x=330,y=120,width=500) #& configura a entry
    
    #TODO //  LABELS sistemas | Perfis do Usuário (1) 
    label_ver_codigo_perfis = ttk.Label(sub_aba_sistemas_ver_perfis,text="Código do sistema : ",font=fonte_negrito)#& label usando font editada
    label_ver_codigo_perfis.place(x=165,y=45)#& configura a label
    
    label_ver_cpf_perfis = ttk.Label(sub_aba_sistemas_ver_perfis,text="CPF do Usuário : ",font=fonte_negrito)#& label usando font editada
    label_ver_cpf_perfis.place(x=185,y=85)#& configura a label
    
    label_ver_nome_perfis = ttk.Label(sub_aba_sistemas_ver_perfis,text="Nome do perfil : ",font=fonte_negrito)#& label usando font editada
    label_ver_nome_perfis.place(x=195,y=125)#& configura a label
    
    #TODO // Lista (TREE) Sistemas (1)
    list_sistemas_ver_perfis = ttk.Treeview(sub_aba_sistemas_ver_perfis, columns=("CPF","Nome",)) #& Cria as Colunas
    list_sistemas_ver_perfis.heading("#0", text="Código") #& Nomeia uma Coluna
    list_sistemas_ver_perfis.heading("#1", text="CPF") #& Nomeia uma Coluna
    list_sistemas_ver_perfis.heading("#2", text="Nome") #& Nomeia uma Coluna
    list_sistemas_ver_perfis.place(x=130,y=200,width=800,height=400)#& configura as Colunas
    
    def atualizar_tabela_perfil_usuarios():
        list_sistemas_ver_perfis.delete(*list_sistemas_ver_perfis.get_children())
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        itens = cursor.execute("""
                SELECT * FROM perfil_usuarios 
        """)

        for item in itens:
            x = list_sistemas_ver_perfis.insert("","end",text=item[0],values=(item[2],item[1],item[0])) #& Lista ficticia
        bd.close()
        entry_sistemas_ver_codigo_perfis.delete(0, END)
        entry_sistemas_ver_cpf_perfis.delete(0, END)
        entry_sistemas_ver_nome_perfis.delete(0, END)
    atualizar_tabela_perfil_usuarios()
    
    def selecionar_perfil_usuario(event):
        selecionar_item = list_sistemas_ver_perfis.selection()
        for x in selecionar_item:
             cpf, nome, codigo = list_sistemas_ver_perfis.item(x,'values')
             entry_sistemas_ver_codigo_perfis.delete(0, END)
             entry_sistemas_ver_cpf_perfis.delete(0, END)
             entry_sistemas_ver_nome_perfis.delete(0, END)
             entry_sistemas_ver_codigo_perfis.insert(END, codigo)
             entry_sistemas_ver_cpf_perfis.insert(END, cpf)
             entry_sistemas_ver_nome_perfis.insert(END, nome)
    list_sistemas_ver_perfis.bind("<Double-1>", selecionar_perfil_usuario)
    
    def deletar_perfil_usuario():
            try:
                bd = sqlite3.connect('SOD_DB.db')
                cursor = bd.cursor()
                nome = entry_sistemas_ver_nome_perfis.get()
                id = int(entry_sistemas_ver_codigo_perfis.get())
                cursor.execute("""DELETE FROM perfil_usuarios WHERE nome = ? AND id_sistema = ?""", (nome,id,))
                bd.commit()
                bd.close()
                atualizar_tabelas()
            except:
                messagebox.showerror("Erro","Algum erro inesperado aconteceu!")

    button_excluir_sistemas_perfis = ttk.Button(sub_aba_sistemas_ver_perfis, text="Excluir",style="MeuBotao.TButton", command= deletar_perfil_usuario) #& botão com style
    button_excluir_sistemas_perfis.place(x=15, y=590) #& configura o botão

    #~###################################################################################################
    #! >>>>> [3] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 1 (SISTEMAS)
    #*Sub Abas (1) SISTEMAS cadastrar sistemas
    
    #TODO //  BASES DO NOTEBOOK sistemas | cadastrar sistemas (1) 
    sub_cad_sistemas = ttk.Frame(sub_aba_sistemas) #& Criação da nova aba
    sub_aba_sistemas.add(sub_cad_sistemas, text="Cadastrar Sistemas") #& adicionando a aba nova na aba principal e dando um nome
    
    #TODO //  ENTRYS sistemas | cadastrar sistemas (1) 
    entry_cad_sistemas_codigo = ttk.Entry(sub_cad_sistemas,font=fonte_negrito2entry) #& Cria uma Entry codigo 
    entry_cad_sistemas_codigo.place(x=330,y=80,width=500,height=40) #& configura a entry 
    
    entry_cad_sistemas_nome = ttk.Entry(sub_cad_sistemas,font=fonte_negrito2entry) #& Cria uma Entry nome
    entry_cad_sistemas_nome.place(x=330,y=130,width=500,height=40) #& configura a entry
    
    #TODO //  LABELS sistemas | cadastrar sistemas (1) 
    label_cad_sistem_codigo = ttk.Label(sub_cad_sistemas,text="Código : ",font=fonte_negrito2)#& label usando font editada
    label_cad_sistem_codigo.place(x=233,y=85)#& configura a label
    
    label_cad_sistem_nome = ttk.Label(sub_cad_sistemas,text="Nome : ",font=fonte_negrito2)#& label usando font editada
    label_cad_sistem_nome.place(x=244,y=135)#& configura a label


    #Perpetua o sistema no banco de dados.
    def cadSistema():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()

            codigo = entry_cad_sistemas_codigo.get()
            nome = entry_cad_sistemas_nome.get()
            if len(nome) == 0:
                messagebox.showerror("Erro","O campo (nome) não pode ser vazio.")
            elif len(codigo) == 0:
                messagebox.showerror("Erro","O campo (codigo) não pode ser vazio.")
            else:
                cursor.execute("""
                                INSERT INTO sistemas(id,nome)
                                VALUES (?,?)
                                
                """, (int(codigo),nome))
                bd.commit()
            bd.close()
            entry_cad_sistemas_codigo.delete(0, END)
            entry_cad_sistemas_nome.delete(0, END)
            atualizar_tabelas()
        except ValueError:
            messagebox.showerror("Erro","Por favor digiteo código válido!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro","Este código já esta cadastrado!")


    #TODO //  BUTTONS sistemas | cadastrar sistemas  (1)
    button_cadastrar_sistemas = ttk.Button(sub_cad_sistemas, text="Cadastrar",style="MeuBotao.TButton", command = cadSistema) #& botão com style
    button_cadastrar_sistemas.place(x=330, y=250,width=450,height=70) #& configura o botão
    
    #~###################################################################################################
    #! >>>>> [1] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 2 (PERFIS)
    #*Sub Abas (2) PERFIS Perfis Cadastrados
    
    #TODO //  BASES DO NOTEBOOK perfis (2) Perfis Cadastrados
    sub_aba_perfis = ttk.Notebook(aba_perfis)#& cria um notebook
    sub_aba_perfis.place(x=0, y=0, width=1000, height=700)#& Configura a proporção da notebook
        
    sub_aba_perfis_ver = ttk.Frame(sub_aba_perfis)#& Criação da nova aba
    sub_aba_perfis.add(sub_aba_perfis_ver, text="Perfis Cadastrados")#& adicionando a aba nova na aba principal e dando um nome
    
    
    #TODO //  ENTRYS perfis (2) Perfis Cadastrados
    entry__ver_perfis_codigo = ttk.Entry(sub_aba_perfis_ver) #& Cria uma Entry nome
    entry__ver_perfis_codigo.place(x=330,y=40,width=500) #& configura a entry
    
    entry__ver_perfis_nome = ttk.Entry(sub_aba_perfis_ver) #& Cria uma Entry cpf
    entry__ver_perfis_nome.place(x=330,y=80,width=500) #& configura a entry
    
    entry__ver_perfis_desc = ttk.Entry(sub_aba_perfis_ver) #& Cria uma Entry descrição
    entry__ver_perfis_desc.place(x=330,y=120,width=500) #& configura a entry
    
    #TODO //  LABELS perfis (2) Perfis Cadastrados
    label_ver_perfis_codigo = ttk.Label(sub_aba_perfis_ver,text="Código do Sistema : ",font=fonte_negrito)#& label usando font editada
    label_ver_perfis_codigo.place(x=160,y=40)#& configura a label
    
    label_ver_perfis_nome = ttk.Label(sub_aba_perfis_ver,text="Nome do Perfil : ",font=fonte_negrito)#& label usando font editada
    label_ver_perfis_nome.place(x=191,y=80)#& configura a label
    
    label_ver_perfis_desc = ttk.Label(sub_aba_perfis_ver,text="Descrição : ",font=fonte_negrito)#& label usando font editada
    label_ver_perfis_desc.place(x=225,y=120)#& configura a label
    
    #TODO // Lista (TREE) perfis (2)
    list__perfis = ttk.Treeview(sub_aba_perfis_ver, columns=("Nome","Descrição",)) #& Cria as Colunas
    list__perfis.heading("#0", text="Código do sistema") #& Nomeia uma Coluna
    list__perfis.heading("#1", text="Nome do Perfil") #& Nomeia uma Coluna
    list__perfis.heading("#2", text="Descrição") #& Nomeia uma Coluna
    list__perfis.place(x=130,y=200,width=800,height=400) #& Configura as Colunas
    
    #Conecta no banco de dados e alimenta a tabela.
    def atualizar_tabela_de_perfis():
        list__perfis.delete(*list__perfis.get_children())
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        itens = cursor.execute("""
                SELECT * FROM perfil 
        """)

        for item in itens:
            x = list__perfis.insert("", "end", text=item[3], values=(item[1],item[2],item[3],item[0])) #& Lista ficticia
        bd.close()
        entry__ver_perfis_codigo.delete(0, END)
        entry__ver_perfis_nome.delete(0, END)
        entry__ver_perfis_desc.delete(0, END)
    atualizar_tabela_de_perfis()


    #Seleciona o sistema da tabela dando dois cliques e mostra os valores nas ENTRYS.
    
    def selecionar_perfil(event):
        global id_int_perfil
        selecionar_item = list__perfis.selection()
        for x in selecionar_item:
             nome, desc, id_sistema, id = list__perfis.item(x,'values')
             entry__ver_perfis_codigo.delete(0, END)
             entry__ver_perfis_nome.delete(0, END)
             entry__ver_perfis_desc.delete(0, END)
             entry__ver_perfis_codigo.insert(END, id_sistema)
             entry__ver_perfis_nome.insert(END, nome)
             entry__ver_perfis_desc.insert(END, desc)
             id_int_perfil = id
    list__perfis.bind("<Double-1>", selecionar_perfil)


    #Deleta o item selecinado na tabela.
    def deletar_perfil():
        global id_int_perfil
        if id_int_perfil == 0:
                messagebox.showerror("ERRO","Por favor selecione o item a ser excluido clicando 2x na tabela.")
        else:  
            try:
                bd = sqlite3.connect('SOD_DB.db')
                cursor = bd.cursor()
                nome = entry__ver_perfis_nome.get()
                id = id_int_perfil
                cursor.execute("""DELETE FROM perfil WHERE id = ?""", (id,))
                cursor.execute("""DELETE FROM MatrizSod WHERE nome_perfil_1 = ? AND nome_perfil_2 = ?""", (nome,nome))
                cursor.execute("""DELETE FROM perfil_usuarios WHERE nome = ?""", (nome,))
                bd.commit()
                bd.close()
                atualizar_tabelas()
            except ValueError:
                messagebox.showerror("Erro","Por favor digite um código válido, ou selecione um item clicando duas vezes na tabela!")
            except:
                messagebox.showerror("Erro","Algum erro inesperado aconteceu!")



    #TODO //  BUTTONS perfis (2) Perfis Cadastrados

    button_excluir_ver_perfis_ = ttk.Button(sub_aba_perfis_ver, text="Excluir",style="MeuBotao.TButton", command= deletar_perfil)#& botão com style
    button_excluir_ver_perfis_.place(x=15, y=590) #& configura o botão
    
    #~###################################################################################################
    #! >>>>> [2] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 2 (PERFIS) 
    #* Sub Abas (2) PERFIS Cadastro de Perfis
    
    #TODO //  BASES DO NOTEBOOK perfis (2) Cadastro de Perfis
    sub_aba_cad_perfis = ttk.Frame(sub_aba_perfis)#& Criação da nova aba
    sub_aba_perfis.add(sub_aba_cad_perfis, text="Cadastro de Perfil")#& adicionando a aba nova na aba principal e dando um nome
    
    
    #TODO //  ENTRYS perfis (2) Cadastro de Perfis
    entry_cad_perfis_codigo = ttk.Entry(sub_aba_cad_perfis,font=fonte_negrito2entry) #& Cria uma Entry nome
    entry_cad_perfis_codigo.place(x=330,y=80,width=500,height=40)#& configura a entry
    
    entry_cad_perfis_nome = ttk.Entry(sub_aba_cad_perfis,font=fonte_negrito2entry) #& Cria uma Entry codigo
    entry_cad_perfis_nome.place(x=330,y=130,width=500,height=40)#& configura a entry
    
    entry_cad_perfis_desc = ttk.Entry(sub_aba_cad_perfis,font=fonte_negrito2entry) #& Cria uma Entry descrição
    entry_cad_perfis_desc.place(x=330,y=180,width=500,height=40)#& configura a entry
    
    
    #TODO //  LABELS perfis (2) Cadastro de Perfis
    label_cad_perfis_nome = ttk.Label(sub_aba_cad_perfis,text="Código do Sistema",font=fonte_negrito2)#& label usando font editada
    label_cad_perfis_nome.place(x=125,y=85)#& configura a label
    
    label_cad_perfis_cpf = ttk.Label(sub_aba_cad_perfis,text="Nome do Perfil",font=fonte_negrito2)#& label usando font editada
    label_cad_perfis_cpf.place(x=165,y=135)#& configura a label
    
    label_cad_perfis_desc = ttk.Label(sub_aba_cad_perfis,text="Descrição",font=fonte_negrito2)#& label usando font editada
    label_cad_perfis_desc.place(x=157,y=185)#& configura a label
    
    def cadPerfil():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()
            codSistema = entry_cad_perfis_codigo.get()
            nome = entry_cad_perfis_nome.get()
            descricao = entry_cad_perfis_desc.get()
            if len(nome) == 0:
                messagebox.showerror("Erro","O campo (nome) não pode ser vazio.")
            elif len(descricao) == 0:
                messagebox.showerror("Erro","O campo (descrição) não pode ser vazio.")
            elif len(codSistema) == 0:
                messagebox.showerror("Erro","O campo (codigo do sistema) não pode ser vazio.")
            else:
                codSistema = int(codSistema)
                cursor.execute("""
                        SELECT id FROM sistemas;
                """)
                codigosDosSitemas = [item[0] for item in cursor.fetchall()]
                if codSistema not in codigosDosSitemas:
                    messagebox.showerror("ERRO",f"O sitema ({codSistema}) não existe! Tente um código existente.")
                    bd.close()
                else:
                    cursor.execute("""
                            INSERT INTO perfil(nome,descricao,id_sistema)
                            VALUES (?,?,?)
                    """, (nome,descricao,codSistema))
                    bd.commit()
            bd.close()
            entry_cad_perfis_codigo.delete(0,END)
            entry_cad_perfis_nome.delete(0,END)
            entry_cad_perfis_desc.delete(0,END)
            atualizar_tabelas()
        except ValueError:
            messagebox.showerror("Erro","Por favor digite um código válido, ou selecione um item clicando duas vezes na tabela!")
        except:
            messagebox.showerror("Erro","Algum erro inesperado aconteceu!")


    #TODO //  BUTTONS perfis (2) Cadastro de Perfis
    button_cadastrar_perfis = ttk.Button(sub_aba_cad_perfis, text="Cadastrar Perfil",style="MeuBotao.TButton", command= cadPerfil)#& botão com style
    button_cadastrar_perfis.place(x=330, y=250,width=450,height=70)#& configura o botão



    #~###################################################################################################
    #! >>>>> [1] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 3 (USERS)   
    #* Sub Abas (3) USERS Usuarios Cadastrados 
    
    #TODO //  BASES DO NOTEBOOK users (3)
    sub_aba_users = ttk.Notebook(aba_users)#& Cria uma Notebook
    sub_aba_users.place(x=0, y=0, width=1000, height=700)#& Configura a proporção da notebook
        
    sub_aba_users_ver = ttk.Frame(sub_aba_users)#& Criação da nova aba
    sub_aba_users.add(sub_aba_users_ver, text="Usuários Cadastrados")#& adicionando a aba nova na aba principal e dando um nome
    
    
    #TODO //  ENTRYS users (3) 
    entry_ver_nome = ttk.Entry(sub_aba_users_ver) #& Cria uma Entry nome
    entry_ver_nome.place(x=330,y=40,width=500)#& configura a entry
    
    entry_ver_cpf = ttk.Entry(sub_aba_users_ver) #& Cria uma Entry cpf
    entry_ver_cpf.place(x=330,y=80,width=500)#& configura a entry
    
    entry_ver_desc = ttk.Entry(sub_aba_users_ver) #& Cria uma Entry descrição
    entry_ver_desc.place(x=330,y=120,width=500)#& configura a entry
    
    #TODO //  LABELS users (3) 
    label_ver_nome = ttk.Label(sub_aba_users_ver,text="Nome : ",font=fonte_negrito)#& label usando font editada
    label_ver_nome.place(x=263,y=45)#& configura a label
    
    label_ver_cpf = ttk.Label(sub_aba_users_ver,text="CPF : ",font=fonte_negrito)#& label usando font editada
    label_ver_cpf.place(x=274,y=85)#& configura a label
    
    label_ver_desc = ttk.Label(sub_aba_users_ver,text="Descrição : ",font=fonte_negrito)#& label usando font editada
    label_ver_desc.place(x=230,y=125)#& configura a label
    
    #TODO // Lista (TREE) users (3)
    list_ver = ttk.Treeview(sub_aba_users_ver, columns=("CPF", "Descrição"))#& cria as Colunas
    list_ver.heading("#0", text="Nome") #& Nomeia uma Coluna
    list_ver.heading("#1", text="CPF") #& Nomeia uma Coluna
    list_ver.heading("#2", text="Descrição") #& Nomeia uma Coluna
    list_ver.place(x=130,y=200,width=800,height=400) #& Configura as Coluna
    
    #Conecta no banco de dados e alimenta a tabela.
    def atualizar_tabela_de_usuarios():
        list_ver.delete(*list_ver.get_children())
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        itens = cursor.execute("""
                SELECT * FROM usuarios 
        """)

        for item in itens:
            x = list_ver.insert("","end",text=item[1],values=(item[2],item[3],item[1],item[0])) #& Lista ficticia
        bd.close()
        entry_ver_nome.delete(0, END)
        entry_ver_cpf.delete(0, END)
        entry_ver_desc.delete(0, END)
    atualizar_tabela_de_usuarios()

    #Seleciona o sistema da tabela dando dois cliques e mostra os valores nas ENTRYS.
    
    def selecionar_usuario(event):
        global id_int_user
        selecionar_item = list_ver.selection()
        for x in selecionar_item:
             cpf, desc,nome, id = list_ver.item(x,'values')
             entry_ver_nome.delete(0, END)
             entry_ver_cpf.delete(0, END)
             entry_ver_desc.delete(0, END)
             entry_ver_nome.insert(END, nome)
             entry_ver_cpf.insert(END, cpf)
             entry_ver_desc.insert(END, desc)
             id_int_user = id
    list_ver.bind("<Double-1>", selecionar_usuario)

    #Deleta o item selecinado na tabela.
    def deletar_usuario():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()
            cpf = entry_ver_cpf.get()
            cursor.execute("""DELETE FROM usuarios WHERE cpf = ?""", (cpf,))
            cursor.execute("""DELETE FROM perfil_usuarios WHERE cpf_usuario = ?""", (cpf,))
            bd.commit()
            bd.close()
            atualizar_tabelas()
        except:
            messagebox.showerror("Erro","Algum erro inesperado aconteceu!")

    #TODO //  BUTTONS users (3) 
    
    button_excluir = ttk.Button(sub_aba_users_ver, text="Excluir",style="MeuBotao.TButton", command= deletar_usuario)#& botão com style
    button_excluir.place(x=15, y=590)#& configura o botão
    
    #~###################################################################################################
    #! >>>>> [2] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 3 (USERS)   
    #* Sub Abas (3) USERS Cadastrar Usuarios
    
    #TODO //  BASES DO NOTEBOOK users (3)Cadastrar Usuarios
    sub_aba_cad_users_ver = ttk.Frame(sub_aba_users)#& Criação da nova aba
    sub_aba_users.add(sub_aba_cad_users_ver, text="Cadastrar Usuários") #& adicionando a aba nova na aba principal e dando um nome
    
    
    #TODO //  ENTRYS users (3) Cadastrar Usuarios
    entry_cad_nome = ttk.Entry(sub_aba_cad_users_ver,font=fonte_negrito2entry) #& Cria uma Entry nome
    entry_cad_nome.place(x=330,y=80,width=500,height=40)#& configura a entry
    
    entry_cad_cpf = ttk.Entry(sub_aba_cad_users_ver,font=fonte_negrito2entry) #& Cria uma Entry cpf
    entry_cad_cpf.place(x=330,y=130,width=500,height=40)#& configura a entry
    
    entry_cad_desc = ttk.Entry(sub_aba_cad_users_ver,font=fonte_negrito2entry) #& Cria uma Entry descrição
    entry_cad_desc.place(x=330,y=180,width=500,height=40)#& configura a entry
    
    #TODO //  LABELS users (3) Cadastrar Usuarios
    label_cad_nome = ttk.Label(sub_aba_cad_users_ver,text="Nome : ",font=fonte_negrito2)#& label usando font editada
    label_cad_nome.place(x=233,y=85)#& configura a label
    
    label_cad_cpf = ttk.Label(sub_aba_cad_users_ver,text="CPF : ",font=fonte_negrito2)#& label usando font editada
    label_cad_cpf.place(x=244,y=135)#& configura a label
    
    label_cad_desc = ttk.Label(sub_aba_cad_users_ver,text="Descrição : ",font=fonte_negrito2)#& label usando font editada
    label_cad_desc.place(x=200,y=185)#& configura a label

    def cadusuario():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()

            nome = entry_cad_nome.get()
            cpf = entry_cad_cpf.get()
            descricao = entry_cad_desc.get()
            if valida_cpf(cpf) == False:
                messagebox.showerror("ERRO","O cpf foi digitado errado. Por favor tente novamente")
            else:
                if len(cpf) == 11:
                    cpf = formata_cpf(cpf)
                if len(nome) == 0:
                        messagebox.showerror("Erro","O campo (nome) não pode ser vazio.")
                elif len(cpf) == 0:
                        messagebox.showerror("Erro","O campo (cpf) não pode ser vazio.")
                elif len(descricao) == 0:
                        messagebox.showerror("Erro","O campo (descrição) não pode ser vazio.")
                cursor.execute("""
                        SELECT cpf FROM usuarios;
                """)
                cpfExistente = [item[0] for item in cursor.fetchall()]
                if cpf in cpfExistente:
                    messagebox.showerror("ERRO",'O CPF ja existe no banco de dados!')
                else:
                    cursor.execute("""
                            INSERT INTO usuarios(nome,cpf,descricao)
                            VALUES (?,?,?)
                    """, (nome,cpf,descricao))
                    bd.commit()
                bd.close()
                entry_cad_nome.delete(0, END)
                entry_cad_cpf.delete(0, END)
                entry_cad_desc.delete(0, END)
                atualizar_tabelas()
        except ValueError:
            messagebox.showerror("Erro","Por favor digiteo código válido!")
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro","Este código já esta cadastrado!")

    #TODO //  BUTTONS users (3) Cadastrar Usuarios
    button_cadastrar = ttk.Button(sub_aba_cad_users_ver, text="Cadastrar Usuário",style="MeuBotao.TButton", command= cadusuario)#& botão com style
    button_cadastrar.place(x=330, y=250,width=450,height=70)#& configura o botão
    
    
    #~################################################################################################### 
    #! >>>>> [3] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 3 (USERS)   
    #* Sub Abas (3) USERS Cadastro de perfis do Usuario
    
    #TODO //  BASES DO NOTEBOOK users (3)Cadastro de perfis do Usuario
    sub_aba_cad_perfis_users = ttk.Frame(sub_aba_users) #& Criação da nova aba
    sub_aba_users.add(sub_aba_cad_perfis_users, text="Cadastro de Perfil do Usuário")#& adicionando a aba nova na aba principal e dando um nome
    
    
    #TODO //  ENTRYS users (3) Cadastro de perfis do Usuario
    entry_cad_perfis_user_cod = ttk.Entry(sub_aba_cad_perfis_users,font=fonte_negrito2entry) #& Cria uma Entry nome
    entry_cad_perfis_user_cod.place(x=330,y=80,width=500,height=40)#& configura a entry
    
    entry_cad_perfis_user_nome = ttk.Entry(sub_aba_cad_perfis_users,font=fonte_negrito2entry) #& Cria uma Entry cpf
    entry_cad_perfis_user_nome.place(x=330,y=130,width=500,height=40)#& configura a entry
    
    entry_cad_perfis_user_cpfperfil = ttk.Entry(sub_aba_cad_perfis_users,font=fonte_negrito2entry) #& Cria uma Entry descrição
    entry_cad_perfis_user_cpfperfil.place(x=330,y=180,width=500,height=40)#& configura a entry
    
    #TODO //  LABELS users (3) Cadastro de perfis do Usuario
    
    label_cad_perfis_nome = ttk.Label(sub_aba_cad_perfis_users,text="Código do Sistema",font=fonte_negrito2)#& label usando font editada
    label_cad_perfis_nome.place(x=125,y=85)#& configura a label
    
    label_cad_perfis_cpf = ttk.Label(sub_aba_cad_perfis_users,text="Nome do Perfil",font=fonte_negrito2)#& label usando font editada
    label_cad_perfis_cpf.place(x=165,y=135)#& configura a label
    
    label_cad_perfis_desc = ttk.Label(sub_aba_cad_perfis_users,text="CPF do Usuario",font=fonte_negrito2)#& label usando font editada
    label_cad_perfis_desc.place(x=157,y=185)#& configura a label
    
    def cadPerfildoUsuario():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()

            cpf = entry_cad_perfis_user_cpfperfil.get()
            if valida_cpf(cpf) == False:
                messagebox.showerror("ERRO","Por favor selecione o item a ser editado clicando 2x na tabela.")
            else:
                if len(cpf) == 11:
                    cpf = formata_cpf(cpf)
                cursor.execute("""
                                SELECT cpf FROM usuarios;
                        """)
                cpfExistente = [item[0] for item in cursor.fetchall()]
                if cpf not in cpfExistente:
                    messagebox.showerror("ERRO",'CPF não cadastrado')
                else:
                    idSistema = int(entry_cad_perfis_user_cod.get())
                    cursor.execute("""
                                        SELECT id FROM sistemas;
                                """)
                    sistemaExistente = [item[0] for item in cursor.fetchall()]
                    if idSistema not in sistemaExistente:
                        messagebox.showerror("ERRO",'Código do sistema não cadastrado')
                    else:
                        nomePerfil = entry_cad_perfis_user_nome.get()
                        cursor.execute("""
                                                    SELECT nome FROM perfil;
                                            """)
                        perfilExistente = [item[0] for item in cursor.fetchall()]
                        if nomePerfil not in perfilExistente:
                            messagebox.showerror("ERRO",'Perfil não cadastrado')
                        else:
                            cursor.execute("""
                                                        SELECT cpf_usuario FROM perfil_usuarios;
                                                """)
                            perfilExistente = [item[0] for item in cursor.fetchall()]
                            if cpf not in perfilExistente:
                                cursor.execute("""
                                        INSERT INTO perfil_usuarios(id_sistema,nome,cpf_usuario)
                                        VaLUES (?,?,?)
                                """, (idSistema,nomePerfil,cpf))
                                bd.commit()
                            else:
                                cursor.execute("""
                                    SELECT nome_perfil_1 FROM MatrizSod WHERE nome_perfil_2 = ? 
                                    UNION 
                                    SELECT nome_perfil_2 FROM MatrizSod WHERE nome_perfil_1 = ?;
                                """, (nomePerfil, nomePerfil))
                                perfilExistente = [item[0] for item in cursor.fetchall()]
                                cursor.execute("""
                                            SELECT nome FROM perfil_usuarios WHERE cpf_usuario = ?
                                """,(cpf,))
                                funcoesexistentesusuario = [item[0] for item in cursor.fetchall()]
                                divergente = 'nao'
                                funcoesDiv = []
                                for i in funcoesexistentesusuario:
                                    if i in perfilExistente:
                                        divergente = 'sim'
                                        funcoesDiv.append(i)
                                if divergente == 'nao':
                                    cursor.execute("""
                                            INSERT INTO perfil_usuarios(id_sistema,nome,cpf_usuario)
                                            VaLUES (?,?,?)
                                    """, (idSistema, nomePerfil, cpf))
                                    bd.commit()
                                else:
                                    messagebox.showerror("ERRO",f"O perfil ({nomePerfil}) conflita com o(os) perfil(S) {funcoesDiv}.")
                bd.close()
                atualizar_tabelas()
        except:
            messagebox.showerror("ERRO","Algo inesperado aconteceu!")
    #TODO //  BUTTONS users (3) Cadastro de perfis do Usuario
    button_cadastrar_perfis_user = ttk.Button(sub_aba_cad_perfis_users, text="Cadastrar Perfil",style="MeuBotao.TButton", command= cadPerfildoUsuario) #& botão com style
    button_cadastrar_perfis_user.place(x=330, y=250,width=450,height=70) #& configura o botão
    
    #~################################################################################################### 
    #! >>>>> [1] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 4 (MSOD)    
    #* Sub Abas (4) MSOD Consulta 
    
    #TODO //  BASES DO NOTEBOOK m.sod (4)
    sub_aba_msod = ttk.Notebook(aba_msod) #& Cria uma Notebook
    sub_aba_msod.place(x=0, y=0, width=1000, height=700) #& Configura a proporção da notebook
        
    sub_aba_msod_ver = ttk.Frame(sub_aba_msod) #& Criação da nova aba
    sub_aba_msod.add(sub_aba_msod_ver, text="Consulta de Matriz SoD") #& adicionando a aba nova na aba principal e dando um nome
    
    #TODO //  ENTRYS m.sod (4) 
    entry_msod1sistem = ttk.Entry(sub_aba_msod) #& Cria uma Entry msod 1 sistem
    entry_msod1sistem.place(x=330,y=40,width=500) #& configura a entry
    
    entry_msod1func = ttk.Entry(sub_aba_msod) #& Cria uma Entry msod 1 func
    entry_msod1func.place(x=330,y=80,width=500) #& configura a entry
    
    entry_msod2sistem = ttk.Entry(sub_aba_msod) #& Cria uma Entry msod 2 sistem
    entry_msod2sistem.place(x=330,y=120,width=500) #& configura a entry
    
    entry_msod2func = ttk.Entry(sub_aba_msod) #& Cria uma Entry msod 2 func
    entry_msod2func.place(x=330,y=160,width=500) #& configura a entry
    
    #TODO //  LABELS m.sod (4) 
    label_msod1sistem = ttk.Label(sub_aba_msod,text="1° Código do Sistema : ",font=fonte_negrito)#& label usando font editada
    label_msod1sistem.place(x=136,y=40)#& configura a label
    
    label_msod1func = ttk.Label(sub_aba_msod,text="1° Nome do Perfil : ",font=fonte_negrito)#& label usando font editada
    label_msod1func.place(x=170,y=80)#& configura a label
    
    label_msod2sistem = ttk.Label(sub_aba_msod,text="2° Código do Sistema : ",font=fonte_negrito)#& label usando font editada
    label_msod2sistem.place(x=136,y=120)#& configura a label

    label_msod2func = ttk.Label(sub_aba_msod,text="2° Nome do Perfil : ",font=fonte_negrito)#& label usando font editada
    label_msod2func.place(x=170,y=160)#& configura a label
    
    
    #TODO // TREES m.sod (4)
    list_msod = ttk.Treeview(sub_aba_msod, columns=("Cod.1° Função", "Cod.2° Sistema", "Cod.2° Função")) #& Cria as Colunas
    list_msod.heading("#0", text="Cod.1° Sistema") #& Nomeia uma Coluna
    list_msod.heading("#1", text="Cod.1° Função") #& Nomeia uma Coluna
    list_msod.heading("#2", text="Cod.2° Sistema") #& Nomeia uma Coluna
    list_msod.heading("#3", text="Cod.2° Função") #& Nomeia uma Coluna
    list_msod.place(x=130,y=200,width=800,height=400) #& Configura as Trees
    
    #Conecta no banco de dados e alimenta a tabela.
    def atualizar_tabela_SOD():
        list_msod.delete(*list_msod.get_children())
        bd = sqlite3.connect('SOD_DB.db')
        cursor = bd.cursor()
        itens = cursor.execute("""
                SELECT * FROM MatrizSod 
        """)

        for item in itens:
            x = list_msod.insert("","end",text=item[1],values=(item[2],item[3], item[4],item[1],item[0])) #& Lista ficticia
        bd.close()
        entry_msod1sistem.delete(0, END)
        entry_msod1func.delete(0, END)
        entry_msod2sistem.delete(0, END)
        entry_msod2func.delete(0, END)
    atualizar_tabela_SOD()

    #Seleciona o sistema da tabela dando dois cliques e mostra os valores nas ENTRYS.
    
    def selecionar_sod(event):
        global id_int_sod
        selecionar_item = list_msod.selection()
        for x in selecionar_item:
             pf1, cod2, pf2, cod1, id = list_msod.item(x,'values')
             entry_msod1sistem.delete(0, END)
             entry_msod1func.delete(0, END)
             entry_msod2sistem.delete(0, END)
             entry_msod2func.delete(0, END)
             entry_msod1sistem.insert(END, cod1)
             entry_msod1func.insert(END, pf1)
             entry_msod2sistem.insert(END, cod2)
             entry_msod2func.insert(END, pf2)
             id_int_sod = id
    list_msod.bind("<Double-1>", selecionar_sod)
    
    #Deleta o item selecinado na tabela.
    def deletar_sod():
        global id_int_sod
        if id_int_sod == 0:
                messagebox.showerror("ERRO","Por favor selecione o item a ser excluido clicando 2x na tabela.")
        else:
            try:
                bd = sqlite3.connect('SOD_DB.db')
                cursor = bd.cursor()
                id = int(id_int_sod)
                cursor.execute("""DELETE FROM MatrizSod WHERE id = ?""", (id,))
                bd.commit()
                bd.close()
                atualizar_tabelas()
            except ValueError:
                messagebox.showerror("Erro","Por favor digite um código válido, ou selecione um item clicando duas vezes na tabela!")
            except:
                messagebox.showerror("Erro","Algum erro inesperado aconteceu!")


    #TODO //  BUTTONS m.sod (4) 
    
    button_msodexc = ttk.Button(sub_aba_msod, text="Excluir",style="MeuBotao.TButton", command= deletar_sod)#& botão com style
    button_msodexc.place(x=15, y=590) #& configura o botão


    #~################################################################################################### 
    #! >>>>> [2] <<<<<  MARCA O NUMERO DA ABA DENTRO DAS SUB ABAS 4 (MSOD)
    #* Sub Abas (4) MSOD cadastro 
    
    #TODO //  BASES DO NOTEBOOK m.sod (4) cadastro
    sub_aba_msod_cad = ttk.Frame(sub_aba_msod)#& Criação da nova aba
    sub_aba_msod.add(sub_aba_msod_cad, text="Cadastro de Matriz SoD")#& adicionando a aba nova na aba principal e dando um nome
    
    #TODO //  ENTRYS m.sod (4) cadastro
    entry_cad_msod1sistem = ttk.Entry(sub_aba_msod_cad)#& Entry msod sistem 1
    entry_cad_msod1sistem.place(x=330,y=40,width=500)#& configura a entry
    
    entry_cad_msod1func = ttk.Entry(sub_aba_msod_cad)#& Entry msod func 1
    entry_cad_msod1func.place(x=330,y=80,width=500)#& configura a entry
    
    entry_cad_msod2sistem = ttk.Entry(sub_aba_msod_cad)#& Entry msod sistem 2
    entry_cad_msod2sistem.place(x=330,y=120,width=500)#& configura a entry
    
    entry_cad_msod2func = ttk.Entry(sub_aba_msod_cad)#& Entry msod func 2
    entry_cad_msod2func.place(x=330,y=160,width=500)#& configura a entry
    
    #TODO //  LABELS m.sod (4) cadastro
    label_cad_msod1sistem = ttk.Label(sub_aba_msod_cad,text="1° Código do Sistema : ",font=fonte_negrito)#& label usando font editada
    label_cad_msod1sistem.place(x=136,y=40)#& configura a label
    
    label_cad_msod1func = ttk.Label(sub_aba_msod_cad,text="1° Nome do Perfil : ",font=fonte_negrito)#& label usando font editada
    label_cad_msod1func.place(x=170,y=80)#& configura a label
    
    label_cad_msod2sistem = ttk.Label(sub_aba_msod_cad,text="2° Código do Sistema : ",font=fonte_negrito)#& label usando font editada
    label_cad_msod2sistem.place(x=136,y=120)#& configura a label

    label_cad_msod2func = ttk.Label(sub_aba_msod_cad,text="2° Nome do Perfil : ",font=fonte_negrito) #& label usando font editada
    label_cad_msod2func.place(x=170,y=160) #& configura a label
    
    def cadMatrizSod():
        try:
            bd = sqlite3.connect('SOD_DB.db')
            cursor = bd.cursor()
            codSistema1 = int(entry_cad_msod1sistem.get())
            codPerfil1 = entry_cad_msod1func.get()
            codSistema2 = int(entry_cad_msod2sistem.get())
            codPerfil2 = entry_cad_msod2func.get()

            cursor.execute("""
                    SELECT id FROM sistemas;
            """)
            idDositema = [item[0] for item in cursor.fetchall()]

            if codSistema1 not in idDositema: 
                messagebox.showerror("Erro",f"O sistema ({codSistema1}) não existe!")
            elif codSistema2 not in idDositema:
                messagebox.showerror("Erro",f"O sistema ({codSistema2}) não existe!")
            else:
                cursor.execute("""
                            SELECT nome FROM perfil;
                    """)
                nomeperfil = [item[0] for item in cursor.fetchall()]
                if codPerfil1 not in nomeperfil:
                    messagebox.showerror("Erro",f"O perfil ({codPerfil1}) não existe!")
                elif codPerfil2 not in nomeperfil:
                    messagebox.showerror("Erro",f"O perfil ({codPerfil2}) não existe!")
                else:
                    cursor.execute("""
                            INSERT INTO MatrizSod(id_sistema_1,nome_perfil_1,id_sistema_2,nome_perfil_2)
                            VALUES (?,?,?,?)
                    """, (codSistema1,codPerfil1,codSistema2,codPerfil2))
                    bd.commit()
                    entry_cad_msod1sistem.delete(0, END)
                    entry_cad_msod1func.delete(0, END)
                    entry_cad_msod2sistem.delete(0, END)
                    entry_cad_msod2func.delete(0, END)
                    atualizar_tabelas()
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro","Este código já esta cadastrado!")
            
    #TODO // BUTTONS m.sod (4) cadastro
    button_cadastrar_msod = ttk.Button(sub_aba_msod_cad, text="Cadastrar Matriz",style="MeuBotao.TButton", command= cadMatrizSod) #& botão com style
    button_cadastrar_msod.place(x=330, y=250,width=450,height=70) #& Configura o botão
    def funcaoF5(event):
        atualizar_tabelas()
    janela_principal.bind('<F5>', funcaoF5)
    janela_principal.bind('<F1>', funcaoF1)
    janela_principal.bind('<F2>', funcaoF2)
    janela_principal.mainloop() #& mantendo a janela principal aberta
    
#~ END CODE

tela_de_login() #& chamada de função
#tela_principal()