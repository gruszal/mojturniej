import pandas as pd
from jinja2 import Environment, FileSystemLoader, select_autoescape

from src.helpers import create_context, get_sanitized_results
from src.json_data_helpers import generate_jsons

if __name__ == '__main__':
    results = pd.read_csv('docs/assets/wyniki2.csv')
    tournaments = pd.read_csv('docs/assets/turnieje.csv')

    results = get_sanitized_results(results)

    generate_jsons(results)

    env = Environment(
        loader=FileSystemLoader("."),
        autoescape=select_autoescape()
    )
    template = env.get_template("src/template.html")
    context = create_context(results, tournaments)

    with open("index.html", mode="w") as f:
        content = template.render(context)
        f.write(content)
