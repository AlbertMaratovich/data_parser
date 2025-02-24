import requests
from bs4 import BeautifulSoup
import pandas as pd


def collect_user_rates(user_login):
    page_num = 1

    data = []

    while True:
        url = f'https://letterboxd.com/{user_login}/films/diary/page/{page_num}/'
        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, 'lxml')

        entries = soup.find_all('tr', class_='diary-entry-row viewing-poster-container')
        print(entries)

        if len(entries) == 0:  # Признак остановки
            break

        for entry in entries:
            td_film_details = entry.find('td', class_='td-film-details')
            film_name = td_film_details.find('a').text

            release_date = entry.find('td', class_='td-released center').text

            td_rating_rating_green = entry.find('td', class_='td-rating rating-green')
            rating_span = td_rating_rating_green.find('span', class_='rating')
            classes = rating_span.get('class', [])

            rating = classes[1].split('-')[1]

            data.append({'film_name': film_name, 'release_date': release_date, 'rating': rating})

        page_num += 1  # Переходим на следующую страницу

    return data


user_rates = collect_user_rates(user_login='rfeldman9')
df = pd.DataFrame(user_rates)

df.to_excel('user_rates.xlsx')
