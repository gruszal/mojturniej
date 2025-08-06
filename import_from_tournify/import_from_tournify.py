from pathlib import Path

import pandas as pd




def convert_to_football_table(df, tournament_name="Tournament") -> pd.DataFrame:
    """
    Converts match results dataframe to football league table format.

    Parameters:
    df: DataFrame with columns ['Team 1', 'Result team 1', 'Team 2', 'Result team 2']
    tournament_name: Name of the tournament (default: "Tournament")

    Returns:
    DataFrame with football table format including Polish abbreviations:
    - RM: Rozegrane Mecze (Matches Played)
    - Z: Zwycięstwa (Wins)
    - R: Remisy (Draws)
    - P: Porażki (Losses)
    - BZ: Bramki Zdobyte (Goals Scored)
    - BS: Bramki Stracone (Goals Conceded)
    - GD: Goal Difference (Różnica bramek)
    - Points: Points (3 for win, 1 for draw, 0 for loss)
    """

    # Get all unique players
    all_players = set(df['Team 1'].tolist() + df['Team 2'].tolist())

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
        team1 = row['Team 1']
        team2 = row['Team 2']
        goals1 = row['Result team 1']
        goals2 = row['Result team 2']

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
            'tournament': tournament_name,
            'GD': gd,
            'Points': points,
            'place': 0  # Will be calculated after sorting
        })

    # Convert to dataframe and sort by points (descending), then by GD (descending), then by BZ (descending)
    result_df = pd.DataFrame(result_data)
    result_df = result_df.sort_values(['Points', 'GD', 'BZ'], ascending=[False, False, False]).reset_index(drop=True)

    # Add rank and place (both are the same in this case)
    result_df['Rank'] = float()
    result_df['place'] = range(1, len(result_df) + 1)

    return result_df

def read_tournament_from_tournify_export(export_file:Path) -> pd.DataFrame:

    df = pd.read_excel(export_file)
    df = df[["Team 1", "Result team 1", "Team 2", "Result team 2"]]
    df = df[~df["Result team 1"].isna()]

    df["Result team 1"] = df["Result team 1"].str.replace("*", "").astype(int)
    df["Result team 2"] = df["Result team 2"].str.replace("*", "").astype(int)
    return df

# Example usage with your data
if __name__ == "__main__":
    excel_file = Path(__file__).parent / ".." / "results" / "Match schedule - Mój Turniej 15.xlsx"

    df_matches = read_tournament_from_tournify_export(excel_file)
    table = convert_to_football_table(df_matches, "Sample Tournament")
    print(table)


    # ['player', 'team', 'Rank', 'RM', 'Z', 'R', 'P', 'BZ', 'BS', 'tournament', 'GD', 'Points', 'place']