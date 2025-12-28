---
title: Prediction Immobiliere
emoji: 🏙️
colorFrom: blue
colorTo: green
sdk: streamlit
sdk_version: 1.41.0
python_version: 3.13
app_file: app.py
pinned: false
---

# 🏙️ Prédiction du Prix de l'Immobilier

Ce projet est une application de Machine Learning permettant d'estimer le prix d'un bien immobilier en fonction de ses caractéristiques (surface, localisation, type de bâtiment, etc.). 

## 🚀 Fonctionnalités
- **Interface Streamlit** : Saisie facile des données et visualisation immédiate.
- **Modèle CatBoost** : Prédictions précises basées sur un algorithme de Gradient Boosting.
- **Explicabilité (SHAP)** : Comprenez pourquoi l'IA a donné ce prix grâce à l'analyse de l'importance des variables.
- **Persistance des données** : Historisation des prédictions dans une base PostgreSQL (via Docker).
- **CI/CD** : Déploiement automatique vers Hugging Face Spaces via GitHub Actions.

### 🛠️ Installation et Utilisation (Local avec Docker)

1. **Cloner le projet** :
   ```bash
   git clone [https://github.com/datasansmythe/Prediction_immobiliere.git](https://github.com/datasansmythe/Prediction_immobiliere.git)
   cd Prediction-Immobiliere
   ```
2. **Lancer avec Docker Compose :**
```bash
docker-compose up --build
```

3. 🧪 Tests
```bash
pytest
```
#### 🏗️ Architecture Technique
- Backend : Python 3.13
- ML Stack : CatBoost, SHAP, Pandas
- Base de données : PostgreSQL
- Conteneurisation : Docker & Docker Compose
- Déploiement : Hugging Face Spaces & GitHub Actions
