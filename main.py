import os
import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape
from dotenv import load_dotenv


def get_winery_age():
    winery_age = (datetime.datetime.now() - datetime.datetime(1920, 1, 1)). \
        days // 365
    if winery_age % 10 in range(2, 5):
        year_description = 'года'
    elif winery_age % 10 == 1:
        year_description = 'год'
    else:
        year_description = 'лет'
    return winery_age, year_description


def get_serialized_drinks(drinks):
    drinks_from_xlsx = pandas.read_excel(
        drinks,
        na_values=None,
        keep_default_na=False,). \
        to_dict(orient='records')
    serialized_drinks = defaultdict(list)

    for drink in drinks_from_xlsx:
        serialized_drinks[drink['Категория']].append(drink)
    return serialized_drinks


def main():
    load_dotenv()
    path_of_the_file_with_drinks = os.getenv('DRINKS', default='drinks.xlsx')
    drinks_serialized = get_serialized_drinks(path_of_the_file_with_drinks)
    env = Environment(
        loader=FileSystemLoader('.'),
        autoescape=select_autoescape(['html', 'xml'])
    )
    template = env.get_template('template.html')
    winery_age, year_description = get_winery_age()
    rendered_page = template.render(
        winery_age=winery_age,
        year_description=year_description,
        drinks=drinks_serialized,
    )
    with open('index.html', 'w', encoding="utf8") as file:
        file.write(rendered_page)
    server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == '__main__':
    main()