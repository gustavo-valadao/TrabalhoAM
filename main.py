from datetime import datetime
import os
import pandas as pd

def pedir_nome():
    while True:
        try:
            userName = input("Antes de iniciar, digite o seu nome: ").strip()

            if not userName:
                raise ValueError("O nome não pode estar vazio.")
            if any(char.isdigit() for char in userName):
                raise ValueError("O nome não deve conter números.")
            if len(userName) > 20:
                raise ValueError("O nome deve ter no máximo 20 caracteres.")

            confirmar = input(f"Você digitou '{userName}'. Está correto? (s/n): ").strip().lower()

            if confirmar == "s":
                return userName  
            elif confirmar == "n":
                print("Ok, vamos tentar de novo.\n")
            else:
                print("Resposta inválida. Por favor, digite 's' para sim ou 'n' para não.\n")

        except ValueError as e:
            print(f"Erro: {e}\n")




def registrar_log(mensagem):
    datahora = datetime.now().strftime("%d/%m/%y  %H:%M:%S")
    log = f"[{datahora}] {nomeUsuario}: {mensagem}\n"
    

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log)




def pedir_caminho_arquivo():
    while True:
        try:
            caminho = input('É necessário abrir um arquivo para continuar. Você poderá:\n > Digitar um caminho manualmente para um arquivo \n > Digitar "1" para abrir "Students_Grading_Dataset.json"\n > Digitar "2" para abrir "Students_Grading_Dataset.csv"\n').strip()
            registrar_log(f"Solicitado o caminho do arquivo. Usuário digitou: {caminho}")  

            if caminho == "1":
                caminho = "Students_Grading_Dataset.json"

            elif caminho == "2":
                caminho = "Students_Grading_Dataset.csv"

            if not os.path.isfile(caminho):
                raise FileNotFoundError("Arquivo não encontrado.")

            if not caminho.lower().endswith((".csv", ".json")):
                raise ValueError("O arquivo deve ser .csv ou .json.")

            return caminho


        except FileNotFoundError as fnf:
            registrar_log(f"Erro: {fnf}\n")  
            print(f"Erro: {fnf}\n")

        except ValueError as ve:
            registrar_log(f"Erro: {ve}\n")  
            print(f"Erro: {ve}\n")

        except Exception as e:
            registrar_log(f"Erro inesperado: {e}\n")
            print(f"Erro inesperado: {e}\n")




def carregar_dataframe():

    if caminho == "":
        return pedir_caminho_arquivo()

    if caminho.endswith(".csv"):
        df = pd.read_csv(caminho)
        registrar_log(f'Carregado o arquivo "{caminho}" para o Data Frame')
        print(f'Carregado o arquivo "{caminho}" para o Data Frame')
        return df

    else:
        df = pd.read_json(caminho)
        registrar_log(f'Carregado o arquivo "{caminho}" para o Data Frame')
        print(f'\nCarregado o arquivo "{caminho}" para o Data Frame')
        return df
    


def exibir_resumo_dataframe(dataFrame):

    print(f'\nAqui está um resumo estatístico sobre estes dados:\n ')

    print(f"Quantidade total registros: {len(dataFrame)}")
    registrar_log(f'Exibido resumo dos dados: {len(dataFrame)} registros.')


    if "Gender" in dataFrame.columns:
        quantidade_homens = 0
        quantidade_mulheres = 0


        for index, linha in dataFrame.iterrows(): 
            if linha['Gender'] == 'Male':
                quantidade_homens += 1
            elif linha['Gender'] == 'Female':
                quantidade_mulheres += 1

        print(f"Quantidade de homens: {quantidade_homens}")
        print(f"Quantidade de mulheres: {quantidade_mulheres}")
        registrar_log(f'Exibido resumo dos dados: {quantidade_homens} homens e {quantidade_mulheres} mulheres')


    if "Parent_Education_Level" in dataFrame.columns:
        registros_sem_educacao_pais = 0

        for index, linha in dataFrame.iterrows(): 
            if pd.isna(linha['Parent_Education_Level']):
                registros_sem_educacao_pais += 1


        print(f"Quantidade de registros sem dados sobre a educação dos pais: {registros_sem_educacao_pais}\n")
        registrar_log(f'Exibido resumo dos dados: {registros_sem_educacao_pais} registros sem dados sobre a educação dos pais')

    



# ===========================================================================================


nomeUsuario = pedir_nome()  

registrar_log(f"\n\nPrograma iniciado. O nome fornecido pelo usuário é : {nomeUsuario}")  

print(f"\nOlá, {nomeUsuario}! Vamos começar.\n")

caminho = pedir_caminho_arquivo()

df = carregar_dataframe()

exibir_resumo_dataframe(df)



