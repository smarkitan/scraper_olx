import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

def scrape_data():
    url = "https://www.olx.ro/imobiliare/birouri-spatii-comerciale/bucuresti/?search%5Bdistrict_id%5D=5&search%5Bfilter_enum_alege%5D%5B0%5D=inchiriere&currency=EUR"

    # Faceți o cerere GET la pagina web
    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifică dacă cererea a avut succes
    except requests.RequestException as e:
        print(f"Eroare la cererea GET: {e}")
        return

    # Analizați conținutul HTML folosind Beautiful Soup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extrageți toate link-urile
    links = [link.get("href") for link in soup.find_all("a", {"class": "css-z3gu2d"})]
    links = ["https://www.olx.ro" + href if href and href.startswith("/d/oferta/") else href for href in links]

    # Extrageți titlurile
    titles = [title.get_text(strip=True) for title in soup.find_all("h6", class_="css-1wxaaza")]

    # Extrageți prețurile
    prices = [re.findall(r'\d+', price.get_text(strip=True).replace(" ", ""))[0] for price in soup.find_all("p", class_="css-13afqrm")]

    # Extrageți suprafețele
    areas = []
    for span in soup.find_all("span", class_="css-643j0o"):
        text = span.get_text(strip=True)
        match = re.search(r'(\d+)\s*m²', text)
        areas.append(match.group(1) if match else "N/A")

    # Asigură-te că listele au aceeași lungime
    min_length = min(len(links), len(titles), len(prices), len(areas))
    links = links[:min_length]
    titles = titles[:min_length]
    prices = prices[:min_length]
    areas = areas[:min_length]

    # Creează un DataFrame și salvează-l ca output.csv
    df = pd.DataFrame({"Link": links, "Title": titles, "Price": prices, "Area (m²)": areas})
    df.to_csv("output.csv", index=False, encoding='utf-8-sig')
