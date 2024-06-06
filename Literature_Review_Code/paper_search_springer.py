import requests
from bs4 import BeautifulSoup
import csv
import re

keywords_group1 = ['android', 'mobile', 'phone', 'phones', 'smartphone', 'smartphones']
keywords_group2 = ['performance', 'speed', 'resource', 'energy', 'responsiveness', 'issue', 'issues']
papers = []
for k1 in keywords_group1:
    for k2 in keywords_group2:
        print(f'keyword1: {k1}, keyword2: {k2}')
        url = f'https://link.springer.com/search?new-search=true&query={k1}+{k2}&sortBy=relevance'
        keyword = f'{k1} {k2}'
        # 发送HTTP请求获取网页内容
        response = requests.get(url)
        # 使用BeautifulSoup解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取总页数
        pagination_ul = soup.find('ul', class_='eds-c-pagination')
        pages = 0
        if pagination_ul:
            li_tags = pagination_ul.find_all('li', attrs={'data-page': True})
            if li_tags:
                pages = int(li_tags[-1].get('data-page'))

        # springer最多一次搜索1k条结果，每页显示20条
        for page in range(1, min(pages+1, 51)):
            print(f'page: {page}/{min(pages+1, 50)}')
            page_url = url + f'&page={page}'
            # 发送HTTP请求获取网页内容
            page_response = requests.get(page_url)
            # 使用BeautifulSoup解析HTML内容
            page_soup = BeautifulSoup(page_response.text, 'html.parser')
            # 找到所有的<li>标签，这些标签位于class为u-list-reset的元素下
            list_items = page_soup.select('.u-list-reset li')
            # 遍历每个<li>标签
            for item in list_items:
                # 找到<li>标签下的<a>标签
                div_author = item.find('div', class_='c-author-list c-author-list--truncated c-author-list--compact')
                a_view_journal = div_author.select('div a[data-track-action="view journal"]')
                paper_source = 'None'
                if a_view_journal:
                    paper_source = a_view_journal[0].get_text()
                a_tag = item.find('a')
                # 找到<a>标签下的<span>标签
                span_tag = a_tag.find('span') if a_tag else None

                # 获取链接和标题
                paper_link = a_tag['href'] if a_tag else None
                paper_title = span_tag.text if span_tag else None
                # print(f'title: {paper_title}')
                # print(f'paper_source: {paper_source}\n')
                # 将论文的链接和标题存储为一个字典，并添加到列表中
                if paper_link and paper_title and k1 in paper_title.lower() and k2 in paper_title.lower():
                    papers.append({'keyword': keyword, 'paper_link': 'https://link.springer.com' + paper_link,
                                   'paper_publication': paper_source, 'paper_title': paper_title})

# 写入CSV文件
with open('data/springer.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['keyword', 'paper_title', 'paper_publication', 'paper_link']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    for paper in papers:
        writer.writerow(paper)

# 提示用户CSV文件创建完成
print('CSV file has been created successfully.')
