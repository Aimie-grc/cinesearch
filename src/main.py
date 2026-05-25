from elasticsearch import Elasticsearch
from colorama import init, Fore, Style
init()

from config import create_mapping
from indexer import index_movies, verif_es
from search import search_by_title, search_advanced, search_plot,search_fuzzy, suggest_titles
from analytics import global_stats, top_genres, best_rated_directors

INFO = Fore.CYAN
SUCCESS = Fore.GREEN
ERROR = Fore.RED
RESET = Style.RESET_ALL

def format_result(results_json, taille_colonne=50):
    if not results_json:
        print("Aucun résultat.")
        return

    keys = list(results_json[0].keys())

    col_width = {}

    # calcul largeur par colonne
    for k in keys:
        max_len = max(len(str(item.get(k, ""))) for item in results_json)
        col_width[k] = max(len(k), min(max_len, taille_colonne))

    # largeur totale dynamique
    total_width = sum(col_width[k] for k in keys) + (3 * len(keys)) + 3

    print("─" * total_width)

    # header
    header = " # │ " + " │ ".join(f"{k.capitalize():<{col_width[k]}}" for k in keys)
    print(header)

    print("─" * total_width)

    # lignes
    for i, item in enumerate(results_json, start=1):
        row_values = []

        for k in keys:
            value = item.get(k, "N/A")

            # float
            if isinstance(value, float):
                value = f"{value:.2f}"

            # liste
            elif isinstance(value, list):
                value = ", ".join(map(str, value))

            value = str(value)

            # troncature
            if len(value) > taille_colonne:
                value = value[:taille_colonne - 3] + "..."

            row_values.append(f"{value:<{col_width[k]}}")

        print(f"{i:<2} │ " + " │ ".join(row_values))

    print("─" * total_width)
    print(f"{len(results_json)} résultat(s) trouvé(s)")

def main():

    print(INFO + "\nBienvenue dans CineSearch !"+ RESET)
    print("Connexion à Elasticsearch...\n")

    try:
        es = Elasticsearch("http://localhost:9200")
        es.info()
        print(SUCCESS + "Elasticsearch connecté.\n"+ RESET)
        
        if not es.indices.exists(index="movies"):
            print(INFO + "Index 'movies' introuvable, création..." + RESET)
            create_mapping(es)
            index_movies(es, "data/movies_cleaned_v2.json")
    
    except Exception as e:
        print(ERROR + f"Impossible de se connecter à Elasticsearch : {e}"+ RESET)
        return

    menu = """
    ╔══════════════════════════════════════════╗
    ║ CinéSearch — Menu Principal              ║
    ╠══════════════════════════════════════════╣
    ║ 1. Recherche par titre                   ║
    ║ 2. Recherche avancée (multi-critères)    ║
    ║ 3. Recherche dans le synopsis            ║
    ║ 4. Recherche floue (tolérance erreurs)   ║
    ║ 5. Auto-complétion de titre              ║
    ║ 6. Statistiques globales                 ║
    ║ 7. Top réalisateurs / acteurs / genres   ║
    ║ 8. Quitter                               ║
    ╚══════════════════════════════════════════╝"""

    while True:
        print(menu)

        choice = input("Votre choix : ").strip()

        try:

            match choice:

                case "1":
                    print("\n--- Recherche par titre ---")
                    titre = input("Titre : ")

                    print(f'\nRésultats pour: "{titre}"')
                    results = search_by_title(es, titre)
                    format_result(results)

                case "2":
                    print("\n--- Recherche avancée ---")

                    title = input("Titre (laisser vide si aucun) : ") or None
                    actor = input("Acteur (laisser vide si aucun) : ") or None
                    director = input("Réalisateur (laisser vide si aucun) : ") or None
                    genre = input("Genre (laisser vide si aucun) : ") or None

                    min_rating = input("Note minimale (laisser vide si aucune) : ")
                    min_rating = float(min_rating) if min_rating else None

                    max_rating = input("Note maximale (laisser vide si aucune) : ")
                    max_rating = float(max_rating) if max_rating else None

                    year_from = input("Année minimum (laisser vide si aucune) : ")
                    year_from = int(year_from) if year_from else None

                    year_to = input("Année maximum (laisser vide si aucune) : ")
                    year_to = int(year_to) if year_to else None

                    print(f'\nRésultats pour recherche avancée: "{title or actor or director or genre or "filtre"}"')

                    results = search_advanced(
                        es,
                        title=title,
                        actor=actor,
                        director=director,
                        genre=genre,
                        min_rating=min_rating,
                        max_rating=max_rating,
                        year_from=year_from,
                        year_to=year_to
                    )

                    format_result(results)

                case "3":
                    print("\n--- Recherche dans le synopsis ---")
                    keywords = input("Mots-clés : ")

                    print(f'\nRésultats pour: "{keywords}"')
                    results = search_plot(es, keywords)
                    format_result(results)

                case "4":
                    print("\n--- Recherche floue ---")
                    term = input("Terme recherché : ")

                    print(f'\nRésultats pour: "{term}"')
                    results = search_fuzzy(es, term)
                    format_result(results)

                case "5":
                    print("\n--- Auto-complétion ---")
                    prefix = input("Début du titre : ")

                    print(f'\nSuggestions pour: "{prefix}"')
                    results = suggest_titles(es, prefix)
                    format_result(results)

                case "6":
                    print("\n--- Statistiques globales ---")
                    global_stats(es)

                case "7":
                    print("\n--- Top genres ---")
                    top_genres(es)

                case "8":
                    print(INFO + "\nMerci d'avoir utilisé CineSearch. À bientôt !" + RESET)
                    break

                case _:
                    print(ERROR + "\nChoix invalide. Veuillez entrer un nombre entre 1 et 8." + RESET)

        except ValueError:
            print(ERROR + "\nVeuillez saisir une valeur numérique valide." + RESET)

        except Exception as e:
            print(ERROR + f"\nUne erreur est survenue : {e}" + RESET)

        input("\nAppuyez sur Entrée pour revenir au menu...")

if __name__ == "__main__":
    main()