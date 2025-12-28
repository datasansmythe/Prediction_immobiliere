# tests/conftest.py

import sys
import os

# Détermine le chemin absolu du répertoire racine du projet
# (le dossier qui contient 'src', 'tests', 'app.py', etc.)
# 1. os.path.dirname(__file__)  -> Répertoire 'tests/'
# 2. os.path.abspath(os.path.join(..., '..')) -> Répertoire parent (la racine C:\...\Prediction_Immobiliere)
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

# Insère ce répertoire racine au début du chemin de recherche des modules Python.
# Cela permet à Pytest de trouver et d'importer le paquet 'src'.
sys.path.insert(0, project_root)

# Si vous voulez vérifier que le chemin est ajouté (pour le débogage):
print(f"Ajout au sys.path: {project_root}")