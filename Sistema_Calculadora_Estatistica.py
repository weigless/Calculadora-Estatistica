''' 
TRABALHO DE ESTATÍSTICA APLICADA
PROFº LUIZ CARLOS

DESENVOLVEDORES: David Souza e Weigless Camargo

***** CALCULADORA ESTATÍSTICA *****

'''

from tkinter import Tk, Label, Entry, Button, StringVar, messagebox, font, Toplevel, ttk
import sqlite3
from funcoes import fazer_login, cadastrar_usuario, verificar_login, abrir_tela_cadastro, cadastrar_e_notificar_usuario



def main():
    caminho_banco_dados = r'C:\Users\Usuário\Documents\PROJETOS PYTHON\Projeto_Estatistica\Sistema_Estatistica.db'
    conexao = sqlite3.connect(caminho_banco_dados)

    janela = Tk()
    janela.title("Autenticação")
    janela.geometry("400x200")

    fonte = font.Font(size=12)

    Label(janela, text="Usuário", font=fonte).grid(row=0, pady=5)
    Label(janela, text="Senha", font=fonte).grid(row=1, pady=5)

    usuario_var = StringVar()
    senha_var = StringVar()

    Entry(janela, textvariable=usuario_var, font=fonte, width=20).grid(row=0, column=1, padx=10, pady=5)
    Entry(janela, textvariable=senha_var, show='*', font=fonte, width=20).grid(row=1, column=1, padx=10, pady=5)

    Button(janela, text="Entrar", command=lambda: verificar_login(janela, conexao, usuario_var, senha_var), font=fonte).grid(row=2, column=0, pady=10)

    Button(janela, text="Cadastrar", command=lambda: abrir_tela_cadastro(janela, conexao, fonte, usuario_var, senha_var), font=fonte).grid(row=2, column=1, pady=10)

    janela.mainloop()

if __name__ == "__main__":
    main()
