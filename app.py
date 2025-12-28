# app.py (à la racine)
import sys
from pathlib import Path

# sys.path.insert(0, str(Path(__file__).parent / "src"))
# from src.api.streamlit_app import main

import streamlit as st
import pandas as pd
import shap
import matplotlib.pyplot as plt
import traceback 

from src.model.predictor import predict_and_explain
from src.api.schemas import PropertyFeatures

from src.database.manager import DatabaseManager

# On initialise le manager de base de données
db = DatabaseManager()
db_active = db.init_db() # Créera la table au premier lancement de l'app

st.set_page_config(
    page_title="Prédiction des prix immobiliers",page_icon="🏡", 
    initial_sidebar_state="collapsed")

## Définition de l'API / UI
# -----------------------------

st.image("./images/images.jfif", width='stretch')
st.markdown(
    """
    <h1 style='color: #EE82EE; font-weight: bold; text-align: center;'>
        PRÉDICTION DES PRIX IMMOBILIERS AVEC EXPLICATION SHAP
    </h1>
    """, 
    unsafe_allow_html=True
)
st.markdown("Entrez les caractéristiques de la propriété pour obtenir une prédiction **du prix** et **son explication**.")

# Interface utilisateur pour les 7 features
with st.container():
    st.subheader("Caractéristiques de la Propriété",divider='rainbow')
    col1, col2, col3,  = st.columns(3)

    # Colonne 1
    with col1:
        surface_habitable = st.number_input("Surface Habitable (m²)", min_value=10.0, step=1.0, value=50.0)
        prix_m2_moyen_mois_precedent = st.number_input("Prix M² Moyen Mois Précédent (€)", min_value=1000.0, step=100.0, value=4500.0)
        nb_transactions_mois_precedent = st.number_input("Nb Transactions Mois Précédent (Zone)", min_value=0, step=1, value=50)

    # Colonne 2
    with col2:
        longitude = st.number_input("Longitude", value=2.3522, format="%.4f")
        latitude = st.number_input("Latitude", value=48.8566, format="%.4f")
        mois_transaction = st.slider("Mois de la Transaction", min_value=1, max_value=12, value=6)

    # Colonne 3 (Pour le type_batiment)
    with col3:
        # Simplification de l'interface : Demander si c'est un Appartement.
        is_appartement = st.radio("Type de Bien", options=['Appartement', 'Autre'], index=0)
        # Conversion en feature binaire 0 ou 1
        type_batiment_Appartement = 1 if is_appartement == 'Appartement' else 0
        st.write("") # Espace
        st.write("") # Espace
        
# Bouton de prédiction
if st.button("Prédire le Prix et Explication (SHAP)"):#, type="primary"
    try:
        # 1. Validation des Données avec Pydantic
        input_data = PropertyFeatures(
            surface_habitable=surface_habitable,
            prix_m2_moyen_mois_precedent=prix_m2_moyen_mois_precedent,
            longitude=longitude,
            latitude=latitude,
            nb_transactions_mois_precedent=nb_transactions_mois_precedent,
            mois_transaction=mois_transaction,
            type_batiment_Appartement=type_batiment_Appartement
        )
        
        # 2. Conversion en DataFrame pour le Modèle (dans l'ordre attendu)
        # L'ordre est crucial, assurez-vous qu'il correspond à vos features originales !
        features_dict = input_data.model_dump()
        input_df = pd.DataFrame([features_dict], columns=[
            'surface_habitable', 
            'prix_m2_moyen_mois_precedent', 
            'longitude', 
            'latitude', 
            'type_batiment_Appartement', 
            'nb_transactions_mois_precedent', 
            'mois_transaction'
        ])
        
        # 3. Prédiction et Explication
        predicted_price, shap_values, base_value = predict_and_explain(input_df)
        
        # 4. Affichage du Résultat
        st.success(f"💰 Le prix estimé est de : **{predicted_price:,.2f} €**")

        # 5. Sauvegarde automatique dans PostgreSQL
        if db_active:
            success = db.save_prediction(input_df.to_dict(), predicted_price)
            if success:
                st.caption("✅ La prédiction a été sauvegardée dans la base de données.")
        else:
            st.caption("Mode Cloud : Prédiction non enregistrée (Base de données déconnectée)")

        # 6. Affichage de l'Explication SHAP
        st.subheader("Analyse de l'Explication (SHAP)")
        st.markdown(
            "Ce graphique montre comment chaque caractéristique a contribué à pousser la prédiction "
            "(valeur de sortie) de la valeur de base (moyenne des prédictions) au prix final estimé."
        )

        fig, ax = plt.subplots(figsize=(8, 6))
        shap.plots.waterfall(shap_values, show=False)
        st.pyplot(fig)
        
    except ConnectionError as ce:
        st.error(f"Erreur de chargement du modèle : {ce}. Veuillez vérifier la présence et la validité de 'modele_final.pkl'.")
    except Exception as e:
        st.error("Une erreur s'est produite lors de la prédiction ou du calcul SHAP.")
        st.code(f"Détails de l'erreur: {e}")
        st.code(traceback.format_exc())

 