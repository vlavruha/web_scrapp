import fake_headers
import requests
import bs4
import json

# Функция записи данных в файл .json
def json_file(file_name="vacancies_list.json"):

    # Имитируем запрос
    headers = fake_headers.Headers(browser="chrome", os="win")
    headers_dict = headers.generate()

    vacancies_list = []

    # Создаем тэг по вакансиям
    params = {"text": "python django flask", "area": [1, 2]}

    url = "https://spb.hh.ru/search/vacancy"

    response = requests.get(url=url, headers=headers_dict, params=params)

    html_data = response.text
    html = bs4.BeautifulSoup(html_data, 'lxml')

    vacancies_tags = html.find_all("div", {"data-sentry-element": "Element"})

    # Получаем список, где находятся необходимые нам данные и находим с помощью метода .find
    for vacancy in vacancies_tags:
        salary = "Не указано"        # так как в некоторых вакансиях не указана зп
        link = vacancy.find("a")["href"]

        # Находим сумму зп, если она есть
        if vacancy.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni"
                                       " compensation-text--kTJ0_rp54B2vNeZ3CTt2 "
                                       "separate-line-on-xs--mtby5gO4J0ixtqzW38wh"):

            # Заменяем пробельные символы с помощью .replace там где это необходимо
            salary = (vacancy.find("span", class_="fake-magritte-primary-text--Hdw8FvkOzzOcoR4xXWni "
                                                  "compensation-text--kTJ0_rp54B2vNeZ3CTt2 "
                                                  "separate-line-on-xs--mtby5gO4J0ixtqzW38wh")
                      .text.replace(u"\u202F", " ").replace(u"\xa0", " "))

        company = vacancy.find("a", {"data-qa": "vacancy-serp__vacancy-employer"}).text.replace(u"\xa0", " ")
        city = vacancy.find("span", {"data-qa": "vacancy-serp__vacancy-address"}).text

        # Создаем список вакансий
        vacancies_list.append({
            "link": link,
            "salary": salary,
            "company": company,
            "city": city
        })
    # И записываем в файл
    with open(file_name, 'w', encoding='utf-8') as f:
        json.dump(vacancies_list, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    json_file()
