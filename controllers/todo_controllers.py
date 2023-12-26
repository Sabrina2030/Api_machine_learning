from models import Prediction_Input, Prediction_Output
from fastapi import HTTPException

import joblib

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

class PredictionController:
    def __init__(self):
        try:
            # Cargar el conjunto de datos
            df = pd.read_csv("Pulsar.csv")

            # Dividir los datos en características (X) y etiquetas (y)
            X = df.drop("Class", axis=1)
            y = df["Class"]

            # Dividir los datos en conjuntos de entrenamiento y prueba
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

            # Inicializar y entrenar el modelo de Árbol de Decisión
            decision_tree_model = DecisionTreeClassifier(random_state=42)
            decision_tree_model.fit(X_train, y_train)

            # Guardar el modelo
            joblib.dump(decision_tree_model, "decision_tree_model.joblib")

            # Cargar el modelo
            self.model = joblib.load("decision_tree_model.joblib")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Error al cargar el modelo: {str(e)}")

        self.predictions = []

    def get_predictions(self) -> list[Prediction_Output]:
        return [Prediction_Output(**prediction) for prediction in self.predictions]

    def get_prediction(self, prediction_id: int) -> Prediction_Output:
        for prediction in self.predictions:
            if int(prediction["id"]) == prediction_id:
                return Prediction_Output(**prediction)
        raise HTTPException(status_code=404, detail="Predicción no encontrada")

    def delete_prediction(self, prediction_id: int):
        try:
            index_to_remove = next(
                i for i, prediction in enumerate(self.predictions) if int(prediction["id"]) == prediction_id
            )
            self.predictions.pop(index_to_remove)
            return {"message": "Predicción eliminada exitosamente"}
        except StopIteration:
            raise HTTPException(status_code=404, detail="Predicción no encontrada")

    def create_prediction(self, pred_input: Prediction_Input) -> Prediction_Output:
        # Convertir la entrada a una lista de flotantes
        input_values = [float(value) for value in pred_input.text_input]

        # Realizar la predicción
        prediction = {
            "id": str(len(self.predictions) + 1),
            "text_input": pred_input.text_input,
            "pred": float(self.model.predict([input_values])[0])
        }
        self.predictions.append(prediction)
        return Prediction_Output(**prediction)


