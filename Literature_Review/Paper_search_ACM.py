import pandas as pd
#IEEE
#ACM
#Springer
#Science Direct
#Wiley

import requests
from bs4 import BeautifulSoup
import tqdm
import random
import time
from utils import Utils
def ACM_Paper_Crawling(url):
    titles = []
    paper_publications = []
    # 定义目标网页的 URL

    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36'}

    time.sleep(random.randint(5, 10))

    # 发送 GET 请求并获取页面内容
    response = requests.get(url, headers=headers)

    # 使用 BeautifulSoup 解析页面内容
    soup = BeautifulSoup(response.content, "html.parser")

    # 找到包含所有 items 的 <ul> 标签
    ul_tag = soup.find("ul", class_="search-result__xsl-body items-results rlist--inline")
    if ul_tag == None:
        return [], []

    li_tags = ul_tag.find_all("li", class_="search__item issue-item-container")

    for li_tag in li_tags:
        div_tag = li_tag.find("div", class_="issue-item issue-item--search clearfix")
        div_issue_item = (div_tag.find("div", class_="issue-item__content").find("div", class_="issue-item__content-right"))

        #none type for paper publication
        if div_issue_item.find('span', class_='epub-section__title') == None:
            continue

        # title = div_issue_item.find("h5", class_="issue-item__title").find("span", class_="hlFld-Title")
        title = div_issue_item.find("h5", class_="issue-item__title").get_text()
        # if title == None:
        #     title = div_issue_item.find("h5", class_="issue-item__title").find("span", class_="hlFld-ContentGroupTitle")
        # 提取纯文本标题
        # plain_text_title = title.get_text()
        titles.append(title)

        paper_publication = div_issue_item.find('span', class_='epub-section__title').text
        if paper_publication == None:
            a = 1

        paper_publications.append(paper_publication)

    return titles, paper_publications


def get_all_papers_from_ACM_library(keywords_group1, keywords_group2, saved_dir='data/ACM_Library'):


    # url_template = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&AllField=Title%3A%28#{keyword1}#%29+AND+Title%3A%28#{keyword2}#%29+AND+Title%3A%28#{keyword3}#%29&startPage=#{pagenumber}#&pageSize=50"
    url_template = "https://dl.acm.org/action/doSearch?fillQuickSearch=false&target=advanced&expand=dl&AllField=Title%3A%28#{keyword1}#%29+AND+Title%3A%28#{keyword2}#%29&startPage=#{pagenumber}#&pageSize=50"

    files = Utils.get_all_subfiles(saved_dir)

    for keyword_g1 in tqdm.tqdm(keywords_group1):
        for keyword_g2 in keywords_group2:
            dict_keywords_to_papers = {'keyword': [], 'title': [], 'publication': []}
            keyword_g1 = keyword_g1.replace(' ', '+')
            keyword_g2 = keyword_g2.replace(' ', '+')
            keywords = f'{keyword_g1}_{keyword_g2}'
            if saved_dir + '/' + keywords + '.csv' in files:
                continue
            url_with_keyword_1_2 = (url_template.replace('#{keyword1}#', keyword_g1)
                                                  .replace('#{keyword2}#', keyword_g2))
            index = 0
            while True:
                time.sleep(random.randint(2, 5))
                url_with_page = url_with_keyword_1_2.replace('#{pagenumber}#', str(index))
                titles, paper_publications = ACM_Paper_Crawling(url_with_page)
                index += 1
                if titles == []:
                    break

                if len(titles) != len(paper_publications):
                    raise ValueError('number of papers not equal to publications!!!')

                for i in range(len(titles)):
                    title = titles[i]
                    publication = paper_publications[i]
                    dict_keywords_to_papers['keyword'].append(keywords)
                    dict_keywords_to_papers['title'].append(title)
                    dict_keywords_to_papers['publication'].append(publication)

            df_keywords_to_papers_publications = pd.DataFrame(dict_keywords_to_papers)
            df_keywords_to_papers_publications.to_csv(saved_dir + '/' + keywords + '.csv', index=False)



if __name__ == '__main__':

    keywords_group1 = Utils.load_keywords('android_keywords.txt')
    keywords_group2 = Utils.load_keywords('pi_related_keywords.txt')

    get_all_papers_from_ACM_library(keywords_group1, keywords_group2)












