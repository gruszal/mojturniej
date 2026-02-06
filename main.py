from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from import_from_tournify.import_from_tournify import TournifyImporter, KeysEN, KeysPL
from src.helpers import create_index_context, get_sanitized_results, create_statistics_context
from src.json_data_helpers import generate_jsons

if __name__ == '__main__':
    results_dir = Path(__file__).parent / "results"

    results = pd.read_csv(results_dir / 'wyniki2.csv')
    tournaments = pd.read_csv(results_dir / 'turnieje.csv')

    results = get_sanitized_results(results)

    # TODO: write to csv insead of read on the fly
    file = results_dir / "Match schedule - Mój Turniej 15.xlsx"
    ti = TournifyImporter(KeysEN(), file, tournament_name="15")
    results, tournaments = ti.add_tournament_from_tournify(
        results,
        tournaments,
        teams=[
            ('Maciek', "Villareal", 4.5),
            ('Wojtek', "Al-ahli", 3.5),
            ('Alek', "Dinamo Zagreb", 3.5),
            ('Domin', "M'gladbach", 4),
            ('Bartek', "PSG", 5),
        ]
    )

    file = results_dir / "Match schedule - Mój Turniej 16.xlsx"
    ti = TournifyImporter(KeysEN(), file, tournament_name="16")
    results, tournaments = ti.add_tournament_from_tournify(
        results,
        tournaments,
        teams=[
            ('Maciek', "Chorwacja", 4.5),
            ('Wojtek', "Węgry", 3.5),
            ('Alek', "Irlandia", 3.5),
            ('Domin', "Ghana", 4),
            ('Bartek', "Argentyna", 5),
        ]
    )

    file = results_dir / "Harmonogram meczowy - Mój Turniej 17.xlsx"
    ti = TournifyImporter(KeysPL(), file, tournament_name="17")
    results, tournaments = ti.add_tournament_from_tournify(
        results,
        tournaments,
        teams=[
            ('Maciek', "Chelsea", 4.5),
            ('Wojtek', "Ajax", 4),
            ('Alek', "Torino", 4),
            ('Domin', "Borussia Dortmund", 4.5),
            ('Bartek', "Barcelona", 5),
        ]
    )

    results.reset_index(drop=True, inplace=True)
    generate_jsons(results)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )

    tournaments["turniej"] = tournaments["turniej"].astype(str)

    template = env.get_template("src/templates/index.html")
    context = create_index_context(results, tournaments)

    with open("index.html", mode="w") as f:
        content = template.render(context)
        f.write(content)

    template = env.get_template("src/templates/statistics.html")
    context = create_statistics_context(results)

    with open("statistics.html", mode="w") as f:
        content = template.render(context)
        f.write(content)
