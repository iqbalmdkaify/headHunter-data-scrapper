import urllib3
import csv
from bs4 import BeautifulSoup
import sys


dynamic_url_path = 'https://hh.ru/search/vacancy?text=Python&from=suggest_post&salary=&clusters=true&area=113&ored_clusters=true&enable_snippets=true&page=2&hhtmFrom=vacancy_search_list&customDomain=1'

search_input = sys.argv[1]  # Что поискать вв hh.ru

http = urllib3.PoolManager()

search_tags = {
    'vacancy_name_a': 'serp-item__title',
    'vacancy_salary_span': 'bloko-header-section-3',
    'vacancy_company_name_a': 'bloko-link bloko-link_kind-tertiary',
    'vacancy_address_attr_data-qa': 'vacancy-serp__vacancy-address',
    'vacancy_responsibility_div_attr_data-qa': 'vacancy-serp__vacancy_snippet_responsibility',
    'vacancy_requirement_div_attr_data-qa': 'vacancy-serp__vacancy_snippet_requirement'
}

headers = ['title', 'salaries', 'company_names', 'addresses', 'requirements']


with open('data.csv', 'w') as f:
    csv_writer = csv.DictWriter(f, fieldnames=headers)

    csv_writer.writeheader()

f.close()


for page in range(0, 100):

    print(f'page: {page}')
    response = http.request(
        'GET', f'https://hh.ru/search/vacancy?text={search_input}&from=suggest_post&salary=&clusters=true&area=113&ored_clusters=true&enable_snippets=true&page={page}&hhtmFrom=vacancy_search_list&customDomain=1')

    if response.status!=404:
        soup = BeautifulSoup(response.data, features='html5lib')
        # print(soup)

        vacany_names = [k.text for k in soup.find_all('a', class_='serp-item__title')]

        vacany_find = [k for k in soup.find_all(
            'div', class_='vacancy-serp-item-body__main-info')]

            # check
        vacany_salary = []
        for element in vacany_find:
            if 'vacancy-serp__vacancy-compensation' in str(element):
                vacany_salary.append(''.join([k.text for k in soup.find(
                    'span', class_='bloko-header-section-3')]))

            elif 'vacancy-serp__vacancy-compensation' not in str(element):
                vacany_salary.append('Not provided')
            # print(element, '\n')
            
        company_names = [k.text for k in soup.find_all(
            'a', class_='bloko-link bloko-link_kind-tertiary')]
        vacany_address = [k.text for k in soup.find_all(
            'div', {'data-qa': 'vacancy-serp__vacancy-address'})]

        vacany_requirements_finds = [k for k in soup.find_all(
            'div', class_='vacancy-serp-item__info')]

        vacany_requirements = []
        for element in vacany_requirements_finds:
            if 'vacancy-serp__vacancy_snippet_requirement' in str(element):
                vacany_requirements.append(''.join([k.text for k in soup.find_all(
                    'div', {'data-qa': 'vacancy-serp__vacancy_snippet_requirement'})]))
            # check
            elif 'vacancy-serp__vacancy-compensation' not in str(element):
                vacany_requirements.append('Not provided')

        
        # print(len(vacany_names), len(vacany_address), len(company_names), len(vacany_salary), len(vacany_requirements), '\n\n')
        with open('data.csv', 'a', encoding='utf-8') as f:
            writer = csv.writer(f)

            for m in range(len(vacany_names)):

                writer.writerow([vacany_names[m], vacany_salary[m], company_names[m], vacany_address[m], vacany_requirements[m]])

        f.close()
    else:
        print('Search finished')
        break
