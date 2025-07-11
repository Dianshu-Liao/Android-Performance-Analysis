import requests
from bs4 import BeautifulSoup
import csv
import re
import tqdm
from utils import Utils
import pandas as pd

def judge(title, keyword1, keyword3):
    title_lower = title.lower()
    keyword1_lower = keyword1.lower()
    # keyword2_lower = keyword2.lower()
    keyword3_lower = keyword3.lower()

    # 构建正则表达式模式以匹配完整的单词或词组
    pattern1 = r'\b' + re.escape(keyword1_lower) + r'\b'
    # pattern2 = r'\b' + re.escape(keyword2_lower) + r'\b'
    pattern3 = r'\b' + re.escape(keyword3_lower) + r'\b'

    # 判断 title 中是否同时包含三个关键词
    return (re.search(pattern1, title_lower) and
            # re.search(pattern2, title_lower) and
            re.search(pattern3, title_lower))


def get_all_papers_from_springer(keywords_group1, keywords_group2, saved_dir='data/Springer'):


    files = Utils.get_all_subfiles(saved_dir)


    for keyword_g1 in tqdm.tqdm(keywords_group1):
        for keyword_g2 in keywords_group2:
        # for keyword_g3 in tqdm.tqdm(keywords_group3):
            dict_keywords = {'keyword': [], 'title': [], 'publication': []}
            # print(f'keyword1: {keyword_g1}, keyword2: {keyword_g2}, keyword3: {keyword_g3}')
            url = f'https://link.springer.com/search?new-search=true&query={keyword_g1}+{keyword_g2}&sortBy=relevance'
            print(f'url: {url}')
            keywords = f'{keyword_g1}_{keyword_g2}'

            if saved_dir + '/' + keywords + '.csv' in files:
                continue

            # 发送HTTP请求获取网页内容
            response = requests.get(url)
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')

            # 获取总页数
            pagination_ul = soup.find('ul', class_='eds-c-pagination')
            pages = 0
            if pagination_ul:
                li_tags = pagination_ul.find_all('li', attrs={'data-page': True})
                # print(li_tags)
                if li_tags:
                    pages = int(li_tags[-1].get('data-page'))

            # springer最多一次搜索1k条结果，每页显示20条
            for page in range(1, min(pages+1, 51)):
                # print(f'page: {page}/{min(pages+1, 50)}')
                page_url = url + f'&page={page}'
                # 发送HTTP请求获取网页内容
                page_response = requests.get(page_url)
                # 使用BeautifulSoup解析HTML内容
                page_soup = BeautifulSoup(page_response.text, 'html.parser')
                # 找到所有的<li>标签，这些标签位于class为u-list-reset的元素下
                list_items = page_soup.select('.u-list-reset li')
                # 遍历每个<li>标签
                for item in list_items:
                    a_tag = item.find('a')
                    # 找到<a>标签下的<span>标签
                    span_tag = a_tag.find('span') if a_tag else None

                    # 获取链接和标题
                    paper_link = a_tag['href'] if a_tag else None
                    paper_title = span_tag.text if span_tag else None
                    # 找到<li>标签下的<a>标签
                    div_author = item.find('div', class_='c-author-list c-author-list--truncated c-author-list--compact')
                    a_view_journal = []
                    if div_author is not None:
                        a_view_journal = div_author.select('div a[data-track-action="view journal"]')
                    paper_source = 'None'
                    if len(a_view_journal) != 0:
                        paper_source = a_view_journal[0].get_text()

                    # print(f'title: {paper_title}')
                    # print(f'paper_source: {paper_source}\n')
                    # 将论文的链接和标题存储为一个字典，并添加到列表中
                    if (paper_link and paper_title and judge(paper_title, keyword_g1, keyword_g2)):
                        # print("Passed paper:")
                        # print(f'title: {paper_title}')
                        # print(f'paper_source: {paper_source}\n')
                        dict_keywords['keyword'].append(keywords)
                        dict_keywords['title'].append(paper_title)
                        dict_keywords['publication'].append(paper_source)
                        # papers.append({'keyword': keywords, 'paper_link': 'https://link.springer.com' + paper_link,
                        #                'paper_publication': paper_source, 'paper_title': paper_title})

            df_keywords_to_papers_publications = pd.DataFrame(dict_keywords)
            df_keywords_to_papers_publications.to_csv(saved_dir + '/' + keywords + '.csv', index=False)




if __name__ == '__main__':
    keywords_group1 = Utils.load_keywords('android_keywords.txt')
    keywords_group2 = Utils.load_keywords('pi_related_keywords.txt')

    get_all_papers_from_springer(keywords_group1, keywords_group2)