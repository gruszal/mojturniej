import pandas as pd


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
    for tournament_id in results['tournament'].unique()[::-1]:
        results_for_tournament_id = results[results['tournament'] == tournament_id].sort_values(by='Points',
                                                                                                ascending=False)
        results_for_tournament_id['place'] = range(1, len(results_for_tournament_id) + 1)

        results = pd.concat([results_for_tournament_id, results[results['tournament'] != tournament_id]])

    results['place'] = results['place'].astype(int)
    return results


def create_context(results: pd.DataFrame, tournaments: pd.DataFrame) -> dict:
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

    return {'tournaments': reversed(context_tournaments)}


def get_sanitized_results(results: pd.DataFrame) -> pd.DataFrame:
    results = fix_commas_in_rank(results)
    results = convert_column_to_int(results, "BZ")
    results = convert_column_to_int(results, "BS")
    results = add_goal_difference_column(results)
    results = add_points_column(results)
    results = add_tournament_place(results)
    return results


def get_places(results):
    df = results.pivot(index='player', columns='tournament', values='place')
    return df


def get_points_per_tournament(results: pd.DataFrame) -> pd.DataFrame:
    df = pd.pivot_table(results, index='player', columns='tournament', values='Points')
    return df


def get_points_per_match_per_tournament(results: pd.DataFrame) -> pd.DataFrame:
    results['points_per_match'] = results['Points'] / results['RM']
    df = pd.pivot_table(results, index='player', columns='tournament', values='points_per_match')
    return df
