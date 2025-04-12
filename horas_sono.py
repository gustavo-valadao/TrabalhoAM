import pandas as pd
import matplotlib.pyplot as plt

# Carrega o CSV com os dados
df = pd.read_csv("Students_Grading_Dataset.csv")

# Cria o gráfico de dispersão
plt.scatter(df["Sleep_Hours_per_Night"], df["Total_Score"], color="blue")

# Adiciona título e rótulos
plt.title("Relação entre Horas de Sono e Nota Final")
plt.xlabel("Horas de Sono")
plt.ylabel("Nota Final")

# Exibe o gráfico
plt.grid(True)
plt.show()