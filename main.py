import datetime
from collections import defaultdict
from http.server import HTTPServer, SimpleHTTPRequestHandler

import pandas
from jinja2 import Environment, FileSystemLoader, select_autoescape

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')

winery_foundation = datetime.datetime(1920, 1, 1)
winery_age = (datetime.datetime.now() - winery_foundation).days // 365
if winery_age % 10 in range(2, 5):
    year_description = 'года'
elif winery_age % 10 == 1:
    year_description = 'год'
else:
    year_description = 'лет'

drinks_from_xlsx = pandas.read_excel(
    'wine3.xlsx',
    na_values=None,
    keep_default_na=False,). \
    to_dict(orient='records')
drinks_serialized = defaultdict(list)

for drink in drinks_from_xlsx:
    drinks_serialized[drink['Категория']].append(drink)

rendered_page = template.render(
    winery_age=winery_age,
    year_description=year_description,
    drinks=drinks_serialized,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('0.0.0.0', 8000), SimpleHTTPRequestHandler)
server.serve_forever()
