import requests
from bs4 import BeautifulSoup

# generation_01_url = "https://www.pokepedia.fr/Cat%C3%A9gorie:Pok%C3%A9mon_de_la_premi%C3%A8re_g%C3%A9n%C3%A9ration"
pokemons_par_generation = "https://www.pokepedia.fr/Cat%C3%A9gorie:Pok%C3%A9mon_par_g%C3%A9n%C3%A9ration"

def get_anchor_text(page):
    list_to_return = []
    html_code = requests.get(page).content 
    soup = BeautifulSoup(html_code, 'html.parser')
    parent = soup.find_all("div", {"class": "mw-category-group"})
    for child in parent:
        list_by_letter = child.find_all("a")
        for anchor in list_by_letter:
            list_to_return.append(anchor.text)
    return list_to_return

#Get all pokedex
différentes_generations = get_anchor_text(pokemons_par_generation)
print(différentes_generations)


# Get all the pokemons from the pokedex page