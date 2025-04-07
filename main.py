import requests
from bs4 import BeautifulSoup
import time

BASE_URL = "https://pokemondb.net"
POKEDEX_URL = f"{BASE_URL}/pokedex/national"

def get_pokemon_list():
  r = requests.get(POKEDEX_URL)
  if r.status_code == 200:
    soup = BeautifulSoup(r.text, 'html.parser')
    pokemon = soup.select(".infocard")
    pokemon_list = []
    for mon in pokemon:
      name = mon.select_one('.ent-name').text
      number = mon.select_one('.infocard-lg-data small').text
      types = [t.text for t in mon.select('.itype')]
      detail_path = mon.select_one('a.ent-name')['href']
      details_url = BASE_URL + detail_path
      
      pokemon_list.append({
        'number': number,
        'name': name,
        'types': types,
        'details_url': details_url
      })
    return pokemon_list
  
def get_pokedex_text(url):
  r = requests.get(url)
  soup = BeautifulSoup(r.text, 'html.parser')
  entries = {}

  pokedex_rows = soup.select('table.vitals-table')[4].select('tr')
  for row in pokedex_rows:
    th = row.find('th')
    td = row.find('td')
    games = [span.text.strip() for span in th.find_all('span', class_='igame')]
    grouped_games = "/".join(games)
    entry = td.text.strip()
    entries[grouped_games] = entry
  return entries

def main():
  pokemon = get_pokemon_list()
  for mon in pokemon:
    print(f"Scraping data for {mon['name']}...")
    entries = get_pokedex_text(mon['details_url'])
    print(entries)
    time.sleep(1)




if __name__ == "__main__":
  main()