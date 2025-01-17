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
        self.results['points_per_match'] = self.results['Points'] / self.results['RM']
        self.results['coef'] = self.results['points_per_match'] / self.results['Rank']

        df = pd.pivot_table(self.results, index='player', columns='tournament', values='coef')

        df_normalized = df.div(df.max())
        return df_normalized


class FiveTournamentRollingCoefficient(CoefficientPerTournament):
    name = 'five_tournament_rolling_coefficient'

    def generate_data(self):
        df_normalized = super().generate_data()
        rolling_df = df_normalized.T.rolling(window=5, min_periods=1).mean().T
        return rolling_df


class AllTournamentsRollingCoefficient(CoefficientPerTournament):
    name = 'all_tournament_rolling_coefficient'

    def generate_data(self):
        cpt = super().generate_data()
        rolling_cpt = cpt.T.rolling(window=cpt.shape[1], min_periods=1).sum().T
        return rolling_cpt


class GoalsFor(JsonData):
    name = 'goals_for'

    def generate_data(self) -> pd.DataFrame:
        goals_for = pd.pivot_table(self.results, index='player', columns='tournament', values='BZ')
        return goals_for


class GoalsAgainst(JsonData):
    name = 'goals_against'

    def generate_data(self) -> pd.DataFrame:
        goals_against = pd.pivot_table(self.results, index='player', columns='tournament', values='BS')
        goals_against = goals_against * -1
        return goals_against


class GoalDifference(JsonData):
    name = 'goal_difference'

    def generate_data(self) -> pd.DataFrame:
        goal_difference = pd.pivot_table(self.results, index='player', columns='tournament', values='GD')
        return goal_difference


def generate_jsons(result: pd.DataFrame) -> None:
    json_data_classes = [
        PlacesPerTournament,
        PointsPerTournament,
        PointsPerMatchPerTournament,
        CoefficientPerTournament,
        FiveTournamentRollingCoefficient,
        AllTournamentsRollingCoefficient,
        GoalsFor,
        GoalsAgainst,
        GoalDifference,
    ]

    for json_data_class in json_data_classes:
        json_data_class(result).save_json()
