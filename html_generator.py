import pandas as pd
from pathlib import Path
import os

def generate_html(input_csv="data/jobs.csv", output_html="public/index.html"):
    # Lire les offres depuis le fichier CSV
    df = pd.read_csv(input_csv)

    # Créer le dossier 'public/' s'il n'existe pas
    Path("public").mkdir(parents=True, exist_ok=True)

    # Générer un tableau HTML depuis le DataFrame
    html_table = df.to_html(index=False, escape=False, render_links=True, classes="job-table")

    # Contenu HTML complet
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Offres d'emploi</title>
    <style>
        body {{ font-family: Arial, sans-serif; padding: 20px; }}
        h1 {{ text-align: center; }}
        table.job-table {{ width: 100%; border-collapse: collapse; margin-top: 20px; }}
        table.job-table th, table.job-table td {{ border: 1px solid #ccc; padding: 8px; }}
        table.job-table th {{ background-color: #f2f2f2; }}
        tr:nth-child(even) {{ background-color: #f9f9f9; }}
    </style>
</head>
<body>
    <h1>Offres d'emploi en développement logiciel</h1>
    {html_table}
</body>
</html>
"""
    if os.path.exists("public") and not os.path.isdir("public"):
        os.remove("public")
    Path("public").mkdir(parents=True, exist_ok=True)

    # Écrire le HTML dans public/index.html
    with open(output_html, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"Fichier HTML généré avec {len(df)} offres : {output_html}")

# Lancer automatiquement si on exécute le script
if __name__ == "__main__":
    generate_html()
