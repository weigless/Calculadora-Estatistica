import sqlite3
from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, font, Toplevel, ttk
from tkinter import Toplevel, Label, Button, filedialog
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Scrollbar
from tkinter import ttk, simpledialog, Button
import tkinter as tk
from tkinter import font, messagebox
import numpy as np
from scipy import stats
from tkinter.ttk import Treeview
from tabulate import tabulate
from tkinter import Tk, Toplevel, Text, Scrollbar, END, messagebox, Entry
from ttkwidgets.autocomplete import AutocompleteEntry
from math import comb
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg



tabela = None
def fazer_login(conexao, usuario, senha):
    apagar_tabelas(conexao)
    cursor = conexao.cursor()
    cursor.execute('SELECT * FROM Login WHERE usuario = ? AND senha = ?', (usuario, senha))
    resultado = cursor.fetchone()
    return resultado is not None

def cadastrar_usuario(conexao, usuario, senha):
    cursor = conexao.cursor()
    cursor.execute('INSERT INTO Login (usuario, senha) VALUES (?, ?)', (usuario, senha))
    conexao.commit()

def verificar_login(janela, conexao, usuario_var, senha_var):
    usuario = usuario_var.get()
    senha = senha_var.get()
    if fazer_login(conexao, usuario, senha):
        messagebox.showinfo("Sucesso", "Login bem-sucedido!")
        abrir_opcoes_analises(conexao)
        janela.withdraw()  # Oculta a janela de login
    else:
        messagebox.showerror("Erro", "Usuário ou senha incorretos")

def abrir_tela_cadastro(janela, conexao, fonte, usuario_var, senha_var):
    janela_cadastro = Toplevel(janela)
    janela_cadastro.title("Cadastro")

    Label(janela_cadastro, text="Usuário", font=fonte).grid(row=0)
    Label(janela_cadastro, text="Senha", font=fonte).grid(row=1)

    usuario_cadastro_var = StringVar()
    senha_cadastro_var = StringVar()

    Entry(janela_cadastro, textvariable=usuario_cadastro_var, font=fonte).grid(row=0, column=1)
    Entry(janela_cadastro, textvariable=senha_cadastro_var, show='*', font=fonte).grid(row=1, column=1)

    Button(janela_cadastro, text="Cadastrar", command=lambda: cadastrar_e_notificar_usuario(conexao, usuario_cadastro_var, senha_cadastro_var, janela_cadastro, fonte), font=fonte).grid(columnspan=2)

def cadastrar_e_notificar_usuario(conexao, usuario_cadastro_var, senha_cadastro_var, janela_cadastro, fonte):
    cadastrar_usuario(conexao, usuario_cadastro_var.get(), senha_cadastro_var.get())
    messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")
    janela_cadastro.destroy()  # Fecha a janela de cadastro após o cadastro ser concluído

janela_opcoes = None
def abrir_opcoes_analises(conexao):
    global janela_opcoes  
    janela_opcoes = Toplevel()
    janela_opcoes.title("Opções de Análises")
    janela_opcoes.geometry("600x500")  

    fonte_opcoes = font.Font(size=14)  # Tamanho da fonte para os botões e labels

    # Adiciona uma Label com o texto "Escolha uma opção:"
    Label(janela_opcoes, text="Escolha uma opção:", font=fonte_opcoes).pack(pady=10)

    # Adiciona os botões numerados com opções
    Button(janela_opcoes, text="Análise de Pareto", command=lambda: abrir_janela_pareto(conexao), font=fonte_opcoes).pack(pady=5)
    Button(janela_opcoes, text="Medidas de Tendência Central e Dispersão", command=lambda: abrir_janela_medidas(conexao), font=fonte_opcoes).pack(pady=5)
    Button(janela_opcoes, text="Calculadora de Probabilidade Binomial", command=lambda: calcular_probabilidade_binomial(janela_opcoes), font=fonte_opcoes).pack(pady=5)
    Button(janela_opcoes, text="Sair", command=lambda: confirmar_sair(conexao, janela_opcoes), font=fonte_opcoes).pack(pady=5)

def abrir_janela_pareto(conexao):
    janela_pareto = tk.Toplevel()
    janela_pareto.title("Análise de Pareto")
    janela_pareto.geometry("400x200")

    fonte_pareto = font.Font(size=12)  # Tamanho da fonte para os botões e labels

    # Adiciona uma Label com o texto "Escolha uma opção:"
    tk.Label(janela_pareto, text="Escolha uma opção:", font=fonte_pareto).pack(pady=10)
    tk.Label(janela_pareto, text="Você vai enviar dados com valores associados?", font=12).pack(pady=15)

    # Função para lidar com a escolha "Sim"
    def escolha_sim():
        messagebox.showinfo("Escolha", "Você escolheu enviar os dados com valores associados.")
        enviar_dados_pareto(conexao)
        janela_pareto.destroy()

    # Função para lidar com a escolha "Não"
    def escolha_nao():
        messagebox.showinfo("Escolha", "Você escolheu enviar os dados sem valores associados.")
        nao_enviar_dados_pareto(conexao)
        janela_pareto.destroy()

    # Adiciona os botões de opção usando a messagebox
    tk.Button(janela_pareto, text="Sim", command=escolha_sim, font=fonte_pareto, width=10).pack(side="left", padx=10, pady=15, anchor="center")
    tk.Button(janela_pareto, text="Não", command=escolha_nao, font=fonte_pareto, width=10).pack(side="left", padx=10, pady=15, anchor="center")
    tk.Button(janela_pareto, text="Voltar", command=janela_pareto.destroy, font=fonte_pareto, width=10).pack(side="left", padx=10, pady=15, anchor="center")

def enviar_dados_pareto(conexao):
    criar_colunas_pareto(conexao)
    abrir_tela_analise_pareto(conexao)

def criar_colunas_pareto(conexao):
    # Abre um cursor para executar comandos SQLite
    cursor = conexao.cursor()

    # Criação das colunas no SQLite
    cursor.execute('''CREATE TABLE IF NOT EXISTS DadosPareto (
                      Qualitativo TEXT,
                      Quantitativo1 INTEGER,
                      Quantitativo2 INTEGER,
                      Impacto REAL  
                  )''')

    # Commit para salvar as alterações
    conexao.commit()

    # Fecha o cursor
    cursor.close()

def abrir_tela_analise_pareto(conexao):
    janela_analise_pareto = Toplevel()
    janela_analise_pareto.title("Análise de Pareto Com Valores Associados")
    janela_analise_pareto.geometry("600x500")

    fonte_analise_pareto = font.Font(size=14)  # Tamanho da fonte para os botões e labels

    # Adiciona uma Label com o título "Análise de Pareto"
    Label(janela_analise_pareto, text="Análise de Pareto Com Valores Associados", font=fonte_analise_pareto).pack(pady=10)

    # Adiciona os botões
    Button(janela_analise_pareto, text="Enviar Dados", command=lambda: importar_dados_pareto(conexao), font=fonte_analise_pareto, width=15).pack(pady=10)
    Button(janela_analise_pareto, text="Tabela da Análise de Pareto", command=lambda: gerar_tabela_pareto(conexao), font=fonte_analise_pareto, width=30).pack(pady=10)
    Button(janela_analise_pareto, text="Gráfico da Análise de Pareto", command=lambda: gerar_grafico_pareto(conexao), font=fonte_analise_pareto, width=30).pack(pady=10)
    Button(janela_analise_pareto, text="Visualizar / Alterar Dados", command=lambda: visualizar_dados_pareto(conexao), font=fonte_analise_pareto, width=20).pack(pady=10)
    Button(janela_analise_pareto, text="Voltar", command=janela_analise_pareto.destroy, font=fonte_analise_pareto, width=25).pack(pady=10)

def visualizar_dados_pareto(conexao):
    janela_visualizar_dados = Toplevel()
    janela_visualizar_dados.title("Visualizar Dados de Pareto")
    janela_visualizar_dados.geometry("800x500")

    # Consulta os dados da tabela DadosPareto no SQLite
    query = "SELECT * FROM DadosPareto"
    df = pd.read_sql(query, conexao)

    # Crie uma tabela para exibir os dados
    tabela = ttk.Treeview(janela_visualizar_dados)
    tabela['columns'] = tuple(df.columns)

    for col in tabela['columns']:
        tabela.column(col, anchor='w', width=150)
        tabela.heading(col, text=col, anchor='w')

    for index, row in df.iterrows():
        tabela.insert('', index, values=tuple(row))

    tabela.pack(padx=10, pady=10, fill='both', expand=True)

    # Adicione um botão para editar dados
    Button(janela_visualizar_dados, text="Editar Dados", command=lambda: editar_dados_pareto(conexao, tabela)).pack(pady=10)
    Button(janela_visualizar_dados, text="Voltar", command=janela_visualizar_dados.destroy).pack(pady=10)

def editar_dados_pareto(conexao, tabela):
    # Obtenha a linha selecionada
    selected_item = tabela.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione uma linha para editar.")
        return

    # Obtenha os valores da linha selecionada
    values = tabela.item(selected_item, 'values')

    # Crie uma caixa de diálogo para editar todos os campos de uma vez
    novo_valores = simpledialog.askstring("Editar Valores", "Digite os novos valores separados por vírgula (,):", initialvalue=','.join(map(str, values)))
    if novo_valores is not None:
        # Divida os novos valores e atualize a linha no banco de dados
        novos_valores = novo_valores.split(',')
        colunas = tabela['columns']
        tabela_nome = 'DadosPareto'
        atualizacao_query = f"UPDATE {tabela_nome} SET "
        for coluna, novo_valor in zip(colunas, novos_valores):
            atualizacao_query += f"{coluna} = '{novo_valor}', "
        # Remova a vírgula extra no final
        atualizacao_query = atualizacao_query.rstrip(', ')
        # Adicione a condição WHERE para identificar a linha específica
        condicao = f"WHERE {' AND '.join([f'{coluna} = ?' for coluna in colunas])}"
        atualizacao_query += f" {condicao}"

        # Execute a atualização no banco de dados
        cursor = conexao.cursor()
        cursor.execute(atualizacao_query, tuple(values))
        conexao.commit()
        cursor.close()

        # Atualize a tabela na interface gráfica
        visualizar_dados_pareto(conexao)
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")

def importar_dados_pareto(conexao):
    messagebox.showinfo("Aviso", "Certifique-se de selecionar um arquivo no formato XLSX e que a primeira linha do arquivo seja o título dos dados.")
    try:
        # Abrir o diálogo de seleção de arquivo
        filepath = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx")])

        if not filepath:
            messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.")
            return

        # Carregar dados do arquivo Excel, ignorando a primeira linha
        df = pd.read_excel(filepath, header=None, skiprows=1)

        # Adicionar colunas ao DataFrame df
        df.columns = ['DescricaoEvento', 'Frequencia', 'Impacto']

        # Salvar os dados no SQLite
        df.to_sql('DadosPareto', conexao, if_exists='replace', index=False)

        messagebox.showinfo("Sucesso", "Dados importados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar dados: {str(e)}")

def gerar_tabela_pareto(conexao):
    try:
        # Consulta os dados da tabela DadosPareto no SQLite
        query = "SELECT * FROM DadosPareto"
        df = pd.read_sql(query, conexao)

        if df.empty:
            messagebox.showinfo("Aviso", "Não há dados disponíveis para análise.")
            return

        # Adicionar coluna 'Total Geral' com o cálculo: 'Impacto' * 'Frequencia'
        df['Total Geral'] = df['Impacto'] * df['Frequencia']

        # Ordenar o DataFrame pela coluna 'Total Geral' em ordem decrescente
        df = df.sort_values(by='Total Geral', ascending=False, ignore_index=True)

        # Adicionar coluna 'Fr(%)' com o cálculo: 'Total Geral' / soma de 'Total Geral'
        df['Fr(%)'] = (df['Total Geral'] / df['Total Geral'].sum(axis=0)) * 100

        # Calcular a frequência cumulativa em percentual
        df['Freq Cumulativa'] = df['Fr(%)'].cumsum()

        # Criar um novo DataFrame para a linha "Total"
        total_row = {
            'DescricaoEvento': 'Total',
            'Frequencia': df['Frequencia'].sum(),
            'Impacto': '-',
            'Total Geral': df['Total Geral'].sum(),
            'Fr(%)': '100%',
            'Freq Cumulativa': '-'
        }
        df_total = pd.DataFrame([total_row])

        # Concatenar o DataFrame original com o DataFrame da linha "Total"
        df = pd.concat([df, df_total], ignore_index=True)

        # Mostrar a tabela gerada
        janela_tabela_pareto = Toplevel()
        janela_tabela_pareto.title("Tabela da Análise de Pareto")

        scroll_y = Scrollbar(janela_tabela_pareto, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        tabela = ttk.Treeview(janela_tabela_pareto)
        tabela['columns'] = (
            'Descrição do Evento', 'Frequência', 'Impacto',
            'Total Geral', 'Fr(%)', 'Freq Cumulativa'
        )

        # Adiciona o seguinte código para definir o alinhamento à esquerda para todas as colunas
        for col in tabela['columns']:
            tabela.column(col, anchor='w', width=150)


        tabela.heading('#0', text='', anchor='center')
        tabela.heading('Descrição do Evento', text='Descrição do Evento', anchor='center')
        tabela.heading('Frequência', text='Frequência', anchor='center')
        tabela.heading('Impacto', text='Impacto', anchor='center')
        tabela.heading('Total Geral', text='Total Geral', anchor='center')
        tabela.heading('Fr(%)', text='Fr(%)', anchor='center')
        tabela.heading('Freq Cumulativa', text='Freq Cumulativa', anchor='center')

        for index, row in df.iterrows():
            descricao_evento = row['DescricaoEvento']
            frequencia = row['Frequencia']
            impacto = '-' if descricao_evento == 'Total' else row['Impacto']
            total_geral = '-' if descricao_evento == 'Total Geral' else row['Total Geral']
            frequencia_porcentagem = f"{row['Fr(%)']:.2f}%" if descricao_evento != 'Total' else '100.00%'
            frequencia_cumulativa= f"{row['Freq Cumulativa']:.2f}%" if descricao_evento != 'Total' else '-'

            tabela.insert('', index, values=(descricao_evento, frequencia, impacto, total_geral, frequencia_porcentagem, frequencia_cumulativa))

        janela_tabela_pareto.geometry("1800x500")
        scroll_y.config(command=tabela.yview)

        tabela.pack(padx=10, pady=10, fill='both', expand=True)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar tabela: {str(e)}")

def gerar_grafico_pareto_sem_valores(conexao):
    try:
        # Consulta os dados da tabela DadosNaoPareto no SQLite
        query = "SELECT * FROM DadosNaoPareto"
        df = pd.read_sql(query, conexao)

        if df.empty:
            messagebox.showinfo("Aviso", "Não há dados disponíveis para análise.")
            return

        # Ordenar o DataFrame pela coluna 'Ocorrencias' em ordem decrescente
        df = df.sort_values(by='Ocorrencias', ascending=False, ignore_index=True)

        # Calcular a frequência cumulativa em percentual
        df['Freq Cumulativa'] = (df['Ocorrencias'].cumsum() / df['Ocorrencias'].sum()) * 100

        # Criar o gráfico de Pareto
        fig, ax1 = plt.subplots(figsize=(10, 6))

        # Barra para 'Ocorrencias'
        ax1.bar(df.index, df['Ocorrencias'], color='b', alpha=0.7, align='center')
        ax1.set_xlabel('Categorias')
        ax1.set_ylabel('Ocorrências', color='b')
        ax1.tick_params('y', colors='b')

        # Adiciona uma linha para 'Freq Cumulativa'
        ax2 = ax1.twinx()
        ax2.plot(df.index, df['Freq Cumulativa'], color='r', marker='o')
        ax2.set_ylabel('Frequência Cumulativa (%)', color='r')
        ax2.tick_params('y', colors='r')

        # Adiciona rótulos ao eixo x
        ax1.set_xticks(df.index)
        ax1.set_xticklabels(df['Descricao'], rotation=45, ha='right')

        plt.title("Gráfico de Pareto")
        plt.show()

        fig.tight_layout()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar gráfico: {str(e)}")

def gerar_grafico_pareto(conexao):
    try:
        # Consulta os dados da tabela DadosPareto no SQLite
        query = "SELECT * FROM DadosPareto"
        df = pd.read_sql(query, conexao)

        if df.empty:
            messagebox.showinfo("Aviso", "Não há dados disponíveis para análise.")
            return

        # Adicionar coluna 'Total Geral' com o cálculo: 'Impacto' * 'Frequencia'
        df['Total Geral'] = df['Impacto'] * df['Frequencia']

        # Ordenar o DataFrame pela coluna 'Total Geral' em ordem decrescente
        df = df.sort_values(by='Total Geral', ascending=False, ignore_index=True)

        # Calcular a frequência cumulativa em percentual
        df['Freq Cumulativa'] = (df['Total Geral'].cumsum() / df['Total Geral'].sum()) * 100

        # Criar o gráfico de Pareto
        fig, ax1 = plt.subplots(figsize=(12, 6))  # Aumentei a largura para 12

        # Barra para 'Total Geral'
        ax1.bar(df.index, df['Total Geral'], color='b', alpha=0.7, align='center', bottom=0.245)  # Ajuste bottom aqui
        ax1.set_xlabel('Categorias')
        ax1.set_ylabel('Total Geral', color='b')
        ax1.tick_params('y', colors='b')

        # Adiciona uma linha para 'Freq Cumulativa'
        ax2 = ax1.twinx()
        ax2.plot(df.index, df['Freq Cumulativa'], color='r', marker='o')
        ax2.set_ylabel('Frequência Cumulativa (%)', color='r')
        ax2.tick_params('y', colors='r')

        # Adiciona rótulos ao eixo x com rotação de 45 graus
        ax1.set_xticks(df.index)
        ax1.set_xticklabels(df['DescricaoEvento'], rotation=45, ha='right', fontsize=8)  # Ajustei a fonte

        plt.title("Gráfico de Pareto")
        plt.show()
        fig.tight_layout()

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar gráfico: {str(e)}")

def importar_dados_pareto_sem_valores(conexao):
    messagebox.showinfo("Aviso", "Certifique-se de selecionar um arquivo no formato XLSX e que a primeira linha do arquivo seja o título dos dados.")
    try:
        # Abrir o diálogo de seleção de arquivo
        filepath = filedialog.askopenfilename(title="Selecione um arquivo", filetypes=[("Arquivos Excel", "*.xlsx")])

        if not filepath:
            messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.")
            return

        # Carregar dados do arquivo Excel, ignorando a primeira linha
        df = pd.read_excel(filepath, header=None, skiprows=1)

        # Adicionar colunas ao DataFrame df
        df.columns = ['Descricao', 'Ocorrencias']

        # Salvar os dados no SQLite
        df.to_sql('DadosNaoPareto', conexao, if_exists='replace', index=False)

        messagebox.showinfo("Sucesso", "Dados importados com sucesso!")

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao importar dados: {str(e)}")
        
def abrir_tela_analise_pareto_sem_valores(conexao):
    janela_analise_pareto = Toplevel()
    janela_analise_pareto.title("Análise de Pareto Sem Valores Associados")
    janela_analise_pareto.geometry("600x500")

    fonte_analise_pareto = font.Font(size=14)  # Tamanho da fonte para os botões e labels

    # Adiciona uma Label com o título "Análise de Pareto"
    Label(janela_analise_pareto, text="Análise de Pareto Sem Valores Associados", font=fonte_analise_pareto).pack(pady=10)

    # Adiciona os botões
    Button(janela_analise_pareto, text="Enviar Dados", command=lambda: importar_dados_pareto_sem_valores(conexao), font=fonte_analise_pareto, width=15).pack(pady=10)
    Button(janela_analise_pareto, text="Tabela da Análise de Pareto", command=lambda: gerar_tabela_pareto_sem_valores(conexao), font=fonte_analise_pareto, width=30).pack(pady=10)
    Button(janela_analise_pareto, text="Gráfico da Análise de Pareto", command=lambda: gerar_grafico_pareto_sem_valores(conexao), font=fonte_analise_pareto, width=30).pack(pady=10)
    Button(janela_analise_pareto, text="Visualizar / Alterar Dados", command=lambda: visualizar_dados_nao_pareto(conexao), font=fonte_analise_pareto, width=20).pack(pady=10)
    Button(janela_analise_pareto, text="Voltar", command=janela_analise_pareto.destroy, font=fonte_analise_pareto, width=25).pack(pady=10)

def visualizar_dados_nao_pareto(conexao):
    janela_visualizar_dados = Toplevel()
    janela_visualizar_dados.title("Visualizar Dados de Não Pareto")
    janela_visualizar_dados.geometry("800x500")

    query = "SELECT * FROM DadosNaoPareto"
    df = pd.read_sql(query, conexao)

    tabela = ttk.Treeview(janela_visualizar_dados)
    tabela['columns'] = tuple(df.columns)

    for col in tabela['columns']:
        tabela.column(col, anchor='w')
        tabela.heading(col, text=col, anchor='w')

    for index, row in df.iterrows():
        tabela.insert('', index, values=tuple(row))

    tabela.pack(padx=10, pady=10, fill='both', expand=True)

    Button(janela_visualizar_dados, text="Editar Dados", command=lambda: editar_dados_nao_pareto(conexao, tabela)).pack(pady=10)
    Button(janela_visualizar_dados, text="Voltar", command=janela_visualizar_dados.destroy).pack(pady=10)

def editar_dados_nao_pareto(conexao, tabela):
    selected_item = tabela.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione uma linha para editar.")
        return

    values = tabela.item(selected_item, 'values')

    novo_valores = simpledialog.askstring("Editar Valores", "Digite os novos valores separados por vírgula (,):", initialvalue=','.join(map(str, values)))
    if novo_valores is not None:
        novos_valores = novo_valores.split(',')
        colunas = tabela['columns']
        tabela_nome = 'DadosNaoPareto'
        atualizacao_query = f"UPDATE {tabela_nome} SET "
        for coluna, novo_valor in zip(colunas, novos_valores):
            atualizacao_query += f"{coluna} = '{novo_valor}', "
        atualizacao_query = atualizacao_query.rstrip(', ')
        condicao = f"WHERE {' AND '.join([f'{coluna} = ?' for coluna in colunas])}"
        atualizacao_query += f" {condicao}"

        cursor = conexao.cursor()
        cursor.execute(atualizacao_query, tuple(values))
        conexao.commit()
        cursor.close()

        visualizar_dados_nao_pareto(conexao)
        messagebox.showinfo("Sucesso", "Dados atualizados com sucesso!")

def nao_enviar_dados_pareto(conexao):
    criar_colunas_nao_pareto(conexao)
    abrir_tela_analise_pareto_sem_valores(conexao)

def criar_colunas_nao_pareto(conexao):
    cursor = conexao.cursor()

    # Criação das colunas no SQLite
    cursor.execute('''CREATE TABLE IF NOT EXISTS DadosNaoPareto (
                      Qualitativo TEXT,
                      Quantitativo INTEGER
                  )''')

    # Commit para salvar as alterações
    conexao.commit()

    # Fecha o cursor
    cursor.close()

def gerar_tabela_pareto_sem_valores(conexao):
    try:
        # Consulta os dados da tabela DadosNaoPareto no SQLite
        query = "SELECT * FROM DadosNaoPareto"
        df = pd.read_sql(query, conexao)

        if df.empty:
            messagebox.showinfo("Aviso", "Não há dados disponíveis para análise.")
            return

              
        df['Fr(%)'] = (df['Ocorrencias'] / df['Ocorrencias'].sum(axis=0)) * 100

        # Calcular a frequência cumulativa em percentual
        df['Freq Cumulativa'] = df['Fr(%)'].cumsum()

        # Criar um novo DataFrame para a linha "Total"
        total_row = {
            'Descricao': 'Total',
            'Ocorrencias': df['Ocorrencias'].sum(),
            'Fr(%)': '100%',
            'Freq Cumulativa': '-'
        }
        df_total = pd.DataFrame([total_row])

        # Concatenar o DataFrame original com o DataFrame da linha "Total"
        df = pd.concat([df, df_total], ignore_index=True)

        # Mostrar a tabela gerada
        janela_tabela_pareto = Toplevel()
        janela_tabela_pareto.title("Tabela da Análise de Pareto Sem Valores")

        scroll_y = Scrollbar(janela_tabela_pareto, orient="vertical")
        scroll_y.pack(side="right", fill="y")

        tabela = ttk.Treeview(janela_tabela_pareto)
        tabela['columns'] = (
            'Descrição', 'Ocorrências', 'Fr(%)', 'Freq Cumulativa'
        )

        # Adiciona o seguinte código para definir o alinhamento à esquerda para todas as colunas
        for col in tabela['columns']:
            tabela.column(col, anchor='w', width=150)

        tabela['columns'] = ('Descricao', 'Ocorrencias', 'Fr(%)', 'Freq Cumulativa')

        tabela.column('#0', anchor='center')
        tabela.column('Descricao', anchor='center')
        tabela.heading('Descricao', text='Descrição', anchor='center')
        tabela.column('Ocorrencias', anchor='center')
        tabela.heading('Ocorrencias', text='Ocorrências', anchor='center')
        tabela.column('Fr(%)', anchor='center')
        tabela.heading('Fr(%)', text='Fr(%)', anchor='center')
        tabela.column('Freq Cumulativa', anchor='center')
        tabela.heading('Freq Cumulativa', text='Freq Cumulativa', anchor='center')


        for index, row in df.iterrows():
            descricao = row['Descricao']
            ocorrencias = row['Ocorrencias']
            frequencia_porcentagem = f"{row['Fr(%)']:.2f}%" if descricao != 'Total' else '100.00%'
            frequencia_cumulativa = f"{row['Freq Cumulativa']:.2f}%" if descricao != 'Total' else '-'

            tabela.insert('', index, values=(descricao, ocorrencias, frequencia_porcentagem, frequencia_cumulativa))

        janela_tabela_pareto.geometry("1800x500")

        scroll_y.config(command=tabela.yview)

        tabela.pack(padx=10, pady=10, fill='both', expand=True)

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar tabela: {str(e)}")
    
def abrir_janela_medidas(conexao):
    janela_medidas = Toplevel()
    janela_medidas.title(" Distribuição de frequência e Medidas Estatísticas")
    janela_medidas.geometry("600x400")

    fonte_analise_pareto = font.Font(size=14)

    Label(janela_medidas, text="Distribuição de frequência e Medidas Estatísticas", font=fonte_analise_pareto).pack(pady=10)

    # Adiciona os botões
    Button(janela_medidas, text="Enviar Dados", command=lambda: importar_dados_medidas(conexao), font=fonte_analise_pareto, width=20).pack(pady=5)
    Button(janela_medidas, text="Tabela de Distribuição de Frequências", command=gerar_tabela_frequencia, font=fonte_analise_pareto, width=30).pack(pady=5)
    Button(janela_medidas, text="Tabela de Medidas Estatísticas", command=gerar_tabela_medidas, font=fonte_analise_pareto, width=30).pack(pady=5)
    #Button(janela_medidas, text="Gerar Gráfico", command=lambda: gerar_grafico_medidas(tabela_frequencia), font=fonte_analise_pareto, width=30).pack(pady=10)
    Button(janela_medidas, text="Voltar", command=janela_medidas.destroy, font=fonte_analise_pareto, width=20).pack(pady=5)
  
def importar_dados_medidas(caminho_bd):

    messagebox.showinfo("Aviso", "Certifique-se de selecionar um arquivo no formato XLSX e que a primeira linha do arquivo seja o título dos dados.")
    arquivo_excel = filedialog.askopenfilename(title="Selecione o arquivo Excel", filetypes=[("Arquivos Excel", "*.xlsx;*.xls")])

    if arquivo_excel:
        try:
            # Verificar se a primeira linha contém letras
            primeira_linha = pd.read_excel(arquivo_excel, nrows=1).iloc[0]
            primeira_linha_contem_letras = any(isinstance(c, str) and any(x.isalpha() for x in c) for c in primeira_linha)

            # Ler o arquivo Excel, ignorando a primeira linha se contiver letras
            dados_excel = pd.read_excel(arquivo_excel, skiprows=1 if primeira_linha_contem_letras else 0)

            # Conectar ao banco de dados SQLite
            conn = sqlite3.connect(r'C:\Users\Usuário\Documents\PROJETOS PYTHON\Projeto_Estatistica\Sistema_Estatistica.db')
            cursor = conn.cursor()

            # Criar a tabela "DadosMedidas" se ela não existir
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS DadosMedidas (
                    Coluna1 INTEGER,
                    Coluna2 REAL,
                    Coluna3 TEXT
                )
            ''')

            # Inserir dados na tabela
            dados_excel.to_sql('DadosMedidas', conn, if_exists='replace', index=False)

            # Commit e fechar a conexão
            conn.commit()
            conn.close()

            # Exibir mensagem de sucesso
            messagebox.showinfo("Sucesso", "Dados importados com sucesso!")

        except Exception as ex:
            # Exibir mensagem de erro em caso de falha
            messagebox.showerror("Erro", f"Ocorreu um erro durante a importação dos dados: {str(ex)}")
    else:
        # Exibir mensagem se nenhum arquivo for selecionado
        messagebox.showinfo("Aviso", "Nenhum arquivo selecionado.")

def tabela_existente(conexao):
    # Verificar se a tabela 'DadosMedidas' existe no banco de dados
    cursor = conexao.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='DadosMedidas';")
    tabela_existe = cursor.fetchone()
    return tabela_existe is not None

def gerar_tabela_frequencia():
    
    conexao = sqlite3.connect(r'C:\Users\Usuário\Documents\PROJETOS PYTHON\Projeto_Estatistica\Sistema_Estatistica.db')
    

    try:
        if not tabela_existente(conexao):
            messagebox.showinfo("Erro", "Você deve enviar os dados primeiro.")
            conexao.close()
            return

        # Executar a consulta para obter os valores numéricos da tabela DadosMedidas
        cursor = conexao.cursor()
        cursor.execute("SELECT * FROM DadosMedidas")
        dados = cursor.fetchall()

        # Verificar se há dados na tabela
        if len(dados) == 0:
            messagebox.showinfo("Aviso", "Você deve enviar os dados primeiro.")
            return
        

        # Criar um DataFrame pandas com os dados
        df = pd.DataFrame(dados, columns=[f"Coluna_{i}" for i in range(len(dados[0]))])

        # Converter todos os valores para números (remover strings, etc.)
        df = df.apply(pd.to_numeric, errors='coerce')

        # Criar a tabela de distribuição de frequências
        tabela_frequencia = pd.cut(df.values.flatten(), bins=10, include_lowest=True).value_counts().sort_index().reset_index()
        tabela_frequencia.columns = ['Intervalo', 'Frequência']

        # Verificar se os dados originais são do tipo inteiro ou float
        tipo_dados = df.applymap(type).iloc[0, 0]

        # Arredondar os valores dos intervalos conforme o tipo dos dados
        if tipo_dados == int:
            tabela_frequencia['Intervalo'] = tabela_frequencia['Intervalo'].apply(lambda x: pd.Interval(round(x.left), round(x.right)))
        elif tipo_dados == float:
            tabela_frequencia['Intervalo'] = tabela_frequencia['Intervalo'].apply(lambda x: pd.Interval(x.left, x.right))
        else:
            # Lógica para outros tipos de dados, se necessário
            pass

        # Adicionar colunas Ponto Médio, Fr, e Fr acumulado (%)
        tabela_frequencia['Ponto Médio'] = tabela_frequencia['Intervalo'].apply(lambda x: x.mid)
        tabela_frequencia['Fr'] = tabela_frequencia['Frequência'] / tabela_frequencia['Frequência'].sum()
        tabela_frequencia['Fr(%)'] = tabela_frequencia['Fr'] * 100 / 100
        tabela_frequencia['Fr acumulado (%)'] = tabela_frequencia['Fr(%)'].cumsum().fillna(0)

        # Adicionar uma linha com totais
        total_row = pd.Series({
            'Intervalo': 'Total',
            'Ponto Médio': '-',
            'Frequência': tabela_frequencia['Frequência'].sum(),
            'Fr': tabela_frequencia['Fr'].sum(),
            'Fr(%)': tabela_frequencia['Fr(%)'].sum(),
            'Fr acumulado (%)': '-'
        })

        # Concatenar o DataFrame original com a linha total
        tabela_frequencia = pd.concat([tabela_frequencia, total_row.to_frame().T], ignore_index=True)

        # Fechar a conexão com o banco de dados
        conexao.close()

        # Exibir a tabela de frequência em uma nova janela
        exibir_janela_tabela(tabela_frequencia)
        

    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao gerar tabela de distribuição de frequências: {str(e)}")
        conexao.close()
   
def exibir_janela_tabela(tabela_frequencia):
    janela_tabela = tk.Tk()
    janela_tabela.title("Tabela de Distribuição de Frequências")

    largura_janela = 1300
    altura_janela = 400

    # Obtenha as dimensões da tela
    largura_tela = janela_tabela.winfo_screenwidth()
    altura_tela = janela_tabela.winfo_screenheight()

    # Calcule a posição para centralizar a janela
    x_pos = (largura_tela - largura_janela) // 2
    y_pos = (altura_tela - altura_janela) // 2

    # Configure a geometria da janela
    janela_tabela.geometry(f"{largura_janela}x{altura_janela}+{x_pos}+{y_pos}")

    # Criar uma treeview para exibir a tabela
    tree = ttk.Treeview(janela_tabela)
    tree['columns'] = ('Intervalo', 'Ponto Médio', 'Frequência', 'Fr', 'Fr(%)', 'Fr acumulado (%)')

    # Configurar as colunas
    for col in ('Intervalo', 'Ponto Médio', 'Frequência', 'Fr', 'Fr(%)', 'Fr acumulado (%)'):
        tree.column(col, anchor=tk.CENTER, width=150)

    # Configurar os cabeçalhos das colunas
    for col in ('Intervalo', 'Ponto Médio', 'Frequência', 'Fr', 'Fr(%)', 'Fr acumulado (%)'):
        tree.heading(col, text=col, anchor=tk.CENTER)

    # Preencher a treeview com os dados da tabela de frequência
    for index, row in tabela_frequencia.iterrows():
        intervalo = f"{row['Intervalo'].left:.2f} - {row['Intervalo'].right:.2f}" if isinstance(row['Intervalo'], pd._libs.interval.Interval) else row['Intervalo']
        ponto_medio = f"{row['Ponto Médio']:.2f}" if row['Ponto Médio'] != '-' else '-'
        fr = f"{row['Fr']:.2f}" if row['Fr'] != '-' else '-'
        fr_percent = f"{row['Fr(%)']:.2%}" if row['Fr(%)'] != '-' else '-'
        fr_acumulado_percent = f"{row['Fr acumulado (%)']:.2%}" if row['Fr acumulado (%)'] != '-' else '-'

        tree.insert('', index, values=(intervalo, ponto_medio, row['Frequência'], fr, fr_percent, fr_acumulado_percent))

    tree.pack(padx=10, pady=10, fill='both', expand=True)
    botao_gerar_grafico = tk.Button(janela_tabela, text="Gerar Gráfico", command=lambda: gerar_grafico(tabela_frequencia))
    botao_gerar_grafico.pack(pady=10)

def gerar_tabela_medidas():
    # Obter os dados do banco de dados SQLite
    conn = sqlite3.connect(r'C:\Users\Usuário\Documents\PROJETOS PYTHON\Projeto_Estatistica\Sistema_Estatistica.db')

    # Verifica se a tabela DadosMedidas existe
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='DadosMedidas';")
    tabela_existe = cursor.fetchone()

    if not tabela_existe:
        messagebox.showinfo("Erro", "Você deve enviar os dados primeiro.")
        conn.close()
        return

    dados_sqlite = pd.read_sql_query("SELECT * FROM DadosMedidas", conn)
    conn.close()

    # Verifica se há dados para calcular as medidas estatísticas
    if dados_sqlite.empty:
        messagebox.showinfo("Erro", "Não há dados para calcular as medidas estatísticas.")
        return

    # Converte todos os valores da tabela em uma única série
    valores = dados_sqlite.values.flatten()

    # Remove valores não numéricos
    valores_numericos = valores[~np.isnan(valores)]

    # Verifica se há valores numéricos
    if len(valores_numericos) == 0:
        messagebox.showinfo("Erro", "Não há valores numéricos para calcular as medidas estatísticas.")
        return

    # Calcula as medidas estatísticas para todos os valores numéricos
    media = np.mean(valores_numericos)
    modas = calcular_modas(valores_numericos)
    mediana = np.median(valores_numericos)
    quartis = np.percentile(valores_numericos, [25, 50, 75])
    iqr = quartis[2] - quartis[0]
    corte_inferior = quartis[0] - 1.5 * iqr
    corte_superior = quartis[2] + 1.5 * iqr
    maior = np.max(valores_numericos)
    menor = np.min(valores_numericos)
    desvio_padrao = np.std(valores_numericos)

    # Obtém as métricas e valores como uma lista de listas
    dados_tabela = [
        ['Média', f'{media:.2f}'],
        ['Moda', ', '.join(map(str, modas)) if modas else 'N/A'],
        ['Mediana', f'{mediana:.2f}'],
        ['Quartis (Q1, Q2, Q3)', f'{quartis[0]}, {quartis[1]}, {quartis[2]}'],
        ['IQR', f'{iqr:.2f}'],
        ['Corte Inferior', f'{corte_inferior:.2f}'],
        ['Corte Superior', f'{corte_superior:.2f}'],
        ['Maior valor', f'{maior}'],
        ['Menor valor', f'{menor}'],
        ['Desvio Padrão', f'{desvio_padrao:.2f}'],
    ]

    # Converte a lista de listas em uma tabela formatada
    tabela_formatada = tabulate(dados_tabela, headers=['Medidas', 'Valores'], tablefmt='pretty')

    # Inicia o loop principal da nova janela
    janela_tabela = Tk()
    janela_tabela.title("Tabela de Medidas Estatísticas")

    # Cria um widget de texto na nova janela
    texto_tabela = Text(janela_tabela, wrap='none', height=20, width=50)
    texto_tabela.pack(side='left', fill='both', expand=True)

    # Adiciona uma barra de rolagem
    scrollbar = Scrollbar(janela_tabela, command=texto_tabela.yview)
    scrollbar.pack(side='right', fill='y')
    texto_tabela.config(yscrollcommand=scrollbar.set)

    # Insere o texto formatado da tabela no widget de texto
    texto_tabela.insert(END, tabela_formatada)

    def gerar_box_plot():
        # Função para gerar o box plot

        # Configuração do Box Plot
        fig, ax = plt.subplots()
        ax.boxplot(valores_numericos, vert=False, widths=0.7, patch_artist=True)
        ax.set_yticklabels([])

        # Adiciona os valores numéricos no Box Plot
        for i, valor in enumerate(valores_numericos):
            ax.text(valor, 1, f'{valor:.2f}', va='center', ha='center', color='white')

        ax.set_title("Box Plot das Medidas")

        # Exibe o Box Plot na janela
        canvas = FigureCanvasTkAgg(fig, master=janela_tabela)
        canvas.draw()
        canvas.get_tk_widget().pack()

    # Adiciona um botão para gerar o box plot
    botao_box_plot = Button(janela_tabela, text="Gerar Box Plot", command=gerar_box_plot)
    botao_box_plot.pack()

    # Inicia o loop principal da nova janela
    janela_tabela.mainloop() 

def calcular_modas(valores):
    contagem = {}
    for valor in valores:
        contagem[valor] = contagem.get(valor, 0) + 1

    modas = [valor for valor, freq in contagem.items() if freq == max(contagem.values())]
    return modas

def gerar_grafico(tabela_frequencia):
    # Criar uma figura com um tamanho maior
    fig, ax = plt.subplots(figsize=(10, 6))

    # Criar uma nova coluna 'Intervalo_str' diretamente do objeto Interval
    tabela_frequencia['Intervalo_str'] = tabela_frequencia['Intervalo'].apply(lambda x: f"{x.left:.2f} - {x.right:.2f}" if isinstance(x, pd._libs.interval.Interval) else str(x))

    # Plotar o histograma excluindo a barra correspondente ao total
    tabela_sem_total = tabela_frequencia[tabela_frequencia['Intervalo_str'] != 'Total']
    ax.bar(tabela_sem_total['Intervalo_str'], tabela_sem_total['Fr(%)'], width=0.8, align='center', alpha=0.7)

    # Adicionar rótulos e título
    ax.set_xlabel('Intervalo')
    ax.set_ylabel('Fr(%)')
    ax.set_title('Histograma de Frequência Relativa Acumulada')

    # Rotacionar os rótulos do eixo x para melhor legibilidade
    plt.xticks(rotation=45, ha="right")

    # Ajustar o layout para garantir que todos os elementos do gráfico sejam visíveis
    fig.tight_layout()

    # Adicionar a barra de rolagem para o gráfico
    canvas = FigureCanvasTkAgg(fig, master=tk.Toplevel())
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(side=tk.TOP, fill=tk.BOTH, expand=1)

def calcular_probabilidade_binomial(janela_pai):
    def calcular():
        n = int(entry_n.get())
        p = float(entry_p.get().replace(',', '.'))

        # Limpar a tabela antes de atualizar
        for row in tree.get_children():
            tree.delete(row)

        # Preencher a tabela com os ensaios e probabilidades
        for k in range(n + 1):
            prob = calcular_prob_binomial(n, k, p)
            prob_formatada = "{:.4f}".format(prob)
            tree.insert("", "end", values=(k, prob_formatada))

    def calcular_prob_binomial(n, k, p):
        return comb(n, k) * (p**k) * ((1 - p)**(n - k))

    def mostrar_probabilidade_acumulada(event, n, p):
        items_selecionados = tree.selection()

        if items_selecionados:
            prob_acumulada = 0
            for item in items_selecionados:
                ensaio_selecionado = tree.item(item, 'values')
                if ensaio_selecionado and ensaio_selecionado[0] is not None:
                    ensaio = int(ensaio_selecionado[0])
                    prob_acumulada += calcular_prob_binomial(n, ensaio, p)

            # Exibir probabilidade acumulada em percentual
            prob_acumulada_percentual = prob_acumulada * 100
            label_resultado["text"] = f'Probabilidade acumulada: {prob_acumulada_percentual:.2f}%'
        else:
            label_resultado["text"] = "Selecione pelo menos um ensaio na tabela."

    janela_prob_binomial = Toplevel(janela_pai)
    janela_prob_binomial.title("Calculadora de Probabilidade Binomial")

    label_n = Label(janela_prob_binomial, text="n (Número de Ensaios):")
    label_n.grid(row=0, column=0, padx=10, pady=5)
    entry_n = Entry(janela_prob_binomial)
    entry_n.grid(row=0, column=1, padx=10, pady=5)

    label_p = Label(janela_prob_binomial, text="p (Probabilidade de Sucesso em um Ensaio):")
    label_p.grid(row=1, column=0, padx=10, pady=5)
    entry_p = Entry(janela_prob_binomial)
    entry_p.grid(row=1, column=1, padx=10, pady=5)

    btn_calcular = Button(janela_prob_binomial, text="Calcular Probabilidade", command=calcular)
    btn_calcular.grid(row=2, column=0, columnspan=2, pady=10)

    # Tabela para exibir os ensaios e probabilidades
    tree = ttk.Treeview(janela_prob_binomial, columns=("Ensaio", "Probabilidade"), show="headings")
    tree.heading("Ensaio", text="Ensaio")
    tree.heading("Probabilidade", text="Probabilidade")
    tree.grid(row=3, column=0, columnspan=2, pady=10)

    # Associar a função de mostrar_probabilidade_acumulada ao evento de seleção na árvore
    tree.bind("<ButtonRelease-1>", lambda event: mostrar_probabilidade_acumulada(event, int(entry_n.get()), float(entry_p.get().replace(',', '.'))))

    # Rótulo para exibir o resultado da probabilidade acumulada
    label_resultado = Label(janela_prob_binomial, text="")
    label_resultado.grid(row=4, column=0, columnspan=2, pady=10)

    janela_prob_binomial.mainloop()

def apagar_tabelas(conexao):
    try:
        # Lista de tabelas a serem apagadas
        tabelas_a_apagar = ['DadosPareto', 'DadosNaoPareto', 'DadosMedidas']

        # Obtém a lista de tabelas no banco de dados
        cursor = conexao.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tabelas = cursor.fetchall()
        tabelas = [tabela[0] for tabela in tabelas]

        # Itera sobre as tabelas e apaga aquelas que estão na lista 'tabelas_a_apagar'
        for tabela in tabelas_a_apagar:
            if tabela in tabelas:
                cursor.execute(f"DROP TABLE IF EXISTS {tabela};")
                print(f'Tabela {tabela} apagada.')

        conexao.commit()        
        cursor.close()

        
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao apagar tabelas: {str(e)}")

def confirmar_sair(conexao, janela_opcoes):
    resposta = messagebox.askyesno("Confirmação", "Se você sair, todos os dados serão apagadas. Deseja continuar?")
    if resposta:
        # Chama a função para apagar tabelas
        apagar_tabelas(conexao)

        # Mostra a mensagem e fecha a janela de opções
        messagebox.showinfo("Aviso", "Dados apagados! Você saiu.")
        janela_opcoes.destroy()