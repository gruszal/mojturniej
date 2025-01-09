import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.helpers import create_context, get_sanitized_results, get_places, get_points_per_tournament, \
    get_points_per_match_per_tournament

if __name__ == '__main__':
    results = pd.read_csv('docs/assets/wyniki2.csv')
    tournaments = pd.read_csv('docs/assets/turnieje.csv')

    results = get_sanitized_results(results)

    places_df = get_places(results)
    places_df.to_json('docs/assets/place_per_tournament.json')

    points_per_tournament_df = get_points_per_tournament(results)
    points_per_tournament_df.to_json('docs/assets/points_per_tournament.json')

    points_per_match_per_tournament_df = get_points_per_match_per_tournament(results)
    points_per_match_per_tournament_df.to_json('docs/assets/points_per_match_per_tournament.json')

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    template = env.get_template("src/template.html")
    context = create_context(results, tournaments)
    with open("index.html", mode="w") as f:
        content = template.render(context)
        f.write(content)
