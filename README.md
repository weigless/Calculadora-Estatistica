# Calculadora Estatística em Python

Este repositório contém uma Calculadora Estatística desenvolvida em Python.

## Funcionalidades

- **Autenticação de Usuário:**
  - A aplicação inicia com uma tela de autenticação, onde o usuário deve fornecer seu nome de usuário e senha.

- **Cadastro de Usuário:**
  - Possibilidade de cadastrar novos usuários para acessar a aplicação.

- **Análise de Pareto:**
  - Geração de gráfico e tabela de análise de Pareto para visualização dos dados.

- **Visualização e Edição de Dados de Pareto:**
  - Interface para visualizar e editar os dados da tabela DadosPareto.

- **Cálculo de Tabela de Frequência:**
  - Geração automática da tabela de frequência a partir dos dados armazenados no banco de dados SQLite.

- **Cálculo de Medidas Estatísticas:**
  - Criação de uma tabela com medidas estatísticas como média, moda, mediana, quartis, IQR, corte inferior, corte superior, maior valor, menor valor e desvio padrão.

- **Cálculo de Probabilidade Binomial:**
  - Calculadora que permite a obtenção de probabilidades binomiais, exibindo uma tabela com os ensaios e suas probabilidades.

- **Limpeza de Tabelas:**
  - Funcionalidade para apagar as tabelas 'DadosPareto', 'DadosNaoPareto' e 'DadosMedidas' do banco de dados.

## Requisitos

- Python 3.x
- Bibliotecas: tkinter, sqlite3, pandas, numpy, matplotlib, tabulate

## Como Utilizar

1. **Execução:**
   - Execute o arquivo `main.py` para iniciar a aplicação.

2. **Autenticação:**
   - Na tela inicial, insira seu nome de usuário e senha para acessar a calculadora estatística.

3. **Cadastro de Usuário:**
   - Selecione a opção "Cadastrar" para criar uma nova conta de usuário.

4. **Análise de Pareto:**
   - Explore a funcionalidade de análise de Pareto para visualizar dados e gerar gráficos.

5. **Visualização e Edição de Dados de Pareto:**
   - Acesse a opção "Visualizar Dados de Pareto" para ver e editar os dados armazenados.

6. **Cálculo de Tabela de Frequência:**
   - Selecione "Gerar Tabela de Frequência" para calcular e exibir a tabela correspondente.

7. **Cálculo de Medidas Estatísticas:**
   - Escolha "Gerar Tabela de Medidas Estatísticas" para calcular e visualizar as medidas estatísticas.

8. **Cálculo de Probabilidade Binomial:**
   - Utilize a opção "Calcular Probabilidade Binomial" para acessar a calculadora de probabilidade binomial.

9. **Limpeza de Tabelas:**
   - Se necessário, utilize a função "Apagar Tabelas" para limpar o banco de dados.

10. **Encerramento:**
    - Confirme a saída da aplicação quando desejar encerrar.

## Observações

- Certifique-se de ter todas as bibliotecas necessárias instaladas antes de executar o programa.
- O arquivo de banco de dados SQLite (`Sistema_Estatistica.db`) é utilizado para armazenar dados relevantes.

---
**Nota:** Este projeto é uma aplicação de estatística, e os desenvolvedores não se responsabilizam por eventuais problemas decorrentes do uso indevido ou alterações inadequadas no código.

