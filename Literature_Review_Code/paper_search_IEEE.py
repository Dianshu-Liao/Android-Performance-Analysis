
#IEEE
#ACM
#Springer
#Science Direct
#Wiley


import pandas as pd

import tqdm
import random
import time
from LargeDataCrawler.utils import Utils
from selenium import webdriver
from selenium.webdriver.common.by import By

def IEEE_Paper_Crawling(url):
    titles = []
    paper_publications = []
    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    div_elements = browser.find_elements(By.CLASS_NAME, "List-results-items")

    for div_element in div_elements:
        try:
            div_element_text_list = div_element.text.split('\n')
            if div_element_text_list[-1] == 'HTML':
                if 'Cited by: Papers (' in div_element_text_list[-3]:
                    paper_publication = div_element_text_list[-5]
                else:
                    paper_publication = div_element_text_list[-4]
            else:
                if 'Cited by: Papers (' in div_element_text_list[-2]:
                    paper_publication = div_element_text_list[-4]
                else:
                    paper_publication = div_element_text_list[-3]
        except:
            # this is not a paper
            continue
        title_name = div_element_text_list[0]

        titles.append(title_name)
        paper_publications.append(paper_publication)
    return titles, paper_publications


def get_all_papers_from_IEEE_library(keywords_group1, keywords_group2, saved_path):
    dict_keywords_to_papers = {'keyword': [], 'title': [], 'publication': []}

    # dict_keywords_to_papers = {}
    url_template = "https://ieeexplore.ieee.org/search/searchresult.jsp?action=search&newsearch=true&matchBoolean=true&queryText=(%22Document%20Title%22:#{keyword1}#)%20AND%20(%22Document%20Title%22:#{keyword2}#)&highlight=true&returnType=SEARCH&matchPubs=true&pageNumber=#{pagenumber}#&returnFacets=ALL"
    files = Utils.get_all_subfiles('IEEE_Library')

    for keyword_g1 in tqdm.tqdm(keywords_group1):
        for keyword_g2 in keywords_group2:
            dict_keywords = {'keyword': [], 'title': [], 'publication': []}

            keywords = keyword_g1 + ' ' + keyword_g2
            if 'IEEE_Library\\'+keywords+'.csv' in files:
                continue
            url_with_keyword_1_2 = url_template.replace('#{keyword1}#', keyword_g1).replace('#{keyword2}#', keyword_g2)
            page_number=1
            # titles_with_keyword_g1_g2 = []

            while True:
                time.sleep(random.randint(2,5))
                url_with_page = url_with_keyword_1_2.replace('#{pagenumber}#', str(page_number))
                titles, paper_publications = IEEE_Paper_Crawling(url_with_page)
                # titles_with_keyword_g1_g2 += titles
                page_number += 1
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


                    dict_keywords['keyword'].append(keywords)
                    dict_keywords['title'].append(title)
                    dict_keywords['publication'].append(publication)
                    a = 1


            # if keywords in dict_keywords_to_papers:
            #     raise ValueError('more than twice matched!!! Check the code!!!')
            # else:
            #     dict_keywords_to_papers[keywords] = titles_with_keyword_g1_g2
            # print('titles: {}'.format(titles_with_keyword_g1_g2))
            df_keywords_to_papers_publications = pd.DataFrame(dict_keywords)
            df_keywords_to_papers_publications.to_csv('IEEE_Library/'+ keywords + '.csv', index=False)

    # Utils.dict_to_json(dict_keywords_to_papers, saved_json_path)

    # df_keywords_to_papers_publications = pd.DataFrame(dict_keywords_to_papers)
    # df_keywords_to_papers_publications.to_csv(saved_path, index=False)


if __name__ == '__main__':
    keywords_group1 = ['android', 'mobile', 'phone', 'phones', 'smartphone', 'smartphones']
    keywords_group2 = ['performance', 'speed', 'resource', 'energy', 'responsiveness', 'issue', 'issues']

    get_all_papers_from_IEEE_library(keywords_group1, keywords_group2, saved_path='data/IEEE_Library_Papers.csv')

