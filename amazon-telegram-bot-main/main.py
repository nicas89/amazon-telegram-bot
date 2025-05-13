import os
import time
import requests
import telegram
from bs4 import BeautifulSoup

TOKEN = os.environ["BOT_TOKEN"]
CHAT_ID = os.environ["CHAT_ID"]
AFFILIATE_ID = os.environ["AMAZON_TAG"]

bot = telegram.Bot(token=TOKEN)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def estrai_offerte():
    url = "https://www.amazon.it/gp/goldbox"
    response = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(response.text, "html.parser")
    prodotti = soup.select(".DealGridItem-module__dealItemDisplayGrid_2c4p7")
    
    risultati = []
    for prodotto in prodotti:
        try:
            titolo = prodotto.select_one("img")["alt"]
            immagine = prodotto.select_one("img")["src"]
            link = "https://www.amazon.it" + prodotto.find("a")["href"].split("?")[0]
            sconto = prodotto.select_one(".BadgeAutomatedLabel-module__badgeLabelText_3y1_g").text
            if "%" in sconto and int(sconto.replace("%", "").replace("−", "")) >= 50:
                link_affiliato = f"{link}?tag={AFFILIATE_ID}"
                risultati.append({
                    "titolo": titolo,
                    "link": link_affiliato,
                    "immagine": immagine,
                    "sconto": sconto
                })
        except:
            continue
    return risultati

def invia_offerte():
    offerte = estrai_offerte()
    for offerta in offerte:
        messaggio = f"**{offerta['titolo']}**\nSconto: {offerta['sconto']}\n[Acquista qui]({offerta['link']})"
        bot.send_photo(chat_id=CHAT_ID, photo=offerta["immagine"], caption=messaggio, parse_mode="Markdown")
        time.sleep(5)

if __name__ == "__main__":
    invia_offerte()
