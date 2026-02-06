from pathlib import Path

import pandas as pd

from src.helpers import update_team_and_rank


class KeysEN:
    TEAM1 = 'Team 1'
    RESULT_TEAM1 = 'Result team 1'
    TEAM2 = 'Team 2'
    RESULT_TEAM2 = 'Result team 2'
    ROUND = "Round"
    PHASE = "Phase"
    GROUP = "Group"


class KeysPL:
    TEAM1 = 'Drużyna 1'
    RESULT_TEAM1 = 'Wynik drużyna 1'
    TEAM2 = 'Drużyna 2'
    RESULT_TEAM2 = 'Wynik drużyna 2'
    ROUND = "Runda"
    PHASE = "Faza"
    GROUP = "Grupa"


class TournifyImporter:
    def __init__(self, keys: KeysPL | KeysEN, export_file: Path, tournament_name: str = "Sample Tournament"):
        self.keys = keys
        self.export_file = export_file
        self.tournament_name = tournament_name

    def convert_to_football_table(self, df) -> pd.DataFrame:
        # Get all unique players
        all_players = set(df[self.keys.TEAM1].tolist() + df[self.keys.TEAM2].tolist())

        # Initialize stats dictionary
        stats = {}
        for player in all_players:
            stats[player] = {
                'RM': 0,  # Matches played
                'Z': 0,  # Wins
                'R': 0,  # Draws
                'P': 0,  # Losses
                'BZ': 0,  # Goals scored
                'BS': 0  # Goals conceded
            }

        # Process each match
        for _, row in df.iterrows():
            team1 = row[self.keys.TEAM1]
            team2 = row[self.keys.TEAM2]
            goals1 = row[self.keys.RESULT_TEAM1]
            goals2 = row[self.keys.RESULT_TEAM2]

            # Update matches played
            stats[team1]['RM'] += 1
            stats[team2]['RM'] += 1

            # Update goals
            stats[team1]['BZ'] += goals1
            stats[team1]['BS'] += goals2
            stats[team2]['BZ'] += goals2
            stats[team2]['BS'] += goals1

            # Update wins/draws/losses
            if goals1 > goals2:
                stats[team1]['Z'] += 1
                stats[team2]['P'] += 1
            elif goals1 < goals2:
                stats[team2]['Z'] += 1
                stats[team1]['P'] += 1
            else:
                stats[team1]['R'] += 1
                stats[team2]['R'] += 1

        # Create result dataframe
        result_data = []
        for player in all_players:
            player_stats = stats[player]
            points = player_stats['Z'] * 3 + player_stats['R'] * 1
            gd = player_stats['BZ'] - player_stats['BS']

            result_data.append({
                'player': player,
                'team': player,  # Assuming player and team are the same
                'Rank': 0,  # Will be calculated after sorting
                'RM': player_stats['RM'],
                'Z': player_stats['Z'],
                'R': player_stats['R'],
                'P': player_stats['P'],
                'BZ': player_stats['BZ'],
                'BS': player_stats['BS'],
                'tournament': self.tournament_name,
                'GD': gd,
                'Points': points,
                'place': 0  # Will be calculated after sorting
            })

        # Convert to dataframe and sort by points (descending), then by GD (descending), then by BZ (descending)
        result_df = pd.DataFrame(result_data)
        result_df = result_df.sort_values(['Points', 'GD', 'BZ'], ascending=[False, False, False]).reset_index(
            drop=True)

        # Add rank and place (both are the same in this case)
        result_df['Rank'] = float()
        result_df['place'] = range(1, len(result_df) + 1)

        return result_df

    def read_tournament_from_tournify_export(self) -> pd.DataFrame:
        df = pd.read_excel(self.export_file)
        df = df[[self.keys.TEAM1, self.keys.RESULT_TEAM1, self.keys.TEAM2, self.keys.RESULT_TEAM2]]
        df = df[~df[self.keys.RESULT_TEAM1].isna()]

        df[self.keys.RESULT_TEAM1] = df[self.keys.RESULT_TEAM1].str.replace("*", "").astype(int)
        df[self.keys.RESULT_TEAM2] = df[self.keys.RESULT_TEAM2].str.replace("*", "").astype(int)
        return df

    def add_tournament_from_tournify(self, results: pd.DataFrame, tournaments: pd.DataFrame, *, teams,
                                     date=None, host=None, notes=None):
        df_matches = self.read_tournament_from_tournify_export()
        table = self.convert_to_football_table(df_matches)

        for player in teams:
            # TODO: check if "player[0]" is in players in the tournamens
            table = update_team_and_rank(table, player[0], player[1], player[2])

        results = pd.concat([results, table])

        if date and host and notes:
            new_tournament = pd.DataFrame([{"turniej": self.tournament_name, "data": date, "host": host, "notes": notes}])
            tournaments = pd.concat([tournaments, new_tournament])

        return results, tournaments


if __name__ == "__main__":
    excel_file = Path(__file__).parent / ".." / "results" / "Match schedule - Mój Turniej 15.xlsx"
    ti = TournifyImporter(KeysEN(), excel_file, tournament_name="15")

    # excel_file = Path(__file__).parent / ".." / "results" / "Harmonogram meczowy - Mój Turniej 17.xlsx"
    # ti = TournifyImporter(KeysPL(), excel_file, tournament_name="Sample Tournament")


    df_matches = ti.read_tournament_from_tournify_export()
    table = ti.convert_to_football_table(df_matches)
    print(table)
