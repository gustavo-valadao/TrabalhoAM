from datetime import datetime
import os
import pandas as pd
import matplotlib.pyplot as plt

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




def registrar_log_inicial(mensagem, usuario):
    datahora = datetime.now().strftime("%d/%m/%y  %H:%M:%S")
    log = f"\n[{datahora}] {usuario}: {mensagem}\n"
    

    with open("log.txt", "a", encoding="utf-8") as f:
        f.write(log)



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
            registrar_log(f"Erro: {fnf}")  
            print(f"Erro: {fnf}\n")

        except ValueError as ve:
            registrar_log(f"Erro: {ve}")  
            print(f"Erro: {ve}\n")

        except Exception as e:
            registrar_log(f"Erro inesperado: {e}")
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

    



def fazer_limpeza_dataframe(dataFrame):
    while True:
        try:
            resposta = input('Para continuar devemos alguns tratamentos nos dados. Digite qualquer coisa para continuar: ')

            if not resposta:
                raise ValueError("Nada foi digitado.")

            registrar_log(f"Usuário confirmou a limpeza dos dados digitando a seguinte mensagem: {resposta}")  

            dataFrame = limpeza_educacao_pais(dataFrame)
            dataFrame = limpeza_attendance(dataFrame)

            return dataFrame


        except ValueError as ve:
            registrar_log(f"Erro: {ve}")  
            print(f"Erro: {ve}\n")




def limpeza_educacao_pais(dataFrame):


    quantidade_antes = len(dataFrame)

    dataFrame = dataFrame.dropna(subset=['Parent_Education_Level'])

    quantidade_depois = len(dataFrame)

    print(f"\nForam removidas {quantidade_antes - quantidade_depois} linhas em que o nível de educação dos pais estava vazio. Agora o arquivo possui {quantidade_depois} registros")
    registrar_log(f"Foram removidas {quantidade_antes - quantidade_depois} linhas em que o nível de educação dos pais estava vazio. Agora o arquivo possui {quantidade_depois} registros")

    return dataFrame



def limpeza_attendance(dataFrame):

    quantidade_nulos = dataFrame['Attendance (%)'].isna().sum()
    mediana_attendance = dataFrame['Attendance (%)'].median()

    if quantidade_nulos > 0:
        dataFrame['Attendance (%)'] = dataFrame['Attendance (%)'].fillna(mediana_attendance)
        print(f"Foram preenchidos {quantidade_nulos} valores nulos na coluna 'Attendance (%)' com a mediana: {mediana_attendance:.2f}")
        registrar_log(f"Foram preenchidos {quantidade_nulos} valores nulos na coluna 'Attendance (%)' com a mediana: {mediana_attendance:.2f}")
    
    else:
        print(f"Tentou-se tratar a coluna de Frequência (Attendance), substituindo os valores nulos pela mediana {mediana_attendance:.2f}. Entretanto, não foram encontrados valores nulos.")
        registrar_log(f"Tentou-se tratar a coluna de Frequência (Attendance), substituindo os valores nulos pela mediana {mediana_attendance:.2f}. Entretanto, não foram encontrados valores nulos.")


    qtd_attendance = len(dataFrame['Attendance (%)'])
    soma_attendance = dataFrame['Attendance (%)'].sum()

    print(f"Feito o tratamento, a coluna de Frequência (Attendance) agora possui {qtd_attendance} registros, que somados registram o valor {soma_attendance:.1f}.")

    return dataFrame



def grafico_dispersao_sono_x_nota_final(dataFrame):
    try:

        if "Sleep_Hours_per_Night" not in dataFrame.columns or "Total_Score" not in dataFrame.columns:
            raise KeyError("Colunas necessárias não encontradas no DataFrame.")


        plt.scatter(dataFrame["Sleep_Hours_per_Night"], dataFrame["Total_Score"], color="blue")
        plt.title("Relação entre Horas de Sono e Nota Final")
        plt.xlabel("Horas de Sono")
        plt.ylabel("Nota Final")
        plt.grid(True)
        plt.show()

        registrar_log("Gráfico de dispersão (sono x nota final) gerado com sucesso.")


    except KeyError as ke:
        print(f"Erro: {ke}")
        registrar_log(f"Erro ao gerar gráfico: {ke}")




def grafico_barras_idade_x_media_intermediaria(dataFrame):
    try:

        if "Age" not in dataFrame.columns or "Midterm_Score" not in dataFrame.columns:
            raise KeyError("Colunas 'Age' e/ou 'Midterm_Score' não encontradas no DataFrame.")

       
        media_notas_por_idade = dataFrame.groupby("Age")["Midterm_Score"].mean()

        media_notas_por_idade.plot(kind="bar", color="cornflowerblue", edgecolor="black")

        plt.title("Média das Notas Intermediárias por Idade")
        plt.xlabel("Idade")
        plt.ylabel("Média das Notas (Midterm_Score)")
        plt.grid(axis="y", linestyle="--", alpha=0.6)
        plt.tight_layout()
        plt.show()

        registrar_log("Gráfico de barras (idade x média das notas intermediárias) gerado com sucesso.")

    except KeyError as ke:
        print(f"Erro: {ke}")
        registrar_log(f"Erro ao gerar gráfico de barras: {ke}")


def grafico_pizza_idades(dataFrame):
    try:
        if "Age" not in dataFrame.columns:
            raise KeyError("A coluna 'Age' não foi encontrada no DataFrame.")

        def categorizar_idade(idade):
            if idade <= 17:
                return "Até 17"
            elif 18 <= idade <= 21:
                return "18 a 21"
            elif 22 <= idade <= 24:
                return "22 a 24"
            else:
                return "25 ou mais"


        dataFrame["Faixa_Etaria"] = dataFrame["Age"].apply(categorizar_idade)

        contagem_faixas = dataFrame["Faixa_Etaria"].value_counts().sort_index()

        plt.figure(figsize=(6, 6))
        contagem_faixas.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["#ff9999", "#66b3ff", "#99ff99", "#ffcc99"])
        plt.title("Distribuição de Alunos por Faixa Etária")
        plt.ylabel("")
        plt.tight_layout()
        plt.show()

        registrar_log("Gráfico de pizza por faixa etária gerado com sucesso.")

    except KeyError as ke:
        print(f"Erro: {ke}")
        registrar_log(f"Erro ao gerar gráfico de pizza: {ke}")



def menu_graficos(dataFrame):
    while True:
        try:
            print("\nQuais informações você deseja ver sobre os dados? Digite uma opção")
            print("1 - Calcular média, mediana, moda, desvio padrão de alguma coluna")
            print("2 - Gráfico de dispersão: Horas de Sono x Nota Final")
            print("3 - Gráfico de barras: Idade x Média das Notas Intermediárias")
            print("4 - Gráfico de pizza: Distribuição de Alunos por Faixa Etária")
            print("0 - Encerrar o programa.")

            escolha = input("Digite a opção desejada: ").strip()

            if escolha == "1":

                registrar_log("Menu de opções - Usuário digitou 1 (Calcular média, mediana, moda, desvio padrão de alguma coluna)")
                analisar_coluna(dataFrame)
            elif escolha == "2":
                registrar_log("Menu de opções - Usuário digitou 2 (gráfico de dispersão: sono x nota final)")
                grafico_dispersao_sono_x_nota_final(dataFrame)

            elif escolha == "3":
                registrar_log("Menu de opções - Usuário digitou 3 (gráfico de barras: idade x média das notas intermediárias)")
                grafico_barras_idade_x_media_intermediaria(dataFrame)

            elif escolha == "4":
                registrar_log("Menu de opções - Usuário digitou 4 (gráfico de pizza: faixa etária)")
                grafico_pizza_idades(dataFrame)

            elif escolha == "0":
                print("\nObrigado por usar nosso programa! Esperamos que tenha gostado o suficiente para ganharmos nota máxima =)")
                registrar_log("Menu de opções - Usuário digitou 0 (Encerrar o programa)")
                break

            else:
                raise ValueError("Opção inválida. Digite 0, 1, 2, 3 ou 4.")

        except ValueError as ve:
            print(f"Erro: {ve}")
            registrar_log(f"Erro no menu de gráficos: {ve}. Usuário digitou {escolha}")

        except Exception as e:
            print(f"Erro inesperado: {e}")
            registrar_log(f"Erro inesperado no menu de gráficos: {e}")



def analisar_coluna(dataFrame):
    colunas_numericas = dataFrame.select_dtypes(include='number').columns.tolist()

    if not colunas_numericas:
        print("Não há colunas numéricas para analisar.")
        return

    while True:
        print("\nColunas numéricas disponíveis:")

        for i, coluna in enumerate(colunas_numericas, start=1):
            print(f"{i} - {coluna}")
        print("99 - Voltar ao menu principal")

        try:
            escolha = input("\nDigite o número da coluna que deseja analisar: ").strip()

            if escolha == "99":
                print("Voltando ao menu principal...\n")
                registrar_log("Menu de análise de coluna - Usuário digitou 99 (voltar ao menu principal)")
                break

            escolha = int(escolha)

            if escolha < 1 or escolha > len(colunas_numericas):
                print("Número inválido. Tente novamente.")
                continue

            coluna = colunas_numericas[escolha - 1]
            print(f"\nVocê escolheu a coluna: {coluna}")

            dados = pd.to_numeric(dataFrame[coluna], errors='coerce').dropna()

            media = dados.mean()
            mediana = dados.median()
            desvio_padrao = dados.std()
            moda_valor = dados.mode()[0]


            print(f"\nAnálise da coluna '{coluna}':")
            print(f"Média: {media:.2f}")
            print(f"Mediana: {mediana:.2f}")
            print(f"Moda: {moda_valor}")
            print(f"Desvio padrão: {desvio_padrao:.2f}")

            registrar_log(f"Analisada a coluna '{coluna}': Média={media:.2f}, Mediana={mediana:.2f}, Moda={moda_valor}, Desvio Padrão={desvio_padrao:.2f}")

        except ValueError:
            print("Por favor, digite um número válido.")
        except Exception as e:
            print(f"Ocorreu um erro ao analisar a coluna: {e}")
            registrar_log(f"Erro ao analisar a coluna: {e}")



# ===========================================================================================


registrar_log_inicial(f"Programa iniciado.", "Sistema")  

nomeUsuario = pedir_nome()  

registrar_log(f"O nome fornecido pelo usuário é : {nomeUsuario}")  

print(f"\nOlá, {nomeUsuario}! Vamos começar.\n")

caminho = pedir_caminho_arquivo()

df = carregar_dataframe()

exibir_resumo_dataframe(df)

df = fazer_limpeza_dataframe(df)

menu_graficos(df)

