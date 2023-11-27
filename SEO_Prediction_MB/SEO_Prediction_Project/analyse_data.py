import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SEO_Prediction_Project.settings')
django.setup()

from SEO_Prediction_App.models import Data
from django.db.models import Count

def delete_duplicates():
   # Récupérer toutes les données du modèle Data
    data = Data.objects.all()

    # Créer une liste pour stocker les doublons
    doublons = []

    for i, record1 in enumerate(data):
        for j, record2 in enumerate(data):
            if i != j:  # Éviter la comparaison de l'enregistrement avec lui-même
                if record1 == record2:  # Comparaison complète des attributs
                    doublons.append(record2)

    print(f"{len(doublons)} doublons")
    
    # Supprimer les doublons
""" for doublon in doublons:
        doublon.delete()

    print(f"{len(doublons)} doublons supprimés avec succès.")"""

if __name__ == "__main__":
    delete_duplicates()
