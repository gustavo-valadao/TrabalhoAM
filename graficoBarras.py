import pandas as pd
import matplotlib.pyplot as plt

# Carrega o CSV com os dados
df = pd.read_csv("Students_Grading_Dataset.csv")

# Agrupa por idade e calcula a média do Midterm_Score
media_notas_por_idade = df.groupby("Age")["Midterm_Score"].mean()

# Cria o gráfico de barras
media_notas_por_idade.plot(kind="bar", color="cornflowerblue", edgecolor="black")

# Personalização
plt.title("Média das Notas Intermediárias por Idade")
plt.xlabel("Idade")
plt.ylabel("Média das Notas (Midterm_Score)")
plt.grid(axis="y", linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()