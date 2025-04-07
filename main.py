import requests


def get_pokemon_list():
  r = requests.get('https://pokemondb.net/pokedex/national')
  if r.status_code == 200:
    print(r.text)


def main():
  get_pokemon_list()




if __name__ == "__main__":
  main()