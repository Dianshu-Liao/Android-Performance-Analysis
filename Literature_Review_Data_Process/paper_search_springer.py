import requests
from bs4 import BeautifulSoup
import csv
import re

keywords_group1 = ['android', 'mobile', 'phone', 'phones', 'smartphone', 'smartphones']
keywords_group2 = ['performance', 'resource', 'energy', 'responsiveness', 'issue', 'issues']
papers = []
for k1 in keywords_group1:
    for k2 in keywords_group2:
        print(f'keyword1: {k1}, keyword2: {k2}')
        url = f'https://link.springer.com/search?new-search=true&query={k1}+{k2}&sortBy=relevance'
        keyword = f'{k1} {k2}'
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        pagination_ul = soup.find('ul', class_='eds-c-pagination')
        pages = 0
        if pagination_ul:
            li_tags = pagination_ul.find_all('li', attrs={'data-page': True})
            if li_tags:
                pages = int(li_tags[-1].get('data-page'))


        for page in range(1, min(pages+1, 51)):
            print(f'page: {page}/{min(pages+1, 50)}')
            page_url = url + f'&page={page}'

            page_response = requests.get(page_url)

            page_soup = BeautifulSoup(page_response.text, 'html.parser')

            list_items = page_soup.select('.u-list-reset li')

            for item in list_items:

                div_author = item.find('div', class_='c-author-list c-author-list--truncated c-author-list--compact')
                a_view_journal = div_author.select('div a[data-track-action="view journal"]')
                paper_source = 'None'
                if a_view_journal:
                    paper_source = a_view_journal[0].get_text()
                a_tag = item.find('a')

                span_tag = a_tag.find('span') if a_tag else None


                paper_link = a_tag['href'] if a_tag else None
                paper_title = span_tag.text if span_tag else None

                if paper_link and paper_title and k1 in paper_title.lower() and k2 in paper_title.lower():
                    papers.append({'keyword': keyword, 'paper_link': 'https://link.springer.com' + paper_link,
                                   'paper_publication': paper_source, 'paper_title': paper_title})


with open('Springer/springer.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['keyword', 'paper_title', 'paper_publication', 'paper_link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for paper in papers:
        writer.writerow(paper)


print('CSV file has been created successfully.')
