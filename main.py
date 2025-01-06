import pandas as pd
from jinja2 import Environment, select_autoescape, FileSystemLoader

results = pd.read_csv('wyniki2.csv')
tournaments = pd.read_csv('turnieje.csv')


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

        # move place column to front
        data.insert(0, 'place', data.pop('place'))

        pandas_table = data.to_html(classes='table table-striped', index=False)

        single_tournament = {
            'id': id_,
            'name': f"Mój Turniej {id_}",
            'date': date,
            'data': data,
            'pandas_table': pandas_table,
        }
        context_tournaments.append(single_tournament)

    return {'tournaments': context_tournaments}


if __name__ == '__main__':
    results = fix_commas_in_rank(results)
    results = convert_column_to_int(results, "BZ")
    results = convert_column_to_int(results, "BS")
    results = add_goal_difference_column(results)
    results = add_points_column(results)
    results = add_tournament_place(results)

    print(results)
    print(tournaments)

    env = Environment(
        loader=FileSystemLoader("."),
        # autoescape=select_autoescape()
        # NOTE: the line above messes with pandas' builtin data.to_html()
    )
    template = env.get_template("template.html")

    context = create_context(results, tournaments)

    with open("index.html", mode="w") as f:
        content = template.render(context)
        f.write(content)

    print(content)
