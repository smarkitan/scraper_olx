import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

url = "https://www.olx.ro/imobiliare/birouri-spatii-comerciale/bucuresti/?search%5Bdistrict_id%5D=5&search%5Bfilter_enum_alege%5D%5B0%5D=inchiriere&currency=EUR"

# Faceți o cerere GET la pagina web
try:
    response = requests.get(url)
    response.raise_for_status()  # Verifică dacă cererea a avut succes
except requests.RequestException as e:
    print(f"Eroare la cererea GET: {e}")
    exit()

# Analizați conținutul HTML folosind Beautiful Soup
soup = BeautifulSoup(response.content, "html.parser")

# Extrageți toate link-urile care încep cu "href="
links = []
for link in soup.find_all("a", {"class": "css-z3gu2d"}):
    href = link.get("href")
    if href and href.startswith("/d/oferta/"):
        links.append("https://www.olx.ro" + href)
    elif href:
        links.append(href)

# Extrageți toate titlurile cu clasa "css-1wxaaza"
titles = [title.get_text(strip=True) for title in soup.find_all("h6", class_="css-1wxaaza")]

# Extrageți toate prețurile cu clasa "css-13afqrm"
prices = []
for price in soup.find_all("p", class_="css-13afqrm"):
    text = price.get_text(strip=True).replace(" ", "")
    match = re.findall(r'\d+', text)
    if match:
        prices.append(match[0])
    else:
        prices.append("N/A")

# Extrageți suprafețele (m²) cu clasa "css-643j0o"
areas = []
for span in soup.find_all("span", class_="css-643j0o"):
    text = span.get_text(strip=True)
    match = re.search(r'(\d+)\s*m²', text)
    if match:
        areas.append(match.group(1))
    else:
        areas.append("N/A")

# Afișează lungimile pentru depanare
print("Numărul de link-uri găsite:", len(links))
print("Numărul de titluri găsite:", len(titles))
print("Numărul de prețuri găsite:", len(prices))
print("Numărul de suprafețe găsite:", len(areas))

# Asigură-te că listele au aceeași lungime
min_length = min(len(links), len(titles), len(prices), len(areas))

# Truncatează listele la aceeași lungime
links = links[:min_length]
titles = titles[:min_length]
prices = prices[:min_length]
areas = areas[:min_length]

# Creează un DataFrame cu link-urile, titlurile, prețurile și suprafețele
df = pd.DataFrame({"Link": links, "Title": titles, "Price": prices, "Area (m²)": areas})

# Afișează DataFrame-ul
print(df)

# Salvează DataFrame-ul într-un fișier CSV cu codificare utf-8
df.to_csv("output.csv", index=False, encoding='utf-8-sig')

# Afișează un mesaj pentru a confirma că fișierul a fost salvat
print("Fișierul a fost salvat în output.csv")
