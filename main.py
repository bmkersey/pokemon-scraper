import requests
from bs4 import BeautifulSoup
import time
import json

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
  entries_by_form = {}

  dex_header = soup.find('h2', string='Pokédex entries')
  if not dex_header:
    return entries_by_form
  

  current = dex_header.find_next_sibling()
  if current and current.name == 'div' and current.find('table'):
    #only base forms
    table = current.find('table')
    entries = {}
    for row in table.select('tr'):
      th = row.find('th')
      td = row.find('td')
      if not th or not td:
        continue
      games = [span.text.strip() for span in th.select('span.igame')]
      grouped_games = "/".join(games)
      entries[grouped_games] = td.text.strip()
    print(entries)
    entries_by_form["default"] = entries

  while current:
    if current.name == 'h3':
      form = current.text.strip()
      table_div = current.find_next_sibling('div')
      table = table_div.find('table') if table_div else None
      if not table:
        current = table_div.find_next_sibling() if table_div else current.find_next_sibling()
        continue
      
      form_entries = {}
      for row in table.select('tr'):
        th = row.find('th')
        td = row.find('td')
        if not th or not td:
          continue
        games = [span.text.strip() for span in th.select('span.igame')]
        grouped_names = "/".join(games)
        entry = td.text.strip()
        form_entries[grouped_names] = entry
      entries_by_form[form] = form_entries
      print(form_entries)
    
    if current.name == 'h2':
      break
    
    current = current.find_next_sibling()

  return entries_by_form

def main():
  pokemon = get_pokemon_list()
  for mon in pokemon:
    print(f"Scraping data for {mon['name']}...")
    entries = get_pokedex_text(mon['details_url'])
    mon['pokedex_entries'] = entries
    time.sleep(1)
  
  with open('pokedex.json', 'w') as f:
    json.dump(pokemon, f, indent=2)




if __name__ == "__main__":
  main()