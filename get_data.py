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

def get_categorie(t):
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Catégorie")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                # print(sibling_td)
                unwanted_anchor = sibling_td.find('a')
                unwanted_anchor.extract()
                return sibling_td.text[1:]

def get_taille(t):
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Taille")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                return sibling_td.text.split(" ",1)[0]

def get_poids(t):
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Poids")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                return sibling_td.text.split(" ",1)[0]

def get_type(t):
    liste_types = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Type")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                # print(sibling_td)
                list_spans = sibling_td.find_all("span")
                for span in list_spans:
                    # print(span)
                    type_pkm = span.find('a').attrs['title'].split(" ",1)[0]
                    liste_types.append(type_pkm)
    if len(liste_types)<2:
        liste_types.append("")
    return liste_types

# Get the precise date from each pokemon
def get_pokemon_data(page):
    liste_data = []
    # print(page)
    html_code = requests.get(page).content
    # print(html_code)
    soup = BeautifulSoup(html_code, 'html.parser')
    # print(soup)
    title = soup.find('title')
    print(title.text)
    fiche_info = soup.find('table', class_='ficheinfo')
    numéro_national = fiche_info.find('span', title="Numérotation nationale")
    # print(numéro_national.text[2:])
    liste_data.append(numéro_national.text[2:])

    # Get the types of Pokemons
    types = get_type(fiche_info)
    liste_data.append(types)

    catégorie = get_categorie(fiche_info)
    liste_data.append(catégorie)

    taille = get_taille(fiche_info)
    liste_data.append(taille)

    poids = get_poids(fiche_info)
    liste_data.append(poids)

    print(liste_data)

#Get all pokedex
différentes_generations = get_anchor_text(pokemons_par_generation)
# print(différentes_generations)

# Get all the pokemons from the pokedex page
# for génération in différentes_generations:
#     génération = génération.replace(" ", "_")
#     # print(génération)
#     liste_pokemon = get_anchor_text(f"https://www.pokepedia.fr/Cat%C3%A9gorie:{génération}")
#     liste_pokemon = [ x for x in liste_pokemon if "Pokémon" not in x and "Ultra-Chimère" not in x and "Espèce convergente" not in x] #Remove from the list any entry with the characters inside.
#     # print(liste_pokemon)
    
#     for pokemon in liste_pokemon:
#         get_pokemon_data(f"https://www.pokepedia.fr/{pokemon}")

get_pokemon_data(f"https://www.pokepedia.fr/Abo")
get_pokemon_data(f"https://www.pokepedia.fr/Rapasdepic")