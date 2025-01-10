import numpy as np
import pandas as pd

from src.helpers import get_sanitized_results


def xxx(results):
    global last_five_tournaments
    results['points_per_match'] = results['Points'] / results['RM']
    results['coef'] = results['points_per_match'] / results['Rank']
    df = pd.pivot_table(results, index='player', columns='tournament', values='coef')
    df_normalized = df.div(df.max())
    rolling_df = df_normalized.rolling(window=5, axis=1, min_periods=1).mean()
    # print(df_normalized)
    # print(rolling_df)
    last_five_tournaments = rolling_df.iloc[:, -1]

    return last_five_tournaments


def ver1(last_five_tournaments):
    number_of_bins = 5  # number of steps in "stars"
    seeding, bins = pd.cut(last_five_tournaments, bins=number_of_bins, retbins=True, labels=range(number_of_bins))

    print(seeding, bins)

    new = pd.DataFrame(last_five_tournaments)
    new['seeding'] = 5 - seeding.astype(int) * 0.5

    print(new.sort_values(by='seeding', ascending=False))


def ver2(last_five_tournaments):
    bins = np.linspace(0, 1, 5)
    print(bins)
    seeding, bins = pd.cut(last_five_tournaments, bins=bins, retbins=True)

    print(seeding, bins)

    new = pd.DataFrame(last_five_tournaments)
    new['seeding'] = 5 - seeding.astype(int) * 0.5

    print(new.sort_values(by='seeding', ascending=False))


if __name__ == '__main__':
    results = pd.read_csv('docs/assets/wyniki2.csv')
    tournaments = pd.read_csv('docs/assets/turnieje.csv')

    results = get_sanitized_results(results)

    last_five_tournaments = xxx(results)
    print(last_five_tournaments)

    ver2(last_five_tournaments)
