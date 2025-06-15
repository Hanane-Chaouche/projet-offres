import os
from pathlib import Path
import pandas as pd
import unicodedata

def clean_for_latin1(s):
    return (
        unicodedata.normalize("NFKD", s)
        .encode("latin1", "replace")
        .decode("latin1")
    )

def generate_html(input_csv="data/jobs.csv", output_html="public/index.html"):
    # Correction WinError 183 : si un fichier 'public' existe, le supprimer
    if os.path.exists("public") and not os.path.isdir("public"):
        os.remove("public")
    Path("public").mkdir(parents=True, exist_ok=True)

    # Chargement des données CSV
    df = pd.read_csv(input_csv)
    # Nettoie toutes les colonnes texte
    for col in df.columns:
        df[col] = df[col].apply(lambda x: clean_for_latin1(str(x)))

    # Génération HTML
    html_content = f"""<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Offres d'emploi</title>
</head>
<body>
    <h1>Offres d'emploi en développement logiciel</h1>
    {df.to_html(index=False, render_links=True, escape=False)}
</body>
</html>
"""

    with open(output_html, "w", encoding="latin1") as f:
        f.write(html_content)

    print(f"Fichier HTML généré avec {len(df)} offres : {output_html}")

if __name__ == "__main__":
    generate_html()
