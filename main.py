from pathlib import Path

import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from import_from_tournify.import_from_tournify import read_tournament_from_tournify_export, convert_to_football_table
from src.helpers import create_index_context, get_sanitized_results, create_statistics_context
from src.json_data_helpers import generate_jsons


def update_team_and_rank(table, player: str, team: str, rank: float):
    table.loc[table['player'] == player, 'team'] = team
    table.loc[table['player'] == player, 'Rank'] = rank
    return table


def add_tournament_from_tournify(results: pd.DataFrame, tournaments: pd.DataFrame, excel_file, tournament_number, teams,
                                 date=None, host=None, notes=None):
    df_matches = read_tournament_from_tournify_export(Path(__file__).parent / "results" / excel_file)
    table = convert_to_football_table(df_matches, tournament_number)
    for player in teams:
        # TODO: check if "player[0]" is in players in the tournamens
        table = update_team_and_rank(table, player[0], player[1], player[2])

    results = pd.concat([results, table])

    if date and host and notes:
        new_tournament = pd.DataFrame([{"turniej": tournament_number, "data": date, "host": host, "notes": notes}])
        tournaments = pd.concat([tournaments, new_tournament])

    return results, tournaments


if __name__ == '__main__':
    results = pd.read_csv('results/wyniki2.csv')
    tournaments = pd.read_csv('results/turnieje.csv')

    results = get_sanitized_results(results)

    # TODO: write to csv insead of read on the fly
    results, tournaments = add_tournament_from_tournify(
        results,
        tournaments,
        excel_file="Match schedule - Mój Turniej 15.xlsx",
        tournament_number=15,
        teams=[
            ('Maciek', "Villareal", 4.5),
            ('Wojtek', "Al-ahli", 3.5),
            ('Alek', "Dinamo Zagreb", 3.5),
            ('Domin', "M'gladbach", 4),
            ('Bartek', "PSG", 5),
        ]
    )

    results, tournaments = add_tournament_from_tournify(
        results,
        tournaments,
        excel_file="Match schedule - Mój Turniej 16.xlsx",
        tournament_number=16,
        teams=[
            ('Maciek', "Chorwacja", 4.5),
            ('Wojtek', "Węgry", 3.5),
            ('Alek', "Irlandia", 3.5),
            ('Domin', "Ghana", 4),
            ('Bartek', "Argentyna", 5),
        ],
    )

    results.reset_index(drop=True, inplace=True)
    generate_jsons(results)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )

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
