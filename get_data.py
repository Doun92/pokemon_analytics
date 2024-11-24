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

# Gestion des différents corps
def get_corps(t):
    liste_corps = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Apparence du corps")
        if anchor:
            list_th = tr.find_all("th")
            for th in list_th:
                sibling_td = th.find_next_sibling("td")
                corps = sibling_td.find("img")
                liste_corps.append(corps.attrs['alt'])     
    return liste_corps

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
    liste_catégories = []
    list_tr = t.find_all("tr")
    for tr in list_tr:
        anchor = tr.find("a", title="Catégorie")
        if anchor:
            liste_inside_cat = tr.find_all("a") 
            if len(liste_inside_cat)>1:
                list_th = tr.find_all("th")
                for th in list_th:
                    sibling_td = th.find_next_sibling("td")
                    unwanted_anchor = sibling_td.find('a')
                    unwanted_anchor.extract()
                    liste_catégories.append(sibling_td.text[1:])
            else:
                plusieurs_catégories_tags = tr.find_next_sibling("tr")
                liste_colonnes = plusieurs_catégories_tags.find_all("td")
                for td in liste_colonnes:
                    unwanted_anchor = td.find('a')
                    unwanted_anchor.extract()
                    try:
                        unwanted_small = td.find('small')
                        unwanted_small.extract()
                    except:
                        pass
                    finally:
                        liste_catégories.append(td.text[1:])

    return liste_catégories

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
def get_type(t, pkm):
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
                    if pkm == "Motisma":
                        third_row = second_row.next_sibling
                        s_col_in_row = third_row.find_all("td")
                        for td in s_col_in_row:
                            list_spans = td.find_all("span")
                            for span in list_spans:
                                type_pkm = span.find('a').attrs['title'].split(" ",1)[0]
                                liste_types.append(type_pkm)
                # Les pokemons plus normaux qui n'ont pas des combos de types
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

def handle_exceptional_pokemons(liste, pkm, param_1="", param_2="", param_3=""):
    if pkm in ["Morphéo"]:
        fake_liste_types = [param_1,""]
        liste[1] = fake_liste_types
        liste[5] = param_2
    
    if pkm == "Cheniselle":
        liste[1] = param_1
        liste[5] = param_2

    if pkm in ["Dialga", "Palkia"]:
        liste[3] = param_1
        liste[4] = param_2
        liste[5] = param_3

    # Pokemon changement de poids et taille uniquement
    if pkm == "Giratina":
        liste[3] = param_1
        liste[4] = param_2

    if pkm == "Bargantua":
        liste[2] = param_1

    if pkm == "Ceriflor":
        liste[5] = param_1
    
    if pkm == "Sancoki":
        liste[5] = param_1
        liste[6] = param_2
    
    if pkm == "Motisma":
        liste[1] = param_1

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
    types = get_type(fiche_info, title.text.split(" — ")[0])
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

def split(a, n):
    # a = list
    # n = how much to divide
    k, m = divmod(len(a), n)
    return (a[i*k+min(i, m):(i+1)*k+min(i+1, m)] for i in range(n))

def main_process(test=False, test_list = []):
    liste_pkm_exceptions = [
    "Morphéo","Dialga", "Bargantua",
    "Arceus", "Ceriflor", "Cheniselle",
    "Giratina", "Motisma", "Sancoki"
    ]
    
    if test:
        for pokemon in test_list:
            test = get_pokemon_data(f"https://www.pokepedia.fr/{pokemon}")
            # print(test[5])
            if pokemon in liste_pkm_exceptions:
                # Pokémons avec plusieurs types et couleurs
                if pokemon in ["Morphéo"]:
                    # print(test[1])
                    for sub_type, sub_colour in zip(test[1], test[5][1:]):
                        response = handle_exceptional_pokemons(test, pokemon, sub_type, sub_colour)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)
                
                # Pokemon avec plusieurs double types
                if pokemon == "Motisma":
                    divided_test = list(split(test[1],6))
                    for sub_types in divided_test:
                        response = handle_exceptional_pokemons(test, pokemon, sub_types)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)

                # Pokémons avec plusieurs combos de types et couleurs
                if pokemon == "Cheniselle":
                    divided_test = list(split(test[1],3))
                    for sub_types, sub_colour in zip(divided_test, test[5][1:]):
                        response = handle_exceptional_pokemons(test, pokemon, sub_types, sub_colour)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)


                # Pokemons avec plusieurs poids et formes et couleurs       
                if pokemon in ["Dialga", "Palkia"]:
                    for sub_height, sub_weight, sub_colour in zip(test[3], test[4], test[5]):
                        response = handle_exceptional_pokemons(test, pokemon, sub_height, sub_weight, sub_colour)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)
                
                # Pokemons avec tailles différentes
                if pokemon == "Giratina":
                    for sub_height, sub_weight in zip(test[3], test[4]):
                        response = handle_exceptional_pokemons(test, pokemon, sub_height, sub_weight)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)

                # Pokémon avec plusieurs catégories
                if pokemon == "Bargantua":
                    for sub_cat in test[2]:
                        response = handle_exceptional_pokemons(test, pokemon, sub_cat)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)

                # Pokémons avec plusieurs couleurs
                if pokemon == "Arceus":
                    test[5] = test[5][1]
                    response = flatten_list(test)
                    response.insert(0, 1)
                    write_csv(response)

                # Différentes couleurs
                if pokemon in ["Ceriflor"]:
                    for sub_color in test[5][1:]:
                        response = handle_exceptional_pokemons(test, pokemon, sub_color)
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)  

                if pokemon == "Sancoki":
                    print("ici")
                    for sub_color in test[5][1:]:
                        response = handle_exceptional_pokemons(test, pokemon, sub_color, test[6,1])
                        response = flatten_list(response)
                        response.insert(0, 1)
                        write_csv(response)  

            else:
                test = flatten_list(test)
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

            for pokemon in liste_pokemon:
                pkm_data = get_pokemon_data(f"https://www.pokepedia.fr/{pokemon}")
                if pokemon in liste_pkm_exceptions:
                    if pokemon == "Morphéo":
                        # print(test[1])
                        for sub_type, sub_colour in zip(pkm_data[1], pkm_data[5][1:]):
                            response = handle_exceptional_pokemons(pkm_data, pokemon, sub_type, sub_colour)
                            response = flatten_list(response)
                            response.insert(0, i+1)
                            write_csv(response)
                    if pokemon in ["Dialga", "Palkia"]:
                        for sub_height, sub_weight, sub_colour in zip(pkm_data[3], pkm_data[4], pkm_data[5]):
                            response = handle_exceptional_pokemons(pkm_data, pokemon, sub_height, sub_weight, sub_colour)
                            response = flatten_list(response)
                            response.insert(0, i+1)
                            write_csv(response)
                    if pokemon == "Bargantua":
                        for sub_cat in pkm_data[2]:
                            response = handle_exceptional_pokemons(pkm_data, pokemon, sub_cat)
                            response = flatten_list(response)
                            response.insert(0, i+1)
                            write_csv(response)

                    # Pokémons avec plusieurs couleurs
                    if pokemon == "Arceus":
                        pkm_data[5] = pkm_data[5][1]
                        response = flatten_list(pkm_data)
                        response.insert(0, i+1)
                        write_csv(response)
                    if pokemon == "Ceriflor":
                        for sub_color in pkm_data[5][1:]:
                            response = handle_exceptional_pokemons(pkm_data, pokemon, sub_color)
                            response = flatten_list(response)
                            response.insert(0, 1)
                            write_csv(response)
                    
                    # Pokemons avec tailles différentes
                    if pokemon == "Giratina":
                        for sub_height, sub_weight in zip(test[3], test[4]):
                            response = handle_exceptional_pokemons(test, pokemon, sub_height, sub_weight)
                            response = flatten_list(response)
                            response.insert(0, 1)
                            write_csv(response)
                else:
                    pkm_data = flatten_list(pkm_data)
                    pkm_data.insert(0, i+1)
                    write_csv(pkm_data)
liste_test_pkm = [
    "Abo","Abra","Alakazam","Aéromite","XD001","Morphéo","Dialga", "Bargantua",
    "Arceus", "Ceriflor", "Cheniselle", "Giratina", "Motisma", "Sancoki"
                  ]
autres_pokemons = ["Shaymin","Tritosor","Boréas","Darumacho","Démétéros","Fulguris","Kyurem","Meloetta","Vivaldaim","Banshitrouye","Hoopa","Méga-Absol","Mistigrix","Pitrouille","Primo-Groudon","Prismillon","Zygarde","Feunard_d'Alola","Froussardine","Lougaroc","Météno","Plumeline","Charmilly","Charmilly_Gigamax","Shifours","Ursaking","Zacian","Zamazenta","Arboliva","Famignol","Mordudor","Ogerpon","Superdofin","Tapatoès","Terapagos"]
"""
Tous les pokémon avec Méga ont un problème
Tous les pokémon régionaux
Tous les pokémon gigamax
Il manque les noms japonais et allemand des pokémon de neuvième génération
"""


"""
Ce qu'il nous faut faire est la chose suivante:
1)  Modifier la fonction exception pour pas qu'elle apparaisse dans la boucle for
    En gros, on charge tous les paramètres et selon le paramètre cahrgé, on change qqch dans la liste
2)  On gère les Méga, les Giga et les Régionaux, c'est en rapport avec le nom, ça devrait pas être compliqué
3) On gère les exceptions des exceptions
4) La nouvelle génération est toujours un problème, on complète la abse de données au cas où
"""
main_process(test=True, test_list=liste_test_pkm, )
# main_process()