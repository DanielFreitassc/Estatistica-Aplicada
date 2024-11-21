from flask import Flask, request, jsonify
from flask_cors import CORS  # Importar a extensão CORS
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

data = pd.read_csv("rotatividade.csv")

X = data.drop(columns=["Rotatividade"])
y = data["Rotatividade"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LinearRegression()
model.fit(X_train, y_train)

app = Flask(__name__)

CORS(app) 

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()

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

        input_data = pd.DataFrame([data])

        prediction = model.predict(input_data)[0]

        return jsonify({
            "input": data,
            "rotatividade_prevista": round(prediction, 2)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
