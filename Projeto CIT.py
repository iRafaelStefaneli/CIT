import customtkinter as ctk
import customtkinter
from customtkinter import *
from customtkinter import CTkFrame
from tkinter import messagebox, PhotoImage
import tkinter as tk
from PIL import Image
import requests
import json

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Paleta de cores baseada no laranja e marrom
COR_LARANJA = "#E87109"
COR_MARROM = "#4B2C0A"
COR_LARANJA_CLARO = "#F9A826"
COR_MARROM_CLARO = "#6D4C41"
COR_FUNDO = "#F5F5F5"
COR_TEXTO = "#333333"
COR_BRANCO = "#FFFFFF"
COR_CINZA = "#E0E0E0"

# Funções auxiliares para styling
def criar_botao_estilizado(parent, texto, comando, cor_principal=COR_LARANJA, largura=200, altura=40):
    return ctk.CTkButton(
        parent,
        text=texto,
        command=comando,
        fg_color=cor_principal,
        hover_color=COR_MARROM,
        text_color=COR_BRANCO,
        font=("Arial", 16, "bold"),
        width=largura,
        height=altura,
        corner_radius=10
    )

def criar_label_estilizado(parent, texto, tamanho_fonte=16, cor_texto=COR_TEXTO, negrito=False):
    fonte = ("Arial", tamanho_fonte, "bold") if negrito else ("Arial", tamanho_fonte)
    return ctk.CTkLabel(
        parent,
        text=texto,
        text_color=cor_texto,
        font=fonte
    )

def criar_entry_estilizado(parent, largura=300, altura=40, mostrar_texto=False):
    return ctk.CTkEntry(
        parent,
        width=largura,
        height=altura,
        fg_color=COR_BRANCO,
        border_color=COR_LARANJA,
        text_color=COR_TEXTO,
        font=("Arial", 14),
        show="*" if mostrar_texto else ""
    )

def criar_frame_estilizado(parent, largura, altura, cor_fundo=COR_FUNDO, com_borda=True):
    return ctk.CTkFrame(
        parent,
        width=largura,
        height=altura,
        fg_color=cor_fundo,
        border_color=COR_LARANJA if com_borda else None,
        border_width=2 if com_borda else 0,
        corner_radius=15
    )

#BAsicamente esse é o codigo do projeto que fizemos até agora

with open('dados.json','r',encoding='utf-8') as arquivo:
     dados = json.load(arquivo)

def processar_resultados_atividades():
    """Processa os resultados das atividades por matéria para o aluno logado"""
    resultados = {}
    
    for atividade in dados.get("Atividades", []):
        for resposta in atividade.get("Respostas", []):
            if resposta.get("id_aluno") == Identificador:
                materia = atividade["Id_Materia"]
                resultado = resposta.get("Resultado", "")
                
                if materia not in resultados:
                    resultados[materia] = {"acertos": 0, "erros": 0}
                
                if resultado == "Acertou":
                    resultados[materia]["acertos"] += 1
                elif resultado == "Errou":
                    resultados[materia]["erros"] += 1
    
    return resultados

def obter_notas_faltas_aluno(): 
    """Obtém notas e faltas do aluno logado"""
    notas_aluno = None
    faltas_aluno = None
    
    for notas in dados.get("Notas", []):
        if notas.get("id_aluno") == Identificador:
            notas_aluno = notas
            break 
    
    for faltas in dados.get("Faltas", []):
        if faltas.get("id_aluno") == Identificador:
            faltas_aluno = faltas
            break  
    
    return notas_aluno, faltas_aluno

matFaltas = 0
portFaltas = 0
inglFaltas = 0
matNotas = 0
portNotas = 0
inglNotas = 0
Notas = [matNotas,portNotas,inglNotas]
Materias = []
Faltas = [matFaltas,portFaltas,inglFaltas]
Identificador = None

def logar():
    global Identificador
    ReceberLogin = entradalogin.get()
    ReceberSenha = entradasenha.get()
    # tentativa mínima de autenticação usando o JSON dados
    usuario_encontrado = None
    try:
        # dados.json usa uma chave 'usuarios' contendo uma lista
        usuarios = []
        if isinstance(dados, dict):
            usuarios = dados.get('usuarios', [])
        elif isinstance(dados, list):
            usuarios = dados

        for entry in usuarios:
            if not isinstance(entry, dict):
                continue
            login_field = str(entry.get('login') or entry.get('user') or '')
            senha_field = entry.get('senha') if 'senha' in entry else entry.get('password')
            # comparar como string para cobrir números no JSON
            if login_field == ReceberLogin and str(senha_field) == str(ReceberSenha):
                usuario_encontrado = entry
                break
    except Exception:
        usuario_encontrado = None

    if usuario_encontrado:
        global Identificador
        Identificador = (usuario_encontrado.get('id',0))
        status = str(usuario_encontrado.get('status', '')).lower() if usuario_encontrado.get('status') else ''
        # fechar tela de login antes de abrir a tela apropriada
        try:
            tellogin.destroy()
        except Exception:
            pass
        if 'alun' in status:
            aluno()
        elif 'prof' in status or 'professor' in status:
            professor()
        elif 'gere' in status or 'gerencia' in status:
            admin()
        else:
            messagebox.showinfo('Login', 'Login realizado, mas status não corresponde a aluno/professor/admin')
    else:
        messagebox.showerror("Voce Errrrrrroooou", "Usuário ou senha incorretos")


def cadastroaluno():
    def cadastraraluno():
        Nome = Entrynome.get()
        Cpf = Entrycpf.get()
        idade = Entryidade.get()
        nomeUsuario = Entryusu.get()
        id_Turma= EntryTurma.get()
        senha=Entrysenha.get()
        senha2=Entrysenha2.get()
        Nome_Mae=Entrynomemae.get()
        Nome_Pai = Entrynomepai.get()
        Telefone_mae = Entrytellmae.get()
        Telefone_pai = Entrytellpai.get()
        cadastro_realizado = None
        try:
            usuarios =[]
            if isinstance(dados, dict):
                usuarios = dados.get('usuarios', [])
            elif isinstance(dados, list):
                usuarios = dados

            usu = any(user["login"] == nomeUsuario for user in usuarios)

            if senha != senha2:
                label12.configure(text="Senhas diferentes, alteração necessária")
            elif usu:
                label12.configure(text=f"O nome de usuario: {nomeUsuario}, já existe")
            elif not Nome or not Cpf or not idade or not nomeUsuario or not id_Turma or not senha or not senha2 or not Nome_Mae or not Nome_Pai or not Telefone_mae or not Telefone_pai:
                label12.configure(text="Prencha os Campos nescessários para realização do cadastro")
            else:
               
                
                try:
                    id_usu = 0
                    for al in dados['usuarios']:
                       if al['id'] > id_usu:
                           id_usu = al['id']
                    newid = id_usu + 1
                    def processar_dadosmat(dados, materias):
                        if 'Turma' in dados:
                            for idprocurado in dados['Turma']:
                                if "Id_Materia" in idprocurado and isinstance(idprocurado['Id_Materia'], list):
                                    materias.extend(idprocurado['Id_Materia'])
                        return materias[:3]  # Retorna os 3 primeiros

                    Materias = []
                    Materias = processar_dadosmat(dados, Materias)

                    cadastrar_aluno={
                        "id_aluno":newid,
                        "id_Turma":id_Turma,
                        "Nome":Nome,
                        "Idade": idade,
                        "Nome_mae": Nome_Mae,
                        "Nome_pai": Nome_Pai,
                        "Cpf":Cpf,
                        "Telefone_mae":Telefone_mae,
                        "Telefone_pai":Telefone_pai
                    }
                    cadastrar_usual={
                        "id": newid,
                        "status": "aluno",
                        "login": nomeUsuario ,
                        "senha": senha
                    }
                    cadastrar_Notas = {
                        "id_aluno": newid,
                        "id_Turma": id_Turma,
                        "Notas_Materias": [
                            {
                                "Nota": 0,
                                "Id_Materia": Materias[0] if len(Materias) > 0 else None
                            },
                            {
                                "Nota": 0,
                                "Id_Materia": Materias[1] if len(Materias) > 1 else None
                            },
                            {
                                "Nota": 0,
                                "Id_Materia": Materias[2] if len(Materias) > 2 else None
                            }
                        ]
                    }
                    cadastar_Faltas = [
                         {
                            "id_aluno": 2,
                            "id_Turma": id_Turma,
                            "Faltas_Materias": [
                                {
                                "Faltas": 0,
                                "Id_Materia": Materias[0] if len(Materias) > 0 else None
                                },
                                {
                                "Faltas":0,
                                "Id_Materia": Materias[1] if len(Materias) > 1 else None
                                },
                                {
                                "Faltas": 0,
                                "Id_Materia": Materias[1] if len(Materias) > 1 else None
                                }
                            ]
                        }
                    ]
                    dados["Informacoes_aluno"].append(cadastrar_aluno)
                    dados["usuarios"].append(cadastrar_usual)
                    dados["Notas"].append(cadastrar_Notas)
                    dados["Faltas"].append(cadastar_Faltas)
                    with open('dados.json','w', encoding='utf-8') as arquivo:
                        json.dump(dados, arquivo, indent=3, ensure_ascii=False)
                    label12.configure(text="Cadastro Realizado")
                except KeyError:
                    print("Erro no cadastro")
                #label12.configure(text="Cadastro Realizado")
        except FileNotFoundError:
            None


    nometurmas=[]
    try:
        if 'Turma' in dados:
            for turma in dados['Turma']:
                nometurmas.append(turma['id_Turma'])
    except FileExistsError:
        None

    Cadtell = ctk.CTk()
    Cadtell.title("Tela de Cadastro")
    Cadtell.geometry("500x400")
    #Cadtell.resizable(False,False)
    infoFrame= CTkScrollableFrame(Cadtell, width= 450, height= 280)
    label0 = ctk.CTkLabel(infoFrame, text="CADASTRO", font=("Helvetica",32))
    label1 = ctk.CTkLabel(infoFrame,text="Digite seu Nome completo")
    Entrynome = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label2 = ctk.CTkLabel(infoFrame,text="Digite seu CPF")
    Entrycpf = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label3 = ctk.CTkLabel(infoFrame,text="Informe a Turma para que o\n aluno possa ser cadastrado atraves do ID")
    EntryTurma = ctk.CTkComboBox(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200,values=nometurmas)
    label4 = ctk.CTkLabel(infoFrame,text="Digite sua Idade")
    Entryidade = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label5 = ctk.CTkLabel(infoFrame,text="Digite seu nome de Usuario")
    Entryusu = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label6 = ctk.CTkLabel(infoFrame,text="Digite uma senha de 5 digitos")
    Entrysenha = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label7 = ctk.CTkLabel(infoFrame,text="Confirme sua Senha")
    Entrysenha2 = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200,show="*")
    label8 = ctk.CTkLabel(infoFrame,text="Digite o nome da MÃE")
    Entrynomemae = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label9 = ctk.CTkLabel(infoFrame,text="Digite o nome do PAI")
    Entrynomepai = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label10 = ctk.CTkLabel(infoFrame,text="Digite o telefone da Mãe")
    Entrytellmae = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    label11 = ctk.CTkLabel(infoFrame,text="Digite o telefone do Pai")
    Entrytellpai = ctk.CTkEntry(infoFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200)
    btnCadastrar = ctk.CTkButton(infoFrame, text="Cadastrar Aluno", command=cadastraraluno)
    label12 = ctk.CTkLabel(infoFrame,text="")

    infoFrame.grid(row=0,column=0,sticky =NSEW)
    label0.grid(row =0,column=0, columnspan =2, sticky =NSEW, pady = 30)
    label1.grid(row =1,column=0,columnspan =2, sticky =E, pady = 10)
    Entrynome.grid(row=2, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label2.grid(row =3,column=0, sticky =EW, pady = 10)
    Entrycpf.grid(row=4, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label3.grid(row =5,column=0, sticky =EW, pady = 10)
    EntryTurma.grid(row=6, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label4.grid(row =7,column=0, sticky =EW, pady = 10)
    Entryidade.grid(row=8, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label5.grid(row =9,column=0, sticky =EW, pady = 10)
    Entryusu.grid(row=10, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label6.grid(row =11,column=0, sticky =EW, pady = 10)
    Entrysenha.grid(row=12, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label7.grid(row=13,column=0, sticky =EW, pady = 10)
    Entrysenha2.grid(row=14, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label8.grid(row=15, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    Entrynomemae.grid(row=16, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label9.grid(row=17, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    Entrynomepai.grid(row=18, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label10.grid(row=19, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    Entrytellmae.grid(row=20, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label11.grid(row=21, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    Entrytellpai.grid(row=22, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    btnCadastrar.grid(row=23, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    label12.grid(row=24, column =0,columnspan=2,sticky=EW,pady = 10, padx=10)
    Cadtell.mainloop()

def cadastroturma():
    def cadastraturma():
        Nome = EntryNome.get()
        idTurma = EntryIdTurma.get()
        Materias = EntryMaterias.get().split(',')
        Coordenador = EntryCoordenador.get()
        Periodo= EntryPeriodo.get()
        idMaterias=EntryMaterias.get().split(',')

        try:
            Turma =[]
            if isinstance(dados, dict):
                Turma = dados.get('Turma', [])
            elif isinstance(dados, list):
                Turma = dados

            idTur = any(Tur["id_Turma"] == idTurma for Tur in Turma)
            nomeTur = any(NTur["Nome_Turma"] == Nome for NTur in Turma)

            if nomeTur:
                labelresultado.configure(text=f"O nome da Turma: {Nome}, já existe")
            elif idTur:
                labelresultado.configure(text=f"O ID: {idTurma}, já existe")
            elif not Nome or not idTurma or not idMaterias or not Materias:
                labelresultado.configure(text="Existem Campos em Brancos complete-os")
            else:
                try:
                    cadastrar_Turma = {
                            "id_Turma": idTurma,
                            "Nome_Turma": Nome,
                            "Id_Materia":[idmateria.strip() for idmateria in idMaterias],
                            "Coordenador":Coordenador,
                            "Periodo": Periodo,
                            "Materias": [materia.strip() for materia in Materias]
                        }
                    
                    dados["Turma"].append(cadastrar_Turma)
                    
                    with open('dados.json', 'w', encoding='utf-8') as arquivo:
                        json.dump(dados, arquivo, indent=3, ensure_ascii=False)
                    
                    labelresultado.configure(text="Cadastro da Turma Realizado com Sucesso!")
                    
                except KeyError as e:
                    labelresultado.configure(text=f"Erro no cadastro: {str(e)}")
                except Exception as e:
                    labelresultado.configure(text=f"Erro inesperado: {str(e)}")
                    
        except FileNotFoundError:
            labelresultado.configure(text="Arquivo de dados não encontrado")
    nomeprofessor=[]
    Horarios = ["Matutino", "Vespertino", "Noturno"]
    try:
        if 'Informacoes_Prof' in dados:
            for prof in dados['Informacoes_Prof']:
                nomeprofessor.append(prof['Nome'])
    except FileExistsError:
        None
    Cadtell = ctk.CTk()
    Cadtell.title("Cadastrar Turma")
    Cadtell.geometry("500x500")
    
    frame = CTkScrollableFrame(Cadtell, width=450, height=450)
    
    label0 = ctk.CTkLabel(frame, text="CADASTRO TURMA", font=("Helvetica", 32))
    label1 = ctk.CTkLabel(frame, text="Nome da Turma")
    EntryNome = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30, 
                           border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label2 = ctk.CTkLabel(frame, text="ID DA TURMA")
    EntryIdTurma = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                               border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label3 = ctk.CTkLabel(frame, text="Matérias (separadas por virgula)")
    EntryMaterias = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                               border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label4 = ctk.CTkLabel(frame, text="Professor Coordenador")
    EntryCoordenador = ctk.CTkComboBox(frame, bg_color="#000075", fg_color="white", height=30,
                          border_width=0, font=("Arial", 22), text_color="Black", width=200,values=nomeprofessor)
    
    label5 = ctk.CTkLabel(frame, text="Informe o Periodo")
    EntryPeriodo = ctk.CTkComboBox(frame, bg_color="#000075", fg_color="white", height=30,
                            border_width=0, font=("Arial", 22), text_color="Black", width=200, values=Horarios)
    
    label6 = ctk.CTkLabel(frame, text="Informe o ID das MAtérias \n na mesma ordem dos nomes (separe com vírgulas)")
    EntryIdMaterias = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                             border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    btnCadastrar = ctk.CTkButton(frame, text="Cadastrar Turma", command=cadastraturma)
    labelresultado = ctk.CTkLabel(frame, text="")

    frame.grid(row=0, column=0, sticky=NSEW, padx=25, pady=25)
    label0.grid(row=0, column=0, columnspan=2, sticky=NSEW, pady=30)
    label1.grid(row=1, column=0, sticky=EW, pady=10)
    EntryNome.grid(row=2, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label2.grid(row=3, column=0, sticky=EW, pady=10)
    EntryIdTurma.grid(row=4, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label3.grid(row=5, column=0, sticky=EW, pady=10)
    EntryMaterias.grid(row=6, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label4.grid(row=7, column=0, sticky=EW, pady=10)
    EntryCoordenador.grid(row=8, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label5.grid(row=9, column=0, sticky=EW, pady=10)
    EntryPeriodo.grid(row=10, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label6.grid(row=11, column=0, sticky=EW, pady=10)
    EntryIdMaterias.grid(row=12, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    btnCadastrar.grid(row=13, column=0, columnspan=2, sticky=EW, pady=20, padx=10)
    labelresultado.grid(row=14, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    
    Cadtell.mainloop()

def cadastroprofessor():
    turmas_temp = []
    
    def cadastrar_professor_final():
        Nome = Entrynome.get()
        Materias = Entrymaterias.get().split(',')
        Telefone = Entrytelefone.get()
        nomeUsuario = Entryusu.get()
        senha = Entrysenha.get()
        senha2 = Entrysenha2.get()
        
        try:
            usuarios = []
            if isinstance(dados, dict):
                usuarios = dados.get('usuarios', [])
            elif isinstance(dados, list):
                usuarios = dados

            usu = any(user["login"] == nomeUsuario for user in usuarios)

            if senha != senha2:
                labelresultado.configure(text="Senhas diferentes, alteração necessária", text_color="red")
            elif usu:
                labelresultado.configure(text=f"O nome de usuario: {nomeUsuario}, já existe", text_color="red")
            elif not Nome or not Materias or not Telefone or not nomeUsuario or not senha or not senha2:
                labelresultado.configure(text="Preencha todos os campos necessários", text_color="red")
            elif len(turmas_temp) == 0:
                labelresultado.configure(text="Adicione pelo menos uma turma", text_color="red")
            else:
                try:
                    id_usu = 0
                    for prof in dados['usuarios']:
                        if prof['id'] > id_usu:
                            id_usu = prof['id']
                    newid = id_usu + 1

                    cadastrar_prof = {
                        "id_Prof": newid,
                        "Nome": Nome,
                        "Materias": [materia.strip() for materia in Materias],
                        "Turmas": turmas_temp.copy(),  
                        "Telefone": Telefone
                    }

                    cadastrar_user = {
                        "id": newid,
                        "status": "Professor",
                        "login": nomeUsuario,
                        "senha": senha
                    }

                    dados["Informacoes_Prof"].append(cadastrar_prof)
                    dados["usuarios"].append(cadastrar_user)
                    
                    with open('dados.json', 'w', encoding='utf-8') as arquivo:
                        json.dump(dados, arquivo, indent=3, ensure_ascii=False)
                    
                    labelresultado.configure(text="Cadastro do Professor Realizado com Sucesso!", text_color="green")
                    
                    turmas_temp.clear()
                    label_turmas_adicionadas.configure(text=f"Turmas adicionadas: 0")
                    
                except KeyError as e:
                    labelresultado.configure(text=f"Erro no cadastro: {str(e)}", text_color="red")
                except Exception as e:
                    labelresultado.configure(text=f"Erro inesperado: {str(e)}", text_color="red")
                    
        except FileNotFoundError:
            labelresultado.configure(text="Arquivo de dados não encontrado", text_color="red")

    def abrir_tela_turmas():
        def adicionar_turma():
            id_turma = Entryid_turma.get()
            id_materia = Entryid_materia.get()
            nome_materia = Entrynome_materia.get()
            
            if not id_turma or not id_materia or not nome_materia:
                labelresultado_turma.configure(text="Preencha todos os campos da turma")
                return
            
            turma = {
                "id_turma": id_turma,
                "id_materia": id_materia,
                "nome_materia": nome_materia
            }
            
            turmas_temp.append(turma)
            
            Entryid_turma.delete(0, 'end')
            Entryid_materia.delete(0, 'end')
            Entrynome_materia.delete(0, 'end')
            
            label_turmas_adicionadas.configure(text=f"Turmas adicionadas: {len(turmas_temp)}")
            labelresultado_turma.configure(text="Turma adicionada com sucesso!", text_color="green")

        
        tela_turmas = ctk.CTkToplevel(Cadtell)
        tela_turmas.title("Cadastro de Turmas")
        tela_turmas.geometry("400x400")
        tela_turmas.transient(Cadtell)
        tela_turmas.grab_set()
        nometurmas =[]
        try:
            if 'Turma' in dados:
                for turma in dados['Turma']:
                    nometurmas.append(turma['id_Turma'])
        except FileExistsError:
            None
        frame_turmas = CTkScrollableFrame(tela_turmas, width=350, height=350)
        
        label_titulo = ctk.CTkLabel(frame_turmas, text="CADASTRAR TURMAS", font=("Helvetica", 20))
        
        label_id_turma = ctk.CTkLabel(frame_turmas, text="ID da Turma")
        Entryid_turma = ctk.CTkComboBox(frame_turmas, height=30, font=("Arial", 16), width=200, values=nometurmas)
        
        label_id_materia = ctk.CTkLabel(frame_turmas, text="ID da Matéria")
        Entryid_materia = ctk.CTkEntry(frame_turmas, height=30, font=("Arial", 16), width=200)
        
        label_nome_materia = ctk.CTkLabel(frame_turmas, text="Nome da Matéria")
        Entrynome_materia = ctk.CTkEntry(frame_turmas, height=30, font=("Arial", 16), width=200)
        
        btn_adicionar_turma = ctk.CTkButton(frame_turmas, text="ADICIONAR MAIS TURMAS", 
                                          command=adicionar_turma, fg_color="#4CAF50")
        
        btn_concluir = ctk.CTkButton(frame_turmas, text="CONCLUIR CADASTRO", 
                                   command=cadastrar_professor_final, fg_color="#2196F3")
        
        label_turmas_adicionadas = ctk.CTkLabel(frame_turmas, text=f"Turmas adicionadas: {len(turmas_temp)}")
        labelresultado_turma = ctk.CTkLabel(frame_turmas, text="")

        frame_turmas.grid(row=0, column=0, sticky=NSEW, padx=25, pady=25)
        label_titulo.grid(row=0, column=0, columnspan=2, sticky=NSEW, pady=20)
        label_id_turma.grid(row=1, column=0, sticky=W, pady=5)
        Entryid_turma.grid(row=2, column=0, columnspan=2, sticky=EW, pady=5, padx=10)
        label_id_materia.grid(row=3, column=0, sticky=W, pady=5)
        Entryid_materia.grid(row=4, column=0, columnspan=2, sticky=EW, pady=5, padx=10)
        label_nome_materia.grid(row=5, column=0, sticky=W, pady=5)
        Entrynome_materia.grid(row=6, column=0, columnspan=2, sticky=EW, pady=5, padx=10)
        btn_adicionar_turma.grid(row=7, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
        btn_concluir.grid(row=8, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
        label_turmas_adicionadas.grid(row=9, column=0, columnspan=2, sticky=EW, pady=5)
        labelresultado_turma.grid(row=10, column=0, columnspan=2, sticky=EW, pady=5)

    Cadtell = ctk.CTk()
    Cadtell.title("Cadastro de Professor")
    Cadtell.geometry("500x600")
    
    frame = CTkScrollableFrame(Cadtell, width=450, height=550)
    
    label0 = ctk.CTkLabel(frame, text="CADASTRO PROFESSOR", font=("Helvetica", 32))
    label1 = ctk.CTkLabel(frame, text="Nome Completo do Professor")
    Entrynome = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30, 
                           border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label2 = ctk.CTkLabel(frame, text="Matérias (separadas por vírgula)")
    Entrymaterias = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                               border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label3 = ctk.CTkLabel(frame, text="Telefone")
    Entrytelefone = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                               border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label4 = ctk.CTkLabel(frame, text="Nome de Usuário")
    Entryusu = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                          border_width=0, font=("Arial", 22), text_color="Black", width=200)
    
    label5 = ctk.CTkLabel(frame, text="Senha")
    Entrysenha = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                            border_width=0, font=("Arial", 22), text_color="Black", width=200, show="*")
    
    label6 = ctk.CTkLabel(frame, text="Confirmar Senha")
    Entrysenha2 = ctk.CTkEntry(frame, bg_color="#000075", fg_color="white", height=30,
                             border_width=0, font=("Arial", 22), text_color="Black", width=200, show="*")
    
    btnTurmas = ctk.CTkButton(frame, text="Cadastrar Turmas", command=abrir_tela_turmas, fg_color="#FF9800")
    
    label_turmas_adicionadas = ctk.CTkLabel(frame, text=f"Turmas adicionadas: {len(turmas_temp)}")
    labelresultado = ctk.CTkLabel(frame, text="")

    frame.grid(row=0, column=0, sticky=NSEW, padx=25, pady=25)
    label0.grid(row=0, column=0, columnspan=2, sticky=NSEW, pady=30)
    label1.grid(row=1, column=0, sticky=EW, pady=10)
    Entrynome.grid(row=2, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label2.grid(row=3, column=0, sticky=EW, pady=10)
    Entrymaterias.grid(row=4, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label3.grid(row=5, column=0, sticky=EW, pady=10)
    Entrytelefone.grid(row=6, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label4.grid(row=7, column=0, sticky=EW, pady=10)
    Entryusu.grid(row=8, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label5.grid(row=9, column=0, sticky=EW, pady=10)
    Entrysenha.grid(row=10, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    label6.grid(row=11, column=0, sticky=EW, pady=10)
    Entrysenha2.grid(row=12, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    btnTurmas.grid(row=13, column=0, columnspan=2, sticky=EW, pady=20, padx=10)
    label_turmas_adicionadas.grid(row=14, column=0, columnspan=2, sticky=EW, pady=5)
    labelresultado.grid(row=15, column=0, columnspan=2, sticky=EW, pady=10, padx=10)
    
    Cadtell.mainloop()

def aluno():
    def mostrar_resultados_atividades():
        """Mostra os resultados das atividades por matéria"""
        resultados = processar_resultados_atividades()
        
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        
        frame_titulo = criar_frame_estilizado(frame_conteudo, 1100, 80, COR_MARROM)
        frame_titulo.pack(pady=20, padx=50)
        frame_titulo.pack_propagate(False)
        
        label_titulo = criar_label_estilizado(frame_titulo, "Resultados das Atividades", 24, COR_BRANCO, True)
        label_titulo.pack(expand=True)
        
        if not resultados:
            label_vazio = criar_label_estilizado(frame_conteudo, "Nenhuma atividade respondida ainda", 18, COR_MARROM_CLARO)
            label_vazio.pack(pady=50)
            return
        
        frame_resultados = criar_frame_estilizado(frame_conteudo, 1000, 400, COR_BRANCO)
        frame_resultados.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Cabeçalho da tabela
        frame_cabecalho = ctk.CTkFrame(frame_resultados, fg_color=COR_LARANJA, height=50, corner_radius=10)
        frame_cabecalho.pack(fill="x", padx=20, pady=10)
        frame_cabecalho.pack_propagate(False)
        
        label_materia = criar_label_estilizado(frame_cabecalho, "Matéria", 18, COR_BRANCO, True)
        label_acertos = criar_label_estilizado(frame_cabecalho, "Acertos", 18, COR_BRANCO, True)
        label_erros = criar_label_estilizado(frame_cabecalho, "Erros", 18, COR_BRANCO, True)
        
        label_materia.pack(side="left", padx=50, pady=15)
        label_acertos.pack(side="left", padx=150, pady=15)
        label_erros.pack(side="left", padx=150, pady=15)
        
        # Dados das matérias
        for i, (materia, resultado) in enumerate(resultados.items()):
            frame_linha = ctk.CTkFrame(frame_resultados, fg_color=COR_CINZA if i % 2 == 0 else COR_BRANCO, height=40)
            frame_linha.pack(fill="x", padx=20, pady=2)
            frame_linha.pack_propagate(False)
            
            label_mat = criar_label_estilizado(frame_linha, materia, 16, COR_TEXTO)
            label_acert = criar_label_estilizado(frame_linha, str(resultado["acertos"]), 16, "#28A745", True)
            label_err = criar_label_estilizado(frame_linha, str(resultado["erros"]), 16, "#DC3545", True)
            
            label_mat.pack(side="left", padx=50, pady=10)
            label_acert.pack(side="left", padx=150, pady=10)
            label_err.pack(side="left", padx=150, pady=10)

    def mostrar_notas_faltas():
        """Mostra notas e faltas do aluno"""
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        
        frame_titulo = criar_frame_estilizado(frame_conteudo, 1100, 80, COR_MARROM)
        frame_titulo.pack(pady=20, padx=50)
        frame_titulo.pack_propagate(False)
        
        label_titulo = criar_label_estilizado(frame_titulo, "Notas e Faltas", 24, COR_BRANCO, True)
        label_titulo.pack(expand=True)
        
        notas_aluno, faltas_aluno = obter_notas_faltas_aluno()
        
        if not notas_aluno or not faltas_aluno:
            label_vazio = criar_label_estilizado(frame_conteudo, "Dados não encontrados", 18, COR_MARROM_CLARO)
            label_vazio.pack(pady=50)
            return
        
        frame_dados = criar_frame_estilizado(frame_conteudo, 1000, 400, COR_BRANCO)
        frame_dados.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Cabeçalho
        frame_cabecalho = ctk.CTkFrame(frame_dados, fg_color=COR_LARANJA, height=50, corner_radius=10)
        frame_cabecalho.pack(fill="x", padx=20, pady=10)
        frame_cabecalho.pack_propagate(False)
        
        label_materia = criar_label_estilizado(frame_cabecalho, "Matéria", 18, COR_BRANCO, True)
        label_nota = criar_label_estilizado(frame_cabecalho, "Nota", 18, COR_BRANCO, True)
        label_faltas = criar_label_estilizado(frame_cabecalho, "Faltas", 18, COR_BRANCO, True)
        
        label_materia.pack(side="left", padx=50, pady=15)
        label_nota.pack(side="left", padx=150, pady=15)
        label_faltas.pack(side="left", padx=150, pady=15)
        
        # Dados
        for i, nota_materia in enumerate(notas_aluno.get("Notas_Materias", [])):
            materia_id = nota_materia.get("Id_Materia", "")
            nota = nota_materia.get("Nota", 0)
            
            faltas_materia = 0
            for falta_item in faltas_aluno.get("Faltas_Materias", []):
                if falta_item.get("Id_Materia") == materia_id:
                    faltas_materia = falta_item.get("Faltas", 0)
                    break
            
            frame_linha = ctk.CTkFrame(frame_dados, fg_color=COR_CINZA if i % 2 == 0 else COR_BRANCO, height=40)
            frame_linha.pack(fill="x", padx=20, pady=2)
            frame_linha.pack_propagate(False)
            
            label_mat = criar_label_estilizado(frame_linha, materia_id, 16, COR_TEXTO)
            label_not = criar_label_estilizado(frame_linha, f"{nota:.1f}", 16, COR_MARROM, True)
            label_falt = criar_label_estilizado(frame_linha, str(faltas_materia), 16, COR_LARANJA, True)
            
            label_mat.pack(side="left", padx=50, pady=10)
            label_not.pack(side="left", padx=150, pady=10)
            label_falt.pack(side="left", padx=150, pady=10)

    def conteudoal():
        def tela_atividade(atividade):
            questao = atividade["Perguntas"][0]["Questoes"]
            alternativas_lista = atividade["Perguntas"][0]["Alternativas"]
            id_atv = atividade["id_Atv"]
            materia = atividade["Id_Materia"]
            respcorreta = atividade["Perguntas"][0]["respCorreta"]
            resposta = ""
            alternativa_selecionada = ctk.StringVar(value="")
            
            def confirmar():
                print("Alternativa marcada:", alternativa_selecionada.get())
                letra_marcada = alternativa_selecionada.get()
                if letra_marcada == "":
                    label2.configure(text="Escolha uma Alternativa")
                else:
                    if respcorreta == letra_marcada:
                        resposta = "Acertou"
                    else:
                        resposta = "Errou"
                    nova_resposta = {
                        "id_Atv": atividade["id_Atv"],
                        "id_Turma": atividade["id_Turma"],
                        "id_aluno": Identificador,
                        "Resultado": resposta,
                        "Resp": [
                            {
                                "Alternativa": letra_marcada,
                                "Resposta_Aluno": atividade["Perguntas"][0]["Alternativas"][["A","B","C","D","E"].index(letra_marcada)]
                            }
                        ]
                    }
                    atividade["Respostas"].append(nova_resposta)
                    with open("dados.json", "w", encoding="utf-8") as f:
                        json.dump(dados, f, indent=3, ensure_ascii=False)
                    if resposta == "Acertou":
                        messagebox.showinfo('Resposta', 'Parabens você Acertou!!')
                        exercicio.destroy()
                        conteudoaluno.destroy()
                    else:
                        messagebox.showerror('Resposta', 'Infelizmente você errou. A resposta correta era a letra {}'.format(respcorreta))
                        exercicio.destroy()
                        conteudoaluno.destroy()
            
            def marcar(letra):
                alternativa_selecionada.set(letra)
                for l, cb in checkbox.items():
                    if l != letra:
                        cb.deselect()

            checkbox = {}
            letras = ["A", "B", "C", "D", "E"]

            exercicio = ctk.CTk()
            exercicio.title("Atividade")

            label1 = ctk.CTkLabel(exercicio, text=f"Atividade {id_atv} - Matéria: {materia}")
            label1.pack()

            labelquestao = ctk.CTkLabel(exercicio, text=questao, wraplength=400)
            labelquestao.pack()

            for i, texto in enumerate(alternativas_lista):
                letra = letras[i]
                cb = ctk.CTkCheckBox(
                    master=exercicio,
                    text=f"{letra}) {texto}",
                    command=lambda l=letra: marcar(l)
                )
                cb.pack(anchor="w", padx=20, pady=5)
                checkbox[letra] = cb

            ctk.CTkButton(exercicio, text="Confirmar Resposta", command=confirmar).pack(pady=20)
            label2 = ctk.CTkLabel(exercicio,text="")
            label2.pack(pady=30)

            exercicio.mainloop()

        conteudoaluno = ctk.CTk()
        conteudoaluno.title("Atividades Disponíveis")
        conteudoaluno.geometry("800x600")
        
        frame_aluno = ctk.CTkScrollableFrame(conteudoaluno, height=500, width=700, fg_color="#ffffff")
        frame_aluno.pack(pady=20, padx=50, fill="both", expand=True)

        atividades = dados["Atividades"]
        atividades_pendentes = []
        id_turma_aluno = None
        
        for info in dados["Informacoes_aluno"]:
            if info["id_aluno"] == Identificador:
                id_turma_aluno = info["id_Turma"]
                break

        for atv in atividades:
            if atv["id_Turma"] == id_turma_aluno:
                ja_respondida = any(resp["id_aluno"] == Identificador for resp in atv["Respostas"])
                if not ja_respondida:
                    atividades_pendentes.append(atv)

        # Criar botões para cada atividade
        for atividade in atividades_pendentes:
            materia = atividade["Id_Materia"]
            id_atv = atividade["id_Atv"]
            texto = f"Atividade {id_atv} - Matéria: {materia}"
            btn = ctk.CTkButton(frame_aluno, text=texto, command=lambda a=atividade: tela_atividade(a))
            btn.pack(pady=10)

        if not atividades_pendentes:
            label_vazio = ctk.CTkLabel(frame_aluno, text="Nenhuma atividade pendente", font=("Arial", 16))
            label_vazio.pack(pady=20)

        conteudoaluno.mainloop()

    # === TELA PRINCIPAL DO ALUNO ===
    alunotell = ctk.CTk()
    alunotell.title("Portal do Aluno")
    alunotell.attributes('-fullscreen', True)
    alunotell.configure(fg_color=COR_FUNDO)
    
    # Header
    frame_header = ctk.CTkFrame(alunotell, height=100, fg_color=COR_MARROM, corner_radius=0)
    frame_header.pack(fill="x", pady=(0, 20))
    frame_header.pack_propagate(False)
    
    label_welcome = criar_label_estilizado(frame_header, "Portal do Aluno", 28, COR_BRANCO, True)
    label_welcome.pack(side="left", padx=50, pady=30)
    
    btn_sair = criar_botao_estilizado(frame_header, "Sair", alunotell.destroy, COR_LARANJA, 100, 35)
    btn_sair.pack(side="right", padx=50, pady=30)
    
    # Menu de navegação
    frame_menu = criar_frame_estilizado(alunotell, 1200, 80, COR_LARANJA)
    frame_menu.pack(pady=(0, 30), padx=100)
    frame_menu.pack_propagate(False)
    
    btn_atividades = criar_botao_estilizado(frame_menu, "Resultados", mostrar_resultados_atividades, COR_MARROM, 200, 50)
    btn_notas = criar_botao_estilizado(frame_menu, "Notas e Faltas", mostrar_notas_faltas, COR_MARROM, 200, 50)
    btn_conteudo = criar_botao_estilizado(frame_menu, "Conteúdo", conteudoal, COR_MARROM, 200, 50)
    
    btn_atividades.pack(side="left", padx=30, pady=15)
    btn_notas.pack(side="left", padx=30, pady=15)
    btn_conteudo.pack(side="left", padx=30, pady=15)
    
    # Área de conteúdo
    global frame_conteudo
    frame_conteudo = criar_frame_estilizado(alunotell, 1200, 600, COR_BRANCO)
    frame_conteudo.pack(pady=(0, 50), padx=100)
    frame_conteudo.pack_propagate(False)
    
    # Conteúdo inicial
    label_inicial = criar_label_estilizado(
        frame_conteudo, 
        "Bem-vindo ao Portal do Aluno!\nSelecione uma opção no menu acima.", 
        20, COR_MARROM, True
    )
    label_inicial.pack(expand=True)
    
    alunotell.mainloop()

    def conteudoal():
        def tela_atividade(atividade):

            questao = atividade["Perguntas"][0]["Questoes"]
            alternativas_lista = atividade["Perguntas"][0]["Alternativas"]
            id_atv = atividade["id_Atv"]
            materia = atividade["Id_Materia"]
            respcorreta = atividade["Perguntas"][0]["respCorreta"]
            resposta = ""
            alternativa_selecionada = ctk.StringVar(value="")
            def confirmar():

                print("Alternativa marcada:", alternativa_selecionada.get())
                letra_marcada = alternativa_selecionada.get()
                if letra_marcada == "":
                    label2.configure(text="Escolha uma Alternativa")
                else:
                    if respcorreta == letra_marcada:
                        resposta = "Acertou"
                    else:
                        resposta = "Errou"
                    nova_resposta = {
                        "id_Atv": atividade["id_Atv"],
                        "id_Turma": atividade["id_Turma"],
                        "id_aluno": Identificador,
                        "Resultado": resposta,
                        "Resp": [
                            {
                                "Alternativa": letra_marcada,
                                "Resposta_Aluno": atividade["Perguntas"][0]["Alternativas"][["A","B","C","D","E"].index(letra_marcada)]
                            }
                        ]
                    }
                    atividade["Respostas"].append(nova_resposta)
                    with open("dados.json", "w", encoding="utf-8") as f:
                        json.dump(dados, f, indent=3, ensure_ascii=False)
                    if resposta == "Acertou":
                        messagebox.showinfo('Resposta', 'Parabens você Acertou!!')
                        exercicio.destroy()
                        conteudoaluno.destroy()
                    else:
                        messagebox.showerror('Resposta', 'Infelizmente você errou. A resposta correta era a letra {}'.format(respcorreta))
                        exercicio.destroy()
                        conteudoaluno.destroy()
            def marcar(letra):
                alternativa_selecionada.set(letra)
                for l, cb in checkbox.items():
                    if l != letra:
                        cb.deselect()

            checkbox = {}
            letras = ["A", "B", "C", "D", "E"]

            exercicio = ctk.CTk()
            exercicio.title("Atividade")

            label1 = ctk.CTkLabel(exercicio, text=f"Atividade {id_atv} - Matéria: {materia}")
            label1.pack()

            labelquestao = ctk.CTkLabel(exercicio, text=questao, wraplength=400)
            labelquestao.pack()

            for i, texto in enumerate(alternativas_lista):
                letra = letras[i]
                cb = ctk.CTkCheckBox(
                    master=exercicio,
                    text=f"{letra}) {texto}",
                    command=lambda l=letra: marcar(l)
                )
                cb.pack(anchor="w", padx=20, pady=5)
                checkbox[letra] = cb

            ctk.CTkButton(exercicio, text="Confirmar Resposta", command=confirmar).pack(pady=20)
            label2 = ctk.CTkLabel(exercicio,text="")
            label2.pack(pady=30)

            



            exercicio.mainloop()

        conteudoaluno = ctk.CTk()
        conteudoaluno.title("Bem vindo")
        framemenu_aluno = ctk.CTkFrame(conteudoaluno,height=100, width=1200, corner_radius= 5, fg_color= "#000075", bg_color="#000075")
        btnnotas=ctk.CTkButton(framemenu_aluno, text="Notas e Faltas") #,command=lambda:conteudoaluno.destroy())
        btndados=ctk.CTkButton(framemenu_aluno, text="Dados do Aluno")
        frame_aluno = ctk.CTkScrollableFrame(conteudoaluno, height=700, width=1200, corner_radius=5, fg_color="#ffffff")

        atividades = dados["Atividades"]
        atividades_pendentes = []
        id_turma_aluno = None
        for info in dados["Informacoes_aluno"]:
            if info["id_aluno"] == Identificador:
                id_turma_aluno = info["id_Turma"]
                break


        for atv in atividades:
            if atv["id_Turma"] == id_turma_aluno:
                ja_respondida = any(resp["id_aluno"] == Identificador for resp in atv["Respostas"])
                if not ja_respondida:
                    atividades_pendentes.append(atv)

        # Criar botões para cada atividade
        for atividade in atividades_pendentes:
            materia = atividade["Id_Materia"]
            id_atv = atividade["id_Atv"]
            texto = f"Atividade {id_atv} - Matéria: {materia}"
            btn = ctk.CTkButton(frame_aluno, text=texto, command=lambda a=atividade: tela_atividade(a))
            btn.pack(pady=10)

        

        
        framemenu_aluno.grid(row=0,column=0,pady=0, padx=(100,100))
        btnnotas.grid(row=0, column = 1, padx= 25, pady=30)
        btndados.grid(row=0, column = 2, padx= 25, pady=30)
        frame_aluno.grid(pady=0, padx=(100,100),row=1)
        conteudoaluno.mainloop()

    def mostrar_resultados_atividades():
        """Mostra os resultados das atividades por matéria"""
        resultados = processar_resultados_atividades()
        
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        
        frame_titulo = criar_frame_estilizado(frame_conteudo, 1100, 80, COR_MARROM)
        frame_titulo.pack(pady=20, padx=50)
        frame_titulo.pack_propagate(False)
        
        label_titulo = criar_label_estilizado(frame_titulo, "Resultados das Atividades", 24, COR_BRANCO, True)
        label_titulo.pack(expand=True)
        
        if not resultados:
            label_vazio = criar_label_estilizado(frame_conteudo, "Nenhuma atividade respondida ainda", 18, COR_MARROM_CLARO)
            label_vazio.pack(pady=50)
            return
        
        frame_resultados = criar_frame_estilizado(frame_conteudo, 1000, 400, COR_BRANCO)
        frame_resultados.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Cabeçalho da tabela
        frame_cabecalho = ctk.CTkFrame(frame_resultados, fg_color=COR_LARANJA, height=50, corner_radius=10)
        frame_cabecalho.pack(fill="x", padx=20, pady=10)
        frame_cabecalho.pack_propagate(False)
        
        label_materia = criar_label_estilizado(frame_cabecalho, "Matéria", 18, COR_BRANCO, True)
        label_acertos = criar_label_estilizado(frame_cabecalho, "Acertos", 18, COR_BRANCO, True)
        label_erros = criar_label_estilizado(frame_cabecalho, "Erros", 18, COR_BRANCO, True)
        
        label_materia.pack(side="left", padx=50, pady=15)
        label_acertos.pack(side="left", padx=150, pady=15)
        label_erros.pack(side="left", padx=150, pady=15)
        
        # Dados das matérias
        for i, (materia, resultado) in enumerate(resultados.items()):
            frame_linha = ctk.CTkFrame(frame_resultados, fg_color=COR_CINZA if i % 2 == 0 else COR_BRANCO, height=40)
            frame_linha.pack(fill="x", padx=20, pady=2)
            frame_linha.pack_propagate(False)
            
            label_mat = criar_label_estilizado(frame_linha, materia, 16, COR_TEXTO)
            label_acert = criar_label_estilizado(frame_linha, str(resultado["acertos"]), 16, "#28A745", True)
            label_err = criar_label_estilizado(frame_linha, str(resultado["erros"]), 16, "#DC3545", True)
            
            label_mat.pack(side="left", padx=50, pady=10)
            label_acert.pack(side="left", padx=150, pady=10)
            label_err.pack(side="left", padx=150, pady=10)

    def mostrar_notas_faltas():
        """Mostra notas e faltas do aluno"""
        for widget in frame_conteudo.winfo_children():
            widget.destroy()
        
        frame_titulo = criar_frame_estilizado(frame_conteudo, 1100, 80, COR_MARROM)
        frame_titulo.pack(pady=20, padx=50)
        frame_titulo.pack_propagate(False)
        
        label_titulo = criar_label_estilizado(frame_titulo, "Notas e Faltas", 24, COR_BRANCO, True)
        label_titulo.pack(expand=True)
        
        notas_aluno, faltas_aluno = obter_notas_faltas_aluno()
        
        if not notas_aluno or not faltas_aluno:
            label_vazio = criar_label_estilizado(frame_conteudo, "Dados não encontrados", 18, COR_MARROM_CLARO)
            label_vazio.pack(pady=50)
            return
        
        frame_dados = criar_frame_estilizado(frame_conteudo, 1000, 400, COR_BRANCO)
        frame_dados.pack(pady=20, padx=50, fill="both", expand=True)
        
        # Cabeçalho
        frame_cabecalho = ctk.CTkFrame(frame_dados, fg_color=COR_LARANJA, height=50, corner_radius=10)
        frame_cabecalho.pack(fill="x", padx=20, pady=10)
        frame_cabecalho.pack_propagate(False)
        
        label_materia = criar_label_estilizado(frame_cabecalho, "Matéria", 18, COR_BRANCO, True)
        label_nota = criar_label_estilizado(frame_cabecalho, "Nota", 18, COR_BRANCO, True)
        label_faltas = criar_label_estilizado(frame_cabecalho, "Faltas", 18, COR_BRANCO, True)
        
        label_materia.pack(side="left", padx=50, pady=15)
        label_nota.pack(side="left", padx=150, pady=15)
        label_faltas.pack(side="left", padx=150, pady=15)
        
        # Dados
        for i, nota_materia in enumerate(notas_aluno.get("Notas_Materias", [])):
            materia_id = nota_materia.get("Id_Materia", "")
            nota = nota_materia.get("Nota", 0)
            
            faltas_materia = 0
            for falta_item in faltas_aluno.get("Faltas_Materias", []):
                if falta_item.get("Id_Materia") == materia_id:
                    faltas_materia = falta_item.get("Faltas", 0)
                    break
            
            frame_linha = ctk.CTkFrame(frame_dados, fg_color=COR_CINZA if i % 2 == 0 else COR_BRANCO, height=40)
            frame_linha.pack(fill="x", padx=20, pady=2)
            frame_linha.pack_propagate(False)
            
            label_mat = criar_label_estilizado(frame_linha, materia_id, 16, COR_TEXTO)
            label_not = criar_label_estilizado(frame_linha, f"{nota:.1f}", 16, COR_MARROM, True)
            label_falt = criar_label_estilizado(frame_linha, str(faltas_materia), 16, COR_LARANJA, True)
            
            label_mat.pack(side="left", padx=50, pady=10)
            label_not.pack(side="left", padx=150, pady=10)
            label_falt.pack(side="left", padx=150, pady=10)

    # === NOVO DESIGN === TELA PRINCIPAL DO ALUNO ===
    alunotell = ctk.CTk()
    alunotell.title("Portal do Aluno")
    alunotell.attributes('-fullscreen', True)
    alunotell.configure(fg_color=COR_FUNDO)
    
    # Header
    frame_header = ctk.CTkFrame(alunotell, height=100, fg_color=COR_MARROM, corner_radius=0)
    frame_header.pack(fill="x", pady=(0, 20))
    frame_header.pack_propagate(False)
    
    label_welcome = criar_label_estilizado(frame_header, "Portal do Aluno", 28, COR_BRANCO, True)
    label_welcome.pack(side="left", padx=50, pady=30)
    
    btn_sair = criar_botao_estilizado(frame_header, "Sair", alunotell.destroy, COR_LARANJA, 100, 35)
    btn_sair.pack(side="right", padx=50, pady=30)
    
    # Menu de navegação
    frame_menu = criar_frame_estilizado(alunotell, 1200, 80, COR_LARANJA)
    frame_menu.pack(pady=(0, 30), padx=100)
    frame_menu.pack_propagate(False)
    
    btn_atividades = criar_botao_estilizado(frame_menu, "Resultados", mostrar_resultados_atividades, COR_MARROM, 200, 50)
    btn_notas = criar_botao_estilizado(frame_menu, "Notas e Faltas", mostrar_notas_faltas, COR_MARROM, 200, 50)
    btn_conteudo = criar_botao_estilizado(frame_menu, "Conteúdo", conteudoal, COR_MARROM, 200, 50)
    
    btn_atividades.pack(side="left", padx=30, pady=15)
    btn_notas.pack(side="left", padx=30, pady=15)
    btn_conteudo.pack(side="left", padx=30, pady=15)
    
    # Área de conteúdo
    frame_conteudo = criar_frame_estilizado(alunotell, 1200, 600, COR_BRANCO)
    frame_conteudo.pack(pady=(0, 50), padx=100)
    frame_conteudo.pack_propagate(False)
    
    # Conteúdo inicial
    label_inicial = criar_label_estilizado(
        frame_conteudo, 
        "Bem-vindo ao Portal do Aluno!\nSelecione uma opção no menu acima.", 
        20, COR_MARROM, True
    )
    label_inicial.pack(expand=True)
    
    alunotell.mainloop()
    # === FIM DO NOVO DESIGN ===


def professor():
    
    def lancarAtividade():
        def CadastrarAtv():
            print("Identificador atual:", Identificador)
            print("Informacoes_Prof:", dados.get('Informacoes_Prof', []))
            numeroalt = sum(1 for a in Alt if a.strip())
            Nome_Exercicio= EntryNome.get()
            Turma = EntryTurma.get()
            Atividade = EntryAtv.get("0.0","end").strip()
            Resposta = EntryAltCorreta.get()
            Id_Mat = EntryIdmat.get()
            try:
                id_Atv = 0
                for at in dados['Atividades']:
                    if at['id_Atv'] > id_Atv:
                        id_Atv = at['id_Atv']
                newid = id_Atv + 1



                if Id_Mat in idmateriasProf:
                    if not Nome_Exercicio or not Turma or not Atividade or not all(Alt):
                        label2.configure(text="Preencha corretamente os campos")
                    elif numeroalt != 5:
                        label2.configure(text="Coloque todas as alternativas")
                    else:
                        Atv = {
                            "id_Turma": Turma,
                            "id_Prof": Identificador,
                            "id_Atv": newid,
                            "Id_Materia": Id_Mat,
                            "Perguntas": [{
                                "Questoes": Atividade,
                                "Alternativas": Alt,
                                "respCorreta": Resposta
                            }],
                            "Respostas": [{
                                "id_Atv": newid,
                                "id_Turma": Turma,
                                "id_aluno": "",
                                "Resp": [{
                                    "Alternativa": "",
                                    "Resposta_Aluno": ""
                                }]
                            }]
                        }
                        dados["Atividades"].append(Atv)
                        with open('dados.json', 'w', encoding='utf-8') as arquivo:
                            json.dump(dados, arquivo, indent=3, ensure_ascii=False)
                else:
                    label2.configure(text="Id Materia não existe na Turma")
            except KeyError as e:
                label2.configure(text=f"Erro no cadastro: {str(e)}", text_color="red")
            except Exception as e:
                label2.configure(text=f"Erro inesperado: {str(e)}", text_color="red")
                    
           
        def Alternativas():
            for i in range(5):
                if all(alt != "" for alt in Alt):
                    print("Todas as alternativas foram prenchidas")
                    break
                elif Alt[i] == "":
                    Alt[i] = Entryalternativas.get("0.0","end").strip()
                    print(f"{Alt[i]}")
                    break
                else:
                     print(f"{Alt[i]}")
        Alt = [""] * 5
        nometurmas=[]
        idmateriasTurma = []
        idmateriasProf = []
        Resp = ["A", "B", "C", "D", "E"]
        try:
            if 'Turma' in dados:
                for turma in dados['Turma']:
                    nometurmas.append(turma['id_Turma'])
            if 'Turma' in dados:
                for turma in dados['Turma']:
                    if 'Id_Materia' in turma and isinstance (turma['Id_Materia'],list):
                        idmateriasTurma.extend(turma['Id_Materia'])



            idmateriasProf = []

            if 'Informacoes_Prof' in dados:
                for prof in dados['Informacoes_Prof']:
                    if int(prof.get('id_Prof', -1)) == Identificador:
                        for turma in prof.get('Turmas', []):
                            materia = turma.get('Id_Materia')
                            if materia:
                                idmateriasProf.append(materia)

            print("Materias do professor:", idmateriasProf)

        except FileNotFoundError:
            print("Erro Arquivo não encontrado")
        lancarAtv = ctk.CTk()
        lancarAtv.title("Lançar nova Atividade")
        lancarAtv.attributes('-fullscreen', True)
        lancarAtv.configure(fg_color="#4B2C0A")
        AtvFrame= CTkScrollableFrame(lancarAtv, width= 550, height= 280)
        label1 = ctk.CTkLabel(AtvFrame, text="Olá Professor adione sua Atividade:", font=("Arial", 30), text_color="White")
        labelnome = ctk.CTkLabel(AtvFrame,text="Digite o nome da atividade")
        EntryNome = ctk.CTkEntry(AtvFrame)
        labelturma=ctk.CTkLabel(AtvFrame, text="Escolha a Turma correspondente")
        EntryTurma = ctk.CTkComboBox(AtvFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200,values=nometurmas)
        labelAtv=ctk.CTkLabel(AtvFrame, text="Escreva o Exercicio")
        EntryAtv = ctk.CTkTextbox(AtvFrame,width=450,height=250)
        EntryAtv.insert("0.0","Digite aqui")
        labelidmateriaprof=ctk.CTkLabel(AtvFrame, text="Escolha o Id da sua matéria")
        EntryIdmat = ctk.CTkComboBox(AtvFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200,values=idmateriasProf)
        labelAlternativas = ctk.CTkLabel(AtvFrame, text="Digite as 5 alternativas")
        Entryalternativas = ctk.CTkTextbox(AtvFrame,width=450,height=100)
        labelAlternativaCorreta = ctk.CTkLabel(AtvFrame, text="Informe a Alternativa Correta")
        EntryAltCorreta = ctk.CTkComboBox(AtvFrame, bg_color="#000075",fg_color="white", height=30,border_width=0,font=("Arial", 22),text_color="Black",width=200,values=Resp)
        BtnAdicionarAlt=ctk.CTkButton(AtvFrame,text="Adicionar Alternativa",command=Alternativas)
        BtnExcluirAlt=ctk.CTkButton(AtvFrame,text="Excluir a Ultima Alternativa Adicionada", command=lambda: Alt.pop() if Alt and any(Alt) else None)
        BtnLancar=ctk.CTkButton(AtvFrame,text="Lançar Atividade", command=CadastrarAtv)
        BtnAdicionarQuest=ctk.CTkButton(AtvFrame,text="Adicionar Questão")
        BtnExcluir=ctk.CTkButton(AtvFrame,text="Excluir atividade")
        label2 = ctk.CTkLabel(AtvFrame, text="", font=("Arial", 15), text_color="White")

        AtvFrame.grid(row=0,column=0,sticky =NSEW)
        label1.grid(row=0,column=0,columnspan = 5, sticky = EW,padx=20,pady=15)
        labelnome.grid(row=1,column=2,sticky=EW,pady=(0,10))
        EntryNome.grid(row=2,column=1, columnspan=3,sticky=EW)
        labelturma.grid(row=3,column=2,sticky=EW,pady=(0,10))
        EntryTurma.grid(row=4,column=1, columnspan=3,sticky=EW)
        labelAtv.grid(row=5,column=2,sticky=EW,pady=(0,10))
        EntryAtv.grid(row=6,column=1, columnspan=3,rowspan=4,sticky=EW)
        labelidmateriaprof.grid(row=10,column=2,sticky=EW,pady=(0,10))
        EntryIdmat.grid(row=11,column=1, columnspan=3,sticky=EW)
        labelAlternativas.grid(row=12,column=2,sticky=EW,pady=(0,10))
        Entryalternativas.grid(row=13,column=1, columnspan=3,rowspan=2,sticky=EW)
        labelAlternativaCorreta.grid(row=16,column=2,sticky=EW,pady=(0,10))
        EntryAltCorreta.grid(row=17,column=1, columnspan=3,rowspan=2,sticky=EW)
        
        BtnAdicionarAlt.grid(row=20,column=1,sticky=EW)
        BtnExcluirAlt.grid(row=20,column=2,sticky=EW)
        BtnLancar.grid(row=20,column=3,sticky=EW)
        BtnAdicionarQuest.grid(row=21,column=1,sticky=EW)
        BtnExcluir.grid(row=21,column=2,sticky=EW)
        label2.grid(row=22,column=2,sticky=EW)
        lancarAtv.mainloop()

    def lancar_notas_faltas():
        """Tela para o professor lançar notas e faltas"""
        def carregar_alunos_turma():
            turma_selecionada = combo_turma.get()
            if not turma_selecionada:
                return []
            
            alunos = []
            for info in dados.get("Informacoes_aluno", []):
                if info.get("id_Turma") == turma_selecionada:
                    alunos.append({
                        "id": info.get("id_aluno"),
                        "nome": info.get("Nome", "")
                    })
            return alunos
        
        def carregar_materias_professor():
            turma_selecionada = combo_turma.get()
            if not turma_selecionada:
                return []
            
            materias = []
            for prof in dados.get("Informacoes_Prof", []):
                if prof.get("id_Prof") == Identificador:
                    for turma in prof.get("Turmas", []):
                        if turma.get("id_Turma") == turma_selecionada:
                            materias.append(turma.get("Id_Materia"))
            return materias
        
        def atualizar_dados():
            alunos = carregar_alunos_turma()
            materias = carregar_materias_professor()
            
            combo_aluno.configure(values=[f"{aluno['id']} - {aluno['nome']}" for aluno in alunos])
            combo_materia.configure(values=materias)
            
            if alunos:
                combo_aluno.set(f"{alunos[0]['id']} - {alunos[0]['nome']}")
            if materias:
                combo_materia.set(materias[0])
        
        def salvar_nota_falta():
            try:
                aluno_selecionado = combo_aluno.get()
                materia_selecionada = combo_materia.get()
                nota = entry_nota.get()
                faltas = entry_faltas.get()
                
                if not all([aluno_selecionado, materia_selecionada, nota, faltas]):
                    messagebox.showerror("Erro", "Preencha todos os campos")
                    return
                
                aluno_id = int(aluno_selecionado.split(" - ")[0])
                nota_float = float(nota)
                faltas_int = int(faltas)
                
                # Atualizar notas
                for aluno_notas in dados["Notas"]:
                    if aluno_notas["id_aluno"] == aluno_id and aluno_notas["id_Turma"] == combo_turma.get():
                        for nota_materia in aluno_notas["Notas_Materias"]:
                            if nota_materia["Id_Materia"] == materia_selecionada:
                                nota_materia["Nota"] = nota_float
                                break
                
                # Atualizar faltas
                for aluno_faltas in dados["Faltas"]:
                    if aluno_faltas["id_aluno"] == aluno_id and aluno_faltas["id_Turma"] == combo_turma.get():
                        for falta_materia in aluno_faltas["Faltas_Materias"]:
                            if falta_materia["Id_Materia"] == materia_selecionada:
                                falta_materia["Faltas"] = faltas_int
                                break
                
                with open("dados.json", "w", encoding="utf-8") as f:
                    json.dump(dados, f, indent=3, ensure_ascii=False)
                
                messagebox.showinfo("Sucesso", "Nota e faltas atualizadas com sucesso!")
                
            except ValueError:
                messagebox.showerror("Erro", "Digite valores numéricos válidos")
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao salvar: {str(e)}")
        
       
        notas_tell = ctk.CTk()
        notas_tell.title("Lançar Notas e Faltas")
        notas_tell.geometry("500x400")
        
        turmas_prof = []
        for prof in dados.get("Informacoes_Prof", []):
            if prof.get("id_Prof") == Identificador:
                for turma in prof.get("Turmas", []):
                    if turma.get("id_Turma") not in turmas_prof:
                        turmas_prof.append(turma.get("id_Turma"))
        
        frame = ctk.CTkFrame(notas_tell)
        frame.pack(pady=20, padx=20, fill="both", expand=True)
        
        ctk.CTkLabel(frame, text="Lançar Notas e Faltas", font=("Arial", 20)).pack(pady=10)
        
        ctk.CTkLabel(frame, text="Selecione a Turma:").pack(pady=5)
        combo_turma = ctk.CTkComboBox(frame, values=turmas_prof)
        combo_turma.pack(pady=5)
        combo_turma.bind("<<ComboboxSelected>>", lambda e: atualizar_dados())
        
        ctk.CTkLabel(frame, text="Selecione o Aluno:").pack(pady=5)
        combo_aluno = ctk.CTkComboBox(frame, values=[])
        combo_aluno.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Selecione a Matéria:").pack(pady=5)
        combo_materia = ctk.CTkComboBox(frame, values=[])
        combo_materia.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Nota (0-10):").pack(pady=5)
        entry_nota = ctk.CTkEntry(frame)
        entry_nota.pack(pady=5)
        
        ctk.CTkLabel(frame, text="Número de Faltas:").pack(pady=5)
        entry_faltas = ctk.CTkEntry(frame)
        entry_faltas.pack(pady=5)
        
        btn_salvar = criar_botao_estilizado(frame, "Salvar Nota e Faltas", salvar_nota_falta, COR_LARANJA, 300, 45)
        btn_salvar.pack(pady=20)
        
        if turmas_prof:
            combo_turma.set(turmas_prof[0])
            atualizar_dados()
        
        notas_tell.mainloop()

    proftell = ctk.CTk()
    proftell.title("Portal do Professor")
    proftell.attributes('-fullscreen', True)
    proftell.configure(fg_color=COR_FUNDO)
    
    # Header
    frame_header = ctk.CTkFrame(proftell, height=100, fg_color=COR_MARROM, corner_radius=0)
    frame_header.pack(fill="x", pady=(0, 20))
    frame_header.pack_propagate(False)
    
    label_welcome = criar_label_estilizado(frame_header, "Portal do Professor", 28, COR_BRANCO, True)
    label_welcome.pack(side="left", padx=50, pady=30)
    
    btn_sair = criar_botao_estilizado(frame_header, "Sair", proftell.destroy, COR_LARANJA, 100, 35)
    btn_sair.pack(side="right", padx=50, pady=30)
    
    # Menu de navegação
    frame_menu = criar_frame_estilizado(proftell, 1200, 80, COR_LARANJA)
    frame_menu.pack(pady=(0, 30), padx=100)
    frame_menu.pack_propagate(False)
    
    btn_notas = criar_botao_estilizado(frame_menu, "Lançar Notas/Faltas", lancar_notas_faltas, COR_MARROM, 250, 50)
    btn_atividades = criar_botao_estilizado(frame_menu, "Lançar Atividade", lancarAtividade, COR_MARROM, 250, 50)
    btn_dados = criar_botao_estilizado(frame_menu, "Meus Dados", lambda: messagebox.showinfo("Em desenvolvimento", "Funcionalidade em desenvolvimento"), COR_MARROM, 250, 50)
    
    btn_notas.pack(side="left", padx=20, pady=15)
    btn_atividades.pack(side="left", padx=20, pady=15)
    btn_dados.pack(side="left", padx=20, pady=15)
    
    # Área de conteúdo
    frame_conteudo = criar_frame_estilizado(proftell, 1200, 600, COR_BRANCO)
    frame_conteudo.pack(pady=(0, 50), padx=100)
    frame_conteudo.pack_propagate(False)
    
    # Conteúdo inicial
    label_inicial = criar_label_estilizado(
        frame_conteudo, 
        "Bem-vindo ao Portal do Professor!\n\n"
        "• Lançar Notas e Faltas: Atualize as avaliações dos alunos\n"
        "• Lançar Atividade: Crie novas atividades para suas turmas\n"
        "• Meus Dados: Visualize suas informações pessoais", 
        18, COR_MARROM, False
    )
    label_inicial.pack(expand=True, padx=50, pady=50)
    
    # Estatísticas rápidas (opcional)
    frame_stats = criar_frame_estilizado(frame_conteudo, 1000, 100, COR_CINZA, False)
    frame_stats.pack(side="bottom", pady=20, padx=50)
    frame_stats.pack_propagate(False)
    
    label_stats = criar_label_estilizado(
        frame_stats, 
        "💼 Professor | 📚 Gestão de Turmas | 🎯 Avaliações", 
        14, COR_MARROM_CLARO, False
    )
    label_stats.pack(expand=True)
    
    proftell.mainloop()

def admin():
    admin_tell = ctk.CTk()
    admin_tell.title("Portal Administrativo")
    admin_tell.attributes('-fullscreen', True)
    admin_tell.configure(fg_color=COR_FUNDO)
    
    # Header
    frame_header = ctk.CTkFrame(admin_tell, height=100, fg_color=COR_MARROM, corner_radius=0)
    frame_header.pack(fill="x", pady=(0, 20))
    frame_header.pack_propagate(False)
    
    label_welcome = criar_label_estilizado(frame_header, "Portal Administrativo", 28, COR_BRANCO, True)
    label_welcome.pack(side="left", padx=50, pady=30)
    
    btn_sair = criar_botao_estilizado(frame_header, "Sair", admin_tell.destroy, COR_LARANJA, 100, 35)
    btn_sair.pack(side="right", padx=50, pady=30)
    
    # Título da seção
    frame_titulo = criar_frame_estilizado(admin_tell, 1200, 80, COR_LARANJA)
    frame_titulo.pack(pady=(0, 30), padx=100)
    frame_titulo.pack_propagate(False)
    
    label_titulo = criar_label_estilizado(frame_titulo, "Gerenciamento do Sistema", 24, COR_BRANCO, True)
    label_titulo.pack(expand=True)
    
    # Área de cards de funcionalidades
    frame_cards = ctk.CTkFrame(admin_tell, fg_color="transparent")
    frame_cards.pack(pady=30, padx=100, fill="both", expand=True)
    
    # Card 1 - Cadastro de Aluno
    frame_card_aluno = criar_frame_estilizado(frame_cards, 350, 200, COR_BRANCO)
    frame_card_aluno.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
    
    icon_aluno = criar_label_estilizado(frame_card_aluno, "👨‍🎓", 40, COR_LARANJA)
    icon_aluno.pack(pady=(20, 10))
    
    label_card_aluno = criar_label_estilizado(frame_card_aluno, "Cadastrar Aluno", 20, COR_MARROM, True)
    label_card_aluno.pack(pady=(0, 10))
    
    desc_aluno = criar_label_estilizado(
        frame_card_aluno, 
        "Adicione novos alunos\nao sistema", 
        14, COR_TEXTO, False
    )
    desc_aluno.pack(pady=(0, 15))
    
    btn_card_aluno = criar_botao_estilizado(frame_card_aluno, "Acessar", cadastroaluno, COR_LARANJA, 200, 40)
    btn_card_aluno.pack(pady=10)
    
    # Card 2 - Cadastro de Turma
    frame_card_turma = criar_frame_estilizado(frame_cards, 350, 200, COR_BRANCO)
    frame_card_turma.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
    
    icon_turma = criar_label_estilizado(frame_card_turma, "🏫", 40, COR_LARANJA)
    icon_turma.pack(pady=(20, 10))
    
    label_card_turma = criar_label_estilizado(frame_card_turma, "Cadastrar Turma", 20, COR_MARROM, True)
    label_card_turma.pack(pady=(0, 10))
    
    desc_turma = criar_label_estilizado(
        frame_card_turma, 
        "Crie novas turmas e\ndefina suas matérias", 
        14, COR_TEXTO, False
    )
    desc_turma.pack(pady=(0, 15))
    
    btn_card_turma = criar_botao_estilizado(frame_card_turma, "Acessar", cadastroturma, COR_LARANJA, 200, 40)
    btn_card_turma.pack(pady=10)
    
    # Card 3 - Cadastro de Professor
    frame_card_prof = criar_frame_estilizado(frame_cards, 350, 200, COR_BRANCO)
    frame_card_prof.grid(row=0, column=2, padx=20, pady=20, sticky="nsew")
    
    icon_prof = criar_label_estilizado(frame_card_prof, "👨‍🏫", 40, COR_LARANJA)
    icon_prof.pack(pady=(20, 10))
    
    label_card_prof = criar_label_estilizado(frame_card_prof, "Cadastrar Professor", 20, COR_MARROM, True)
    label_card_prof.pack(pady=(0, 10))
    
    desc_prof = criar_label_estilizado(
        frame_card_prof, 
        "Adicione professores\ne suas disciplinas", 
        14, COR_TEXTO, False
    )
    desc_prof.pack(pady=(0, 15))
    
    btn_card_prof = criar_botao_estilizado(frame_card_prof, "Acessar", cadastroprofessor, COR_LARANJA, 200, 40)
    btn_card_prof.pack(pady=10)
    
    # Configurar grid para centralizar
    frame_cards.grid_columnconfigure(0, weight=1)
    frame_cards.grid_columnconfigure(1, weight=1)
    frame_cards.grid_columnconfigure(2, weight=1)
    frame_cards.grid_rowconfigure(0, weight=1)
    
    # Footer com informações
    frame_footer = ctk.CTkFrame(admin_tell, fg_color=COR_CINZA, height=60, corner_radius=0)
    frame_footer.pack(side="bottom", fill="x", pady=(20, 0))
    frame_footer.pack_propagate(False)
    
    label_footer = criar_label_estilizado(
        frame_footer, 
        "🔧 Administração do Sistema | 📊 Gestão Completa | 👥 Controle de Usuários", 
        12, COR_MARROM, False
    )
    label_footer.pack(expand=True)
    
    admin_tell.mainloop()

#Criando tela de Login
tellogin = ctk.CTk()
tellogin.title("Sistema Educacional - Login")
tellogin.geometry("500x600")
tellogin.configure(fg_color=COR_FUNDO)
tellogin.resizable(False, False)

# Frame principal
frame_login = criar_frame_estilizado(tellogin, 450, 500, COR_BRANCO)
frame_login.pack(pady=50, padx=25, fill="both", expand=True)
frame_login.pack_propagate(False)

# Logo/Header
frame_header = ctk.CTkFrame(frame_login, fg_color=COR_MARROM, height=100, corner_radius=0)
frame_header.pack(fill="x", pady=(0, 30))
frame_header.pack_propagate(False)

label_titulo = criar_label_estilizado(frame_header, "Sistema Educacional", 28, COR_BRANCO, True)
label_titulo.pack(expand=True)

label_subtitulo = criar_label_estilizado(frame_header, "Faça login para continuar", 16, COR_LARANJA_CLARO)
label_subtitulo.pack(pady=(0, 15))

# Formulário de login
frame_form = ctk.CTkFrame(frame_login, fg_color="transparent")
frame_form.pack(pady=30, padx=50, fill="both")

# Campo de login
criar_label_estilizado(frame_form, "Usuário:", 16, COR_MARROM).pack(anchor="w", pady=(10, 5))
entradalogin = criar_entry_estilizado(frame_form, 350, 45)
entradalogin.pack(pady=(0, 20))

# Campo de senha
criar_label_estilizado(frame_form, "Senha:", 16, COR_MARROM).pack(anchor="w", pady=(10, 5))
entradasenha = criar_entry_estilizado(frame_form, 350, 45, True)
entradasenha.pack(pady=(0, 30))

# Botão de login
btnLogar = criar_botao_estilizado(frame_form, "ENTRAR", logar, COR_LARANJA, 350, 50)
btnLogar.pack(pady=20)

# Footer
label_footer = criar_label_estilizado(frame_login, "© 2024 Sistema Educacional - Todos os direitos reservados", 12, COR_MARROM_CLARO)
label_footer.pack(side="bottom", pady=20)

# Bind Enter para login
def fazer_login_enter(event):
    logar()

entradasenha.bind("<Return>", fazer_login_enter)

tellogin.mainloop()
