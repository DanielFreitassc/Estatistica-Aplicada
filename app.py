from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar a extensão CORS
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Carregar os dados
data = pd.read_csv("rotatividade.csv")

# Separar os dados em variáveis independentes (X) e dependente (y)
X = data.drop(columns=["Rotatividade"])
y = data["Rotatividade"]

# Normalizar os dados de entrada
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Dividir os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X_scaled, y, test_size=0.2, random_state=42)

# Criar o modelo de regressão linear e treinar
model = LinearRegression()
model.fit(X_train, y_train)

# Configurar a aplicação Flask
app = Flask(__name__)

CORS(app)  # Permitir requisições CORS
from sklearn.metrics import mean_squared_error, r2_score

# Fazer previsões com os dados de teste
y_pred = model.predict(X_test)

# Calcular o erro quadrático médio (MSE) e o R²
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"MSE: {mse}")
print(f"R²: {r2}")

for feature, coef in zip(X.columns, model.coef_):
    print(f"Coeficiente para {feature}: {coef}")
    
@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

        # Verificar se todos os campos obrigatórios estão presentes
        required_fields = [
            "Ambiente_Toxico",
            "Salario_Insatisfatorio",
            "Falta_de_Crescimento",
            "Carga_Horaria_Excessiva",
            "Gestao_Inefetiva"
        ]
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Campo '{field}' é obrigatório"}), 400

        # Converter os dados de entrada para um DataFrame
        input_data = pd.DataFrame([data])

        # Normalizar os dados de entrada (aplicar a mesma transformação feita no treinamento)
        input_data_scaled = scaler.transform(input_data)

        # Fazer a previsão
        prediction = model.predict(input_data_scaled)[0]

        # Converter o valor para porcentagem, garantir que o valor esteja entre 0% e 100%
        rotatividade_percent = min(max(round(prediction, 2), 0), 100)

        return jsonify({
            "input": data,
            "rotatividade_prevista": f"{rotatividade_percent}%"
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Rodar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True, port=8080)
