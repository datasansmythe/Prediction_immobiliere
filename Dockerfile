# Utilise l'image officielle Python
FROM python:3.13-slim

# Définit le dossier de travail dans le conteneur
WORKDIR /app

# Installe les dépendances système nécessaires pour psycopg2 (Base de données)
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copie le fichier des dépendances
COPY requirements.txt .

# Installe les bibliothèques Python
RUN pip install --no-cache-dir -r requirements.txt

# Copie tout le reste de ton code (src, app.py, etc.)
COPY . .

# Hugging Face utilise le port 7860 par défaut
EXPOSE 7860

# Commande pour lancer l'application
CMD ["streamlit", "run", "app.py", "--server.port=7860", "--server.address=0.0.0.0"]