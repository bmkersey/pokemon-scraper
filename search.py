def search_by_name(data):
  name = input("Enter name (partial or full): ").strip().lower()
  matches = [p for p in data if name in p['name'].lower()]

  if not matches:
    print("No matches found.")
    return None

  if len(matches) == 1:
    return matches[0]

  print("\nMultiple matches found:")
  for i, p in enumerate(matches, 1):
    print(f"{i}. {p['name']}")

  while True:
    choice = input(f"Select a number [1-{len(matches)}]: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(matches):
      return matches[int(choice) - 1]
    print("Invalid choice. Try again.")


def search_by_number(data):
  number_input = input("Enter Pokédex number (e.g., 4 or 004 or #0004): ").strip().lstrip('#')
  number_formatted = f"#{int(number_input):04d}"  # Converts to "#0004" format

  for p in data:
    if p['number'] == number_formatted:
      return p

  print("No Pokémon found with that number.")
  return None

def search_by_game(data):
  game = input("Enter game name (e.g., 'Red/Blue', 'Sword', etc.): ").strip().lower()
  matches = []

  for p in data:
    for form, entries in p.get('pokedex_entries', {}).items():
      for g in entries:
        if g.lower() == game:
          matches.append((p, form))
          break  # Don't duplicate this Pokémon for multiple matching forms

  if not matches:
    print("No Pokémon found with entries for that game.")
    return None

  print(f"\nFound {len(matches)} Pokémon with entries in {game}:")
  for i, (p, form) in enumerate(matches, 1):
    print(f"{i}. {p['name']} ({form})")

  while True:
    choice = input(f"Choose a number [1-{len(matches)}]: ").strip()
    if choice.isdigit() and 1 <= int(choice) <= len(matches):
      pokemon, selected_form = matches[int(choice) - 1]
      return pokemon, selected_form, game
    print("Invalid choice. Try again.")
