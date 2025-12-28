from pydantic import BaseModel, Field

class PropertyFeatures(BaseModel):
    """Schéma Pydantic pour les caractéristiques d'une propriété, incluant la feature encodée."""
    
    # Features numériques
    surface_habitable: float = Field(
        ..., 
        gt=10.0, 
        description="Surface habitable de la propriété en mètres carrés (doit être supérieure à 10)."
    )
    prix_m2_moyen_mois_precedent: float = Field(
        ..., 
        gt=1000.0, 
        description="Prix moyen au m² dans la zone le mois précédent."
    )
    longitude: float = Field(
        ..., 
        description="Coordonnée géographique de la longitude."
    )
    latitude: float = Field(
        ..., 
        description="Coordonnée géographique de la latitude."
    )
    nb_transactions_mois_precedent: int = Field(
        ..., 
        ge=0, 
        description="Nombre de transactions immobilières enregistrées le mois précédent dans la zone."
    )
    mois_transaction: int = Field(
        ..., 
        ge=1, 
        le=12,
        description="Mois de l'année où la transaction a eu lieu (1 pour Janvier à 12 pour Décembre)."
    )
    
    # Feature Binaire/Encodée (One-Hot Encoder)
    # Puisque 'type_batiment_Appartement' est un résultat d'encodage, 
    # nous le demandons comme une valeur binaire (0 ou 1).
    type_batiment_Appartement: int = Field(
        ..., 
        ge=0,
        le=1,
        description="1 si le bien est un appartement, 0 sinon."
    )