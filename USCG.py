### Script to scrape all the possible combinations of boating incident data.
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import product


def scrape():
    request = requests.get('https://bard.knightpoint.systems/PublicInterface/Report1.aspx')
    content = request.content

    soup = BeautifulSoup(content, 'html.parser')

    criteria = soup.find('select', {'id': 'dlist_criteria'}).find_all('option')
    state = soup.find('select', {'id': 'dlist_state'}).find_all('option')
    year = soup.find('select', {'id': 'dlist_year'}).find_all('option')

    criteria_list = [c.text for c in criteria]
    state_list = [s.text for s in state[1:]]
    year_list = [y.text for y in year[1:]]

    combinations = list(product(criteria_list, state_list, year_list))

    dataframe = pd.DataFrame(columns=['Dimension', 'Jurisdiction', 'Year'])

    for c, s, y in combinations:
        entry = {
            'Dimension': c,
            'Jurisdiction': s,
            'Year': y
        }

        dataframe = dataframe.append(entry, ignore_index=True)

    return dataframe.to_csv('USCG Data.csv')


