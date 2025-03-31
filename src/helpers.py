import pandas as pd

from src.json_data_helpers import FiveTournamentRollingCoefficient


def fix_commas_in_rank(results: pd.DataFrame) -> pd.DataFrame:
    results['Rank'] = results['Rank'].str.replace(',', '.')
    results['Rank'] = results['Rank'].astype(float)
    return results


def convert_column_to_int(results: pd.DataFrame, column_name: str) -> pd.DataFrame:
    results[column_name] = pd.to_numeric(results[column_name], errors='coerce').astype('Int64')
    return results


def add_goal_difference_column(results: pd.DataFrame) -> pd.DataFrame:
    results['GD'] = results['BZ'] - results['BS']
    return results


def add_points_column(results: pd.DataFrame) -> pd.DataFrame:
    results['Points'] = results['Z'] * 3 + results['R']
    return results


def add_tournament_place(results: pd.DataFrame) -> pd.DataFrame:
    # Define a function to process each tournament group
    def assign_places(group):
        group = group.sort_values(by=['Points', 'GD', 'BZ'], ascending=[False, False, False])
        # Assign ranks
        group['place'] = range(1, len(group) + 1)
        return group

    # Apply the function to each tournament group
    results = results.groupby('tournament', group_keys=False).apply(assign_places)

    # Ensure 'place' is an integer
    results['place'] = results['place'].astype(int)

    return results


def create_tournaments(results: pd.DataFrame, tournaments: pd.DataFrame) -> list:
    context_tournaments = []

    for index, tournament in tournaments.iterrows():
        id_ = tournament['turniej']
        date = tournament['data']
        data = results[results['tournament'] == id_]

        data.insert(0, 'place', data.pop('place'))

        data.pop('tournament')

        single_tournament = {
            'id': id_,
            'name': f"Mój Turniej {id_}",
            'date': date,
            'data': data.to_dict('records'),
        }
        context_tournaments.append(single_tournament)

    context_tournaments.reverse()

    return context_tournaments


def create_all_time(results: pd.DataFrame):
    results_grouped = results.groupby(["player", "place"]).size().reset_index(name="count")
    results_by_player = results_grouped.pivot(index="player", columns="place", values="count")
    results_by_player_sorted = results_by_player.sort_values(by=[1, 2, 3, 4, 5], ascending=[False] * 5).astype('int64',
                                                                                                               errors='ignore')
    results_sanitized = results_by_player_sorted.fillna(0).astype(int)
    return results_sanitized.T.to_dict()


def create_index_context(results: pd.DataFrame, tournaments: pd.DataFrame) -> dict:
    return {
        'tournaments': create_tournaments(results, tournaments),
    }


def sum_matches_played(results: pd.DataFrame):
    # TODO: calculate points_per_match
    sum_df = results.groupby(["player"]).sum().filter(items=["player", "RM", "Z", "R", "P", "BZ", "BS", "GD", "Points"])
    # TODO: coefficient is not normalized here
    return sum_df.T.to_dict()


def create_statistics_context(results: pd.DataFrame) -> dict:
    return {
        'all_time': create_all_time(results),
        'sum_matches': sum_matches_played(results),
        'seeding': FiveTournamentRollingCoefficient(results).get_seeding(tiers=5)
        # TODO: make number of tiers stored in one place
    }


def get_sanitized_results(results: pd.DataFrame) -> pd.DataFrame:
    results = fix_commas_in_rank(results)
    results = convert_column_to_int(results, "BZ")
    results = convert_column_to_int(results, "BS")
    results = add_goal_difference_column(results)
    results = add_points_column(results)
    results = add_tournament_place(results)
    return results
