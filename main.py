from scrape import scrape
import os
import json
from search import search_by_name

def scrape_pokedex(output_file='pokedex.json'):
  print("Scraping fresh data...please be patient.")
  scrape(output_file)
  return

def load_data(output_file='pokedex.json', force_scrape=False):
  if force_scrape or not os.path.exists(output_file):
    scrape_pokedex()
    
  with open(output_file) as f:
    return json.load(f)

def get_choice():
  while True:
    choice = input("Enter your choice [1-4]: ").strip()
    if choice in {'1','2','3','4'}:
      return choice
    print("Invalid choice, try again.")

def print_entry(pokemon):
  forms = list(pokemon.get('pokedex_entries', {}).keys())

  if not forms:
    print("No Pokédex entries found.")
    return

    # If only one form (e.g. 'default'), just show it
  if len(forms) == 1:
    selected_form = forms[0]
  else:
    print(f"\nAvailable forms for {pokemon['name']}:")
    for i, form in enumerate(forms, 1):
      print(f"{i}. {form}")
    while True:
      choice = input(f"Choose a form [1-{len(forms)}]: ").strip()
      if choice.isdigit() and 1 <= int(choice) <= len(forms):
        selected_form = forms[int(choice) - 1]
        break
      print("Invalid choice. Try again.")

    print(f"\n{pokemon['name']} ({selected_form})")
    print("Types:", ", ".join(pokemon.get('types', [])))

    entries = pokemon['pokedex_entries'][selected_form]
    for game, entry in entries.items():
      print(f"\n{game}: {entry}")

def main():
  print("Welcome to the Python Pokedex!")
  print("It is recommended to only get fresh data on the first run or when a new game has come out.")
  scrape_data = input("Do you need to run a scrape? (This will take ~15-20 mins.)[Y/N]: ").strip().lower() == 'y'

  data = load_data(force_scrape=scrape_data)

  while True:
    print('\nSearch by:')
    print("1. Name")
    print("2. Number")
    print('3. Game')
    print('4. Exit')

    choice = get_choice()

    match choice:
      case '1':
        pokemon = search_by_name(data)
        if pokemon:
          print_entry(pokemon)
        else:
          print('Not Found')
      case '2':
        pass
      case '3':
        pass
      case '4':
        print('Goodbye!')
        break
      case _:
        print("Invalid please try again.")
    

if __name__ == '__main__':
  main()