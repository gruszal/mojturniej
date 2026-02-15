from pathlib import Path

import pandas as pd

from import_from_tournify.import_from_tournify import TournifyImporter, KeysEN


def update_wyniki(filename, teams, tournament_name: str, keys=KeysEN()):
    results_dir = Path(__file__).parent

    file = results_dir / filename

    ti = TournifyImporter(keys, file, tournament_name)

    results = pd.read_csv(results_dir / 'wyniki.csv')
    tournaments = pd.read_csv(results_dir / 'turnieje.csv')

    if bool(results["tournament"].astype(str).eq(tournament_name).any()):
        raise ValueError(f"Tournament {tournament_name} already exists")

    results, tournaments = ti.add_tournament_from_tournify(
        results,
        tournaments,
        teams=teams
    )

    results = results.drop(columns=['GD','Points','place'])

    results["BS"] = results["BS"].replace("", pd.NA).astype("Int64")
    results["BZ"] = results["BZ"].replace("", pd.NA).astype("Int64")

    results.to_csv(results_dir / 'wyniki.csv', index=False)
