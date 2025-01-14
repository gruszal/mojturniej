import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.helpers import create_context, get_sanitized_results, \
    CoefficientPerTournament, \
    GoalsFor, GoalsAgainst, GoalDifference, FiveTournamentRollingCoefficient, PointsPerMatchPerTournament, \
    PointsPerTournament, PlacesPerTournament

if __name__ == '__main__':
    results = pd.read_csv('docs/assets/wyniki2.csv')
    tournaments = pd.read_csv('docs/assets/turnieje.csv')

    results = get_sanitized_results(results)

    PlacesPerTournament(results).save_json()
    PointsPerTournament(results).save_json()
    PointsPerMatchPerTournament(results).save_json()
    CoefficientPerTournament(results).save_json()
    FiveTournamentRollingCoefficient(results).save_json()

    goals_for = GoalsFor(results).save_json()
    goals_against = GoalsAgainst(results).save_json()
    goal_difference = GoalDifference(results).save_json()

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    template = env.get_template("src/template.html")
    context = create_context(results, tournaments)
    with open("index.html", mode="w") as f:
        content = template.render(context)
        f.write(content)
