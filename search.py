def search_by_name(data):
  name = input("Enter name: ").strip().lower()
  for pokemon in data:
    if pokemon['name'].lower() == name:
      return pokemon
  print('Not found')
  return {}