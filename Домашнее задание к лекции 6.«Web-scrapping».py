import json
import requests
from bs4 import BeautifulSoup
from fake_headers import Headers

headers_generator = Headers(os='win', headers=True)
headers = headers_generator.generate()

response = requests.get('https://spb.hh.ru/search/vacancy?text=python&area=1&area=2', headers=headers)
html_data = response.text
soup = BeautifulSoup(html_data, 'lxml')

vac_list = soup.find_all('main', class_='vacancy-serp-content')

vacancies = []
for vac_tag in vac_list:
    description_tag = vac_tag.find('div', class_="HH-MainContent HH-Supernova-MainContent")
    description_text = description_tag.get_text(strip=True) if description_tag else ""

    # if "Django" in description_text and "Flask" in description_text:
    vac_link_tag = vac_tag.find('a', class_='bloko-link')
    vac_link = vac_link_tag.get('href') if vac_link_tag else ""

    vac_salary_tag = vac_tag.find('span', class_='serp-item__title serp-item__title-link')
    vac_salary = vac_salary_tag.get_text() if vac_salary_tag else ""

    vac_employer_tag = vac_tag.find('a', class_='bloko-link bloko-link_kind-tertiary')
    vac_employer = vac_employer_tag.get_text() if vac_employer_tag else ""

    vac_city_tag = vac_tag.find('span', class_='serp-item__title serp-item__title-link')
    vac_city = vac_city_tag.get_text() if vac_city_tag else ""

    vacancies.append({
        'link': vac_link,
        'salary': vac_salary,
        'employer': vac_employer,
        'city': vac_city
    })

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)
