import requests
from bs4 import BeautifulSoup
import pandas as pd


def collect_user_rates(user_login):
    page_num = 1

    data = []

    while True:
        url = f'https://www.kinopoisk.ru/user/{user_login}/votes/list/vs/vote/page/{page_num}/#list'
        html_content = requests.get(url).text

        soup = BeautifulSoup(html_content, 'lxml')

        entries_item = soup.find_all('div', class_='item')
        entries_even = soup.find_all('div', class_='item even')
        entries = entries_item + entries_even

        if len(entries) == 0:  # Признак остановки
            break

        for entry in entries:
            div_film_details = entry.find('div', class_="nameRus")    # тут возможна ошибка
            film_name = div_film_details.find('a').text

            # тут стоит вернуться и переделать под дату просмотра
            # release_date = entry.find('td', class_='td-released center').text

            div_select_rating = entry.find('div', class_="selects vote_widget")
            span_rating = div_select_rating.find('span')
            print(span_rating)
            rating = span_rating.find("div").text  # тут остановился
            # classes = rating_span.get('class', [])    # не понимаю что тут происходит
            # rating = classes[1].split('-')[1]

            # data.append({'film_name': film_name, 'release_date': release_date, 'rating': rating})
            data.append({'film_name': film_name, 'rating': rating})

        page_num += 1  # Переходим на следующую страницу

    return data


user_rates = collect_user_rates(user_login='130145667')
df = pd.DataFrame(user_rates)

df.to_excel('user_rates.xlsx')
