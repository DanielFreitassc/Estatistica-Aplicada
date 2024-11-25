# Importando as bibliotecas necessárias
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Carregando o dataset
dataset = pd.read_csv("rotatividade.csv")

# Exibindo as primeiras linhas do dataset para inspecionar a estrutura
print("Dataset Original:")
print(dataset.head())

# Alterando a variável "Falta_de_Crescimento" para ter valores negativos para o teste
# Vamos fazer com que a variável "Falta_de_Crescimento" tenha um valor negativo em alguns pontos
dataset['Falta_de_Crescimento'] = dataset['Falta_de_Crescimento'] * -1  # Invertendo os valores para negativos

# Exibindo as primeiras linhas após a modificação
print("\nDataset Após Alteração para Valores Negativos em 'Falta_de_Crescimento':")
print(dataset.head())

# Plotando o gráfico para verificar a alteração no comportamento da variável
plt.figure(figsize=(10, 6))
plt.plot(dataset['Falta_de_Crescimento'], label='Falta de Crescimento', color='red')
plt.title('Comportamento de Falta de Crescimento')
plt.xlabel('Índice')
plt.ylabel('Falta de Crescimento')
plt.legend()
plt.grid(True)
plt.show()
