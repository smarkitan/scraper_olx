import requests
import pandas as pd
from bs4 import BeautifulSoup
import re

#def scrape_data():
#    url = "https://www.olx.ro/imobiliare/birouri-spatii-comerciale/bucuresti/?search%5Bdistrict_id%5D=5&search%5Bfilter_enum_alege%5D%5B0%5D=inchiriere&currency=EUR"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Verifică dacă cererea a avut succes
    except requests.RequestException as e:
        print(f"Eroare la cererea GET: {e}")
        return

    soup = BeautifulSoup(response.content, "html.parser")

    # Listă pentru link-uri, titluri, prețuri și suprafețe
    links = []
    titles = []
    prices = []
    areas = []

    # Extragere date pentru link-urile de tipul 1 și 2
    for div in soup.find_all("div", class_="css-1ut25fa", type="list"):
        a_tag = div.find("a", href=True)
        
        if a_tag:
            href = a_tag.get("href")
            
            if href.startswith("/d/oferta/"):
                # Tipar 1: Linkul începe cu "/d/oferta/"
                full_link = "https://www.olx.ro" + href
                links.append(full_link)
                
                # Extrage datele (titles, prices, areas) care urmează după link
                title = div.find_next("h6", class_="css-1wxaaza")
                price = div.find_next("p", class_="css-13afqrm")
                area = div.find_next("span", class_="css-643j0o")
                
                titles.append(title.get_text(strip=True) if title else "N/A")
                prices.append(re.findall(r'\d+', price.get_text(strip=True).replace(" ", ""))[0] if price else "N/A")
                areas.append(re.search(r'(\d+)\s*m²', area.get_text(strip=True)).group(1) if area else "N/A")
                
            elif href.startswith("https://www.storia.ro/ro/oferta/"):
                # Tipar 2: Linkul începe cu "https://www.storia.ro/ro/oferta/"
                links.append(href)
                
                # Extrage datele (titles, prices, areas) care urmează după link
                title = div.find_next("h6", class_="css-1wxaaza")
                price = div.find_next("p", class_="css-13afqrm")
                area = div.find_next("span", class_="css-643j0o")
                
                titles.append(title.get_text(strip=True) if title else "N/A")
                prices.append(re.findall(r'\d+', price.get_text(strip=True).replace(" ", ""))[0] if price else "N/A")
                areas.append(re.search(r'(\d+)\s*m²', area.get_text(strip=True)).group(1) if area else "N/A")

    # Verificare lungimi liste
    print(f"Lungimi liste: links={len(links)}, titles={len(titles)}, prices={len(prices)}, areas={len(areas)}")

    # Verifică dacă toate listele au aceeași lungime
    min_length = min(len(links), len(titles), len(prices), len(areas))
    links = links[:min_length]
    titles = titles[:min_length]
    prices = prices[:min_length]
    areas = areas[:min_length]

    # Creează un DataFrame și salvează-l ca output.csv
    df = pd.DataFrame({
        "Link": links,
        "Title": titles,
        "Price (Eur)": prices,
        "Area (Sqm)": areas
    })

    # Verifică DataFrame-ul înainte de a salva
    print(df.head())

    df.to_csv("output.csv", index=False, encoding='utf-8-sig')
    print("Datele au fost salvate cu succes în output.csv")

# Execută funcția de scraping
scrape_data()
