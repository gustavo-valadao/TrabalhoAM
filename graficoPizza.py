import pandas as pd
import matplotlib.pyplot as plt

# Carrega o CSV com os dados
df = pd.read_csv("Students_Grading_Dataset.csv")


# Função para categorizar as idades em faixas
def categorizar_idade(idade):
    if idade <= 17:
        return "Até 17"
    elif 18 <= idade <= 21:
        return "18 a 21"
    elif 22 <= idade <= 24:
        return "22 a 24"
    else:
        return "25 ou mais"

# Aplica a função para criar a nova coluna
df["Faixa_Etaria"] = df["Age"].apply(categorizar_idade)

# Conta quantos alunos estão em cada faixa
contagem_faixas = df["Faixa_Etaria"].value_counts().sort_index()

# Cria o gráfico de pizza
plt.figure(figsize=(6,6))
contagem_faixas.plot(kind="pie", autopct="%1.1f%%", startangle=90, colors=["#ff9999","#66b3ff","#99ff99","#ffcc99"])
plt.title("Distribuição de Alunos por Faixa Etária")
plt.ylabel("")  # Remove o rótulo do eixo Y
plt.tight_layout()
plt.show()
