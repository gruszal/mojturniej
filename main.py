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


if __name__ == '__main__':
    results = pd.read_csv('results/wyniki2.csv')
    tournaments = pd.read_csv('results/turnieje.csv')

    results = get_sanitized_results(results)

    # TODO: this is hardcoded for tournament 15
    excel_file = Path(__file__).parent / "results" / "Match schedule - Mój Turniej 15.xlsx"
    df_matches = read_tournament_from_tournify_export(excel_file)
    table = convert_to_football_table(df_matches, 15)
    table = update_team_and_rank(table, 'Maciek', "Valencia", 4.5)
    table = update_team_and_rank(table, 'Wojtek', "Al-ahli", 3.5)
    table = update_team_and_rank(table, 'Alek', "Dinamo Zagreb", 3.5)
    table = update_team_and_rank(table, 'Domin', "M'gladbach", 4)
    table = update_team_and_rank(table, 'Bartek', "PSG", 5)
    results = pd.concat([results, table])

    new_tournament = pd.DataFrame([{"turniej": 15, "data": "05.08.2025", "host": "Domin", "notes": "Turniej z pełną rundą podstawową i połową rundy rewanżową."}])
    tournaments = pd.concat([tournaments, new_tournament])

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
