"Chrome/114.0.0.0 Safari/537.36"
import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import os
import logging

# Configurer le logging
LOG_DIR = Path("logs")
LOG_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOG_DIR / "log.txt",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/114.0.0.0 Safari/537.36"
    )
}


def scrape_hackernews():
    """Scrape les offres HackerNews et retourne une liste de dictionnaires."""
    url = "https://news.ycombinator.com/jobs"
    offers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for row in soup.find_all("tr", class_="athing"):
            a = row.find("a")
            if a and "item?id=" in a.get("href", ""):
                offers.append({
                    "Source": "HackerNews",
                    "Titre": a.text.strip(),
                    "Entreprise": "N/A",
                    "Lien": "https://news.ycombinator.com/" + a["href"]
                })
    except Exception as e:
        logging.error("Erreur HackerNews: %s", e)
    return offers


def scrape_python_jobs():
    """Scrape les offres Python.org et retourne une liste de dictionnaires."""
    url = "https://www.python.org/jobs/"
    offers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for job in soup.select(".list-recent-jobs li"):
            title = job.h2.text.strip()
            company = job.find("span", class_="listing-company-name").text.strip()
            link = "https://www.python.org" + job.h2.a["href"]
            offers.append({
                "Source": "Python.org",
                "Titre": title,
                "Entreprise": company,
                "Lien": link
            })
    except Exception as e:
        logging.error("Erreur Python.org: %s", e)
    return offers


def scrape_jsremotely():
    """Scrape les offres JSRemotely et retourne une liste de dictionnaires."""
    url = "https://jsremotely.com/"
    offers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for div in soup.find_all("div", class_="job"):
            a = div.find("a")
            if a:
                title = a.text.strip()
                link = "https://jsremotely.com" + a["href"]
                offers.append({
                    "Source": "JSRemotely",
                    "Titre": title,
                    "Entreprise": "N/A",
                    "Lien": link
                })
    except Exception as e:
        logging.error("Erreur JSRemotely: %s", e)
    return offers


def scrape_remotive():
    """Scrape les offres Remotive et retourne une liste de dictionnaires."""
    url = "https://remotive.io/api/remote-jobs?category=software-dev"
    offers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        if res.status_code == 200:
            jobs = res.json().get("jobs", [])
            for job in jobs:
                offers.append({
                    "Source": "Remotive",
                    "Titre": job["title"],
                    "Entreprise": job["company_name"],
                    "Lien": job["url"]
                })
        else:
            logging.error("Erreur Remotive: statut %s", res.status_code)
    except Exception as e:
        logging.error("Erreur Remotive: %s", e)
    return offers


def scrape_workingnomads():
    """Scrape les offres WorkingNomads et retourne une liste de dictionnaires."""
    url = "https://www.workingnomads.com/jobs"
    offers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for li in soup.select("div#jobsboard > a"):
            title = li.find("h3")
            company = li.find("h4")
            if title and company:
                offers.append({
                    "Source": "WorkingNomads",
                    "Titre": title.text.strip(),
                    "Entreprise": company.text.strip(),
                    "Lien": "https://www.workingnomads.com" + li["href"]
                })
    except Exception as e:
        logging.error("Erreur WorkingNomads: %s", e)
    return offers


def scrape_authenticjobs():
    """Scrape les offres AuthenticJobs et retourne une liste de dictionnaires."""
    url = "https://authenticjobs.com/"
    offers = []
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "lxml")
        for job in soup.select(".job-listing"):
            title_tag = job.find("h4")
            company_tag = job.find("h5")
            a_tag = job.find("a", href=True)
            if title_tag and a_tag:
                offers.append({
                    "Source": "AuthenticJobs",
                    "Titre": title_tag.text.strip(),
                    "Entreprise": company_tag.text.strip() if company_tag else "N/A",
                    "Lien": "https://authenticjobs.com" + a_tag["href"]
                })
    except Exception as e:
        logging.error("Erreur AuthenticJobs: %s", e)
    return offers


def main():
    """Point d'entrée principal pour l'extraction multi-sources et l'enregistrement CSV."""
    logging.info("Scraping multi-sources en cours...")

    all_offers = []
    all_offers += scrape_hackernews()
    all_offers += scrape_python_jobs()
    all_offers += scrape_jsremotely()
    all_offers += scrape_remotive()
    all_offers += scrape_workingnomads()
    all_offers += scrape_authenticjobs()

    df = pd.DataFrame(all_offers)
    data_path = Path("data")
    # Si "data" existe déjà sous forme de fichier, on le supprime
    if data_path.exists() and not data_path.is_dir():
        os.remove(data_path)

    # Créer automatiquement le dossier data/
    data_path.mkdir(parents=True, exist_ok=True)

    # Enregistrer dans le bon dossier
    df.to_csv(data_path / "jobs.csv", index=False, encoding="utf-8")

    logging.info("Fichier jobs.csv généré avec %d offres d'emploi.", len(df))


if __name__ == "__main__":
    main()
