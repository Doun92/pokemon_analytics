import requests
from bs4 import BeautifulSoup
import csv

# On prend le texte dans la balise HTML a
# On retourne un liste de toutes les balises a dans la div de classe "mw-category-group"
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

# Gestion des stats
def get_statistiques(t):
    empty_dict = {}
    list_headings = t.find_all("h2")
    for heading in list_headings:
        if "Statistiques" in heading.text:
            list_next_divs = heading.find_next_siblings("div")
            for next_divs in list_next_divs:
                if next_divs.find("table"):
                    stat_anchors = next_divs.find_all("a", title="Statistique")
                    for i, anchor in enumerate(stat_anchors):
                        if i<7:
                            stat_name = anchor.text
                            if stat_name != "Statistique":
                                prt = anchor.parent
                                empty_dict[stat_name] = int(prt.find_next_sibling("td").text)
    return empty_dict

def get_corps(t):
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Apparence du corps")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                corps = sibling_td.find("img")
                return corps.attrs['alt']

# Function to flatten nested lists and dictionaries
def flatten_list(data):
    flattened = []
    for item in data:
        if isinstance(item, list):  # If item is a list, recursively flatten it
            flattened.extend(flatten_list(item))
        elif isinstance(item, dict):  # If item is a dict, flatten its key-value pairs
            flattened.extend((value) for key, value in item.items())
        else:  # Otherwise, add the item directly
            flattened.append(item)
    return flattened

def get_couleur(t):
    liste_couleurs = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Couleur")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                liste_images = sibling_td.find_all("img")
                for image in liste_images:
                    liste_couleurs.append(image.attrs['alt'])
    return liste_couleurs

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

# Gestion des tailles
def get_taille(t):
    liste_tailles = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Taille")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                # Cette condition permet de gérer les pokémons à plusieur tailles
                if th.has_attr('colspan'):
                    parent = th.parent
                    first_row = parent.next_sibling
                    f_col_in_row = first_row.find_all("td")
                    for td in f_col_in_row:
                        taille = td.text.split(" ",1)[0]
                        liste_tailles.append(taille)
                else:
                    sibling_td = th.find_next_sibling("td")
                    taille = sibling_td.text.split(" ",1)[0]
                    liste_tailles.append(taille)
    return liste_tailles

# Gestion des poids
def get_poids(t):
    liste_poids = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Poids")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                # Cette condition permet de gérer les pokémons à plusieur poids
                if th.has_attr('colspan'):
                    parent = th.parent
                    first_row = parent.next_sibling
                    f_col_in_row = first_row.find_all("td")
                    for td in f_col_in_row:
                        poids = td.text.split(" ",1)[0]
                        liste_poids.append(poids)
                else:
                    sibling_td = th.find_next_sibling("td")
                    poids = sibling_td.text.split(" ",1)[0]
                    liste_poids.append(poids)
    return liste_poids

# Gestion des types
def get_type(t):
    liste_types = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Type")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                # This condition is meant to deal with pokemons with more than 2 types
                if th.has_attr('colspan'):
                    parent = th.parent
                    first_row = parent.next_sibling
                    f_col_in_row = first_row.find_all("td")
                    for td in f_col_in_row:
                        list_spans = td.find_all("span")
                        for span in list_spans:
                            type_pkm = span.find('a').attrs['title'].split(" ",1)[0]
                            liste_types.append(type_pkm)
                    second_row = parent.next_sibling.next_sibling
                    s_col_in_row = second_row.find_all("td")
                    for td in s_col_in_row:
                        list_spans = td.find_all("span")
                        for span in list_spans:
                            type_pkm = span.find('a').attrs['title'].split(" ",1)[0]
                            liste_types.append(type_pkm)
                else:
                    sibling_td = th.find_next_sibling("td")
                    list_spans = sibling_td.find_all("span")
                    for span in list_spans:
                        type_pkm = span.find('a').attrs['title'].split(" ",1)[0]
                        liste_types.append(type_pkm)
    if len(liste_types)<2:
        liste_types.append("")
    return liste_types

# Gestion des noms
def get_étymologies(t):
    # On est obligés car un pokémon en particulier n'a pas de section étyomologie
    try:
        liste_étymologies = []
        étymologie_titre = t.find(id="Étymologies").parent
        étymologie_liste = étymologie_titre.find_next_sibling("ul")
        # print(étymologie_liste)
        for li in étymologie_liste:
            # print(li.text)
            # print(len(li))
            language = li.text.split(":",1)[0]
            if len(li)>1:
                if "Français" in language:
                    # print(f"Français: {li.text}")
                    nom = li.find("i")
                    liste_étymologies.append(nom.text)
                if "Allemand" in language or "allemand" in language:
                    # print(f"Allemand: {li.text}")
                    nom = li.find("i")
                    liste_étymologies.append(nom.text)
                if "Anglais" in language or "anglais" in language:
                    # print(f"Anglais: {li.text}")
                    nom = li.find("i")
                    liste_étymologies.append(nom.text)
                if "Japonais" in language or "japonais" in language:
                    # print(f"Japonais: {li.text}")
                    nom = li.find("i")
                    liste_étymologies.append(nom.text)
    except:
        title = t.find('title')
        if "XD001" in title.text:
            liste_étymologies = ["XD001","XD001","Shadow Lugia","Dark Lugia"]
    finally:
        return liste_étymologies

def handle_exceptional_pokemons(liste, pkm, type_from_above, couleurs):
    # if pkm == "Morphéo":
    #     fake_liste = [type_from_above,""]
    #     liste[1] = fake_liste
    #     return liste
    
    if pkm == "Morphéo":
        fake_liste_types = [type_from_above,""]
        fake_liste_colours = [couleurs, ""]
        liste[1] = fake_liste_types
        liste[5] = fake_liste_colours
        return liste

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

    couleur = get_couleur(fiche_info)
    liste_data.append(couleur)

    corps = get_corps(fiche_info)
    liste_data.append(corps)

    étymologies = get_étymologies(soup)
    liste_data.append(étymologies)

    statistiques = get_statistiques(soup)
    liste_data.append(statistiques)

    return liste_data

def write_csv(data):
    file = "mon_pokedex.csv"
    with open(file, "+a", encoding="utf8", newline='') as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        writer.writerow(data)

def main_process(test=False, test_list = []):
    if test:
        for pokemon in test_list:
            test = get_pokemon_data(f"https://www.pokepedia.fr/{pokemon}")
            if pokemon == "Morphéo":
                # print(test[1])
                for sub_type, sub_colour in zip(test[1], test[5][1:]):
                    response = handle_exceptional_pokemons(test, pokemon, sub_type, sub_colour)
                    response = flatten_list(response)
                    response.insert(0, 1)
                    response.insert(0, 1)
                    write_csv(response)
            else:
                test = flatten_list(test)
                test.insert(0, 1)
                test.insert(0, 1)
                write_csv(test)
    else:
        #Page avec toutes les générations
        pokemons_par_generation = "https://www.pokepedia.fr/Cat%C3%A9gorie:Pok%C3%A9mon_par_g%C3%A9n%C3%A9ration"

        # Liste des différentes générations pokemon
        différentes_generations = get_anchor_text(pokemons_par_generation)

        # On va circuler à travers ces listes pour pouvoir prendre les données de cahque pokemon dans cahque liste
        for i, génération in enumerate(différentes_generations):
            génération = génération.replace(" ", "_")
            
            #Remove from the list any entry with the characters inside.
            liste_pokemon = get_anchor_text(f"https://www.pokepedia.fr/Cat%C3%A9gorie:{génération}")
            liste_pokemon = [ x for x in liste_pokemon if "Pokémon" not in x and "Ultra-Chimère" not in x and "Espèce convergente" not in x]

            for id, pokemon in enumerate(liste_pokemon):
                pkm_data = get_pokemon_data(f"https://www.pokepedia.fr/{pokemon}")
                if pokemon == "Morphéo":
                    # print(pkm_data[1])
                    for sub_type in pkm_data[1]:
                        response = handle_exceptional_pokemons(pkm_data,pokemon,sub_type)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        response.insert(0, 1)
                        write_csv(response)
                else:
                    flat_pkm = flatten_list(pkm_data)
                    flat_pkm.insert(0, i+1)
                    flat_pkm.insert(0, id+1)
                    write_csv(flat_pkm)

"""
Dialga et Palkia vont faire souci.
Ils ont tous deux une forme originelle à gérer.
Comme pour Morphéo, il faudra créer une ligne par forme.
Il ne manque plus qu'à créer deux lignes par taille et poids et c'est bon
"""
main_process(test=True, test_list=["Abo","Abra","Alakazam","Aéromite","XD001","Morphéo","Dialga"])
# main_process(test=True, test_list=["Morphéo"])
# main_process()