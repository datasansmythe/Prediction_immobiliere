import pickle 
import os
import numpy as np

class predictor:
    def __init__(self, model_path: str, shap_explainer_path: str):
        # On construit les chemins par rapport au fichier predictor.py
        base_dir = os.path.dirname(os.path.abspath(__file__))

        self.model_path = os.path.join(base_dir, model_path)
        self.shap_explainer_path = os.path.join(base_dir, shap_explainer_path)

        self.model = self.load_model(self.model_path)
        self.shap_explainer = self.load_shap_explainer(self.shap_explainer_path)


    def load_model(self, model_path: str):
        if not os.path.exists(model_path):
            raise FileNotFoundError(f"Model file not found at {model_path}")
        with open(model_path, 'rb') as model_file:
            model = pickle.load(model_file)
        return model


    def predict(self, features: np.ndarray) -> np.ndarray:
        if not isinstance(features, np.ndarray):
            raise ValueError("Input features must be a numpy array")
        return self.model.predict(features)


    def load_shap_explainer(self, shap_explainer_path: str):
        if not os.path.exists(shap_explainer_path):
            raise FileNotFoundError(f"SHAP explainer not found at {shap_explainer_path}")
        with open(shap_explainer_path, 'rb') as shap_file:
            shap_explainer = pickle.load(shap_file)
        return shap_explainer
    

    def explain(self, features: np.ndarray):
        expl = self.shap_explainer(features)
        shap_values = expl[0]             
        base_value = shap_values.base_values
        return base_value, shap_values
    

def predict_and_explain(input_df):
    predictor_instance = predictor(
        model_path="catboost_regressor_simplifier.pkl",
        shap_explainer_path="shap_explainer.pkl"
    )

    features = input_df.to_numpy()
    predicted_price = predictor_instance.predict(features)[0]
    base_value, shap_values = predictor_instance.explain(input_df)
    return predicted_price, shap_values, base_value
