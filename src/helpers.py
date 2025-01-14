import abc
from abc import ABCMeta

import pandas as pd


class JsonData(metaclass=ABCMeta):
    assets_dir = 'docs/assets/'

    def __init__(self, results):
        self.results = results

    @property
    @abc.abstractmethod
    def name(self):
        pass

    @abc.abstractmethod
    def generate_data(self) -> pd.DataFrame:
        pass

    def save_json(self):
        data = self.generate_data()
        data.to_json(self.assets_dir + self.name + '.json')


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


def get_coefficient_per_tournament(results: pd.DataFrame) -> pd.DataFrame:
    results['points_per_match'] = results['Points'] / results['RM']
    results['coef'] = results['points_per_match'] / results['Rank']

    df = pd.pivot_table(results, index='player', columns='tournament', values='coef')

    df_normalized = df.div(df.max())

    return df_normalized


class PlacesPerTournament(JsonData):
    name = 'places_per_tournament'

    def generate_data(self) -> pd.DataFrame:
        df = self.results.pivot(index='player', columns='tournament', values='place')
        return df


class PointsPerTournament(JsonData):
    name = 'points_per_tournament'

    def generate_data(self) -> pd.DataFrame:
        df = pd.pivot_table(self.results, index='player', columns='tournament', values='Points')
        return df


class PointsPerMatchPerTournament(JsonData):
    name = 'points_per_match_per_tournament'

    def generate_data(self) -> pd.DataFrame:
        self.results['points_per_match'] = self.results['Points'] / self.results['RM']
        df = pd.pivot_table(self.results, index='player', columns='tournament', values='points_per_match')
        return df


class CoefficientPerTournament(JsonData):
    name = 'coefficient_per_tournament'

    def generate_data(self):
        return get_coefficient_per_tournament(self.results)


class FiveTournamentRollingCoefficient(JsonData):
    name = 'five_tournament_rolling_coefficient'

    def generate_data(self):
        df_normalized = get_coefficient_per_tournament(self.results)
        rolling_df = df_normalized.T.rolling(window=5, min_periods=1).mean().T
        return rolling_df


class GoalsFor(JsonData):
    name = 'goals_for'

    def generate_data(self) -> pd.DataFrame:
        goals_for = pd.pivot_table(self.results, index='player', columns='tournament', values='BZ')
        return goals_for


class GoalsAgainst(JsonData):
    name = 'goals_against'

    def generate_data(self) -> pd.DataFrame:
        goals_against = pd.pivot_table(self.results, index='player', columns='tournament', values='BS')
        return goals_against


class GoalDifference(JsonData):
    name = 'goal_difference'

    def generate_data(self) -> pd.DataFrame:
        goal_difference = pd.pivot_table(self.results, index='player', columns='tournament', values='GD')
        return goal_difference
