import pytest
import pandas as pd
import numpy as np
import os
import shap
from pathlib import Path


# Importez la fonction de prédiction de votre modèle
from src.model.predictor import predict_and_explain
from src.model.predictor import predictor
 
# Données d'entrée valides pour le test
VALID_INPUT_DATA = {
    'surface_habitable': [55.0],
    'prix_m2_moyen_mois_precedent': [4200.0],
    'longitude': [2.35],
    'latitude': [48.85],
    'type_batiment_Appartement': [1],
    'nb_transactions_mois_precedent': [45],
    'mois_transaction': [7]
}
VALID_DF = pd.DataFrame(VALID_INPUT_DATA)

# --------------------------
# Tests de Chargement et de Fonctionnalité du Modèle
# --------------------------

def test_model_file_exists():
    """Vérifie si le fichier modèle est présent à l'emplacement attendu."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. On remonte d'un niveau (..) puis on va dans src/model/
    model_path = os.path.abspath(os.path.join(
        current_dir, '..', 'src', 'model', 'catboost_regressor_simplifier.pkl'
    ))
    
    # Debug optionnel : décommentez pour voir le chemin calculé dans le terminal
    print(f"\nChemin testé : {model_path}")

    # 3. L'assertion (le vrai test)
    assert os.path.exists(model_path), f"Le fichier est introuvable ici : {model_path}"


@pytest.fixture
def my_predictor():
    """Prépare une instance de predictor pour tous les tests."""
    return predictor(
        model_path='catboost_regressor_simplifier.pkl', 
        shap_explainer_path='shap_explainer.pkl'
    )

def test_model_not_none(my_predictor):
    assert my_predictor.model is not None

def test_prediction_type(my_predictor):
    assert my_predictor.shap_explainer is not None


def test_prediction_returns_valid_output():
    """Teste si la fonction de prédiction retourne une valeur de prix valide (float positif)."""
    
    # 1. Effectuer la prédiction et l'explication
    prediction, shap_values, base_value = predict_and_explain(VALID_DF)
    
    # 2. Vérification du Prix (Prediction)
    assert isinstance(prediction, (float, np.floating))
    assert prediction > 10000.0 # Vérifiez que le prix est réaliste (plus grand qu'un minimum)
    
    # 3. Vérification des Valeurs SHAP
    assert len(shap_values) == len(VALID_DF.columns) 
    assert isinstance(shap_values, (np.ndarray, shap.Explanation))
    
    # 4. Vérification de la Base Value (Expected Value)
    assert isinstance(base_value, (float, np.floating))

 