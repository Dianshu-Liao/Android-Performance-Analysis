import tqdm
import random
import time
from utils import Utils
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd

def Wiley_Paper_Crawling(url):
    titles = []
    paper_publications = []

    browser = webdriver.Chrome()
    browser.get(url)
    # time.sleep(3)


    div_elements = browser.find_elements(By.CLASS_NAME, "item__body")

    for div_element in div_elements:
        div_element_text = div_element.text
        div_element_text_list = div_element.text.split('\n')

        if (div_element_text_list[1] == 'Full Access') | (div_element_text_list[1] == 'Free Access')| (div_element_text_list[1] == 'Open Access'):
            title_name = div_element_text_list[2]
        else:
            title_name = div_element_text_list[1]
        # if collection is in the last second line: -5
        # else: -4

        if 'Abstract' == div_element_text_list[-1]:
            if 'Collections: ' in div_element_text_list[-2]:
                if 'OpenURL' == div_element_text_list[-3]:
                    if 'First published: ' in div_element_text_list[-4]:
                        paper_publication = div_element_text_list[-5]
                    else:
                        a = 1
                else:
                    a = 1
            else:
                if ('OpenURL' == div_element_text_list[-2]) & ('First published: ' in div_element_text_list[-3]):
                    paper_publication = div_element_text_list[-4]
                else:
                    a = 1

        else:
            if 'Summary' == div_element_text_list[-1]:
                if ('OpenURL' == div_element_text_list[-2]) & ('First published: ' in div_element_text_list[-3]):
                    paper_publication = div_element_text_list[-4]
                else:
                    a = 1
            else:
                if 'Volume' in div_element_text_list[-1]:
                    paper_publication = div_element_text_list[-2]
                else:
                    if ('Description' == div_element_text_list[-1]) & ('First published: ' in div_element_text_list[-2]):
                        paper_publication = div_element_text_list[-4]
                    else:
                        if ('OpenURL' == div_element_text_list[-1]) & ('First published: ' in div_element_text_list[-2]):
                            paper_publication = div_element_text_list[-3]
                        else:
                            if ('Collections: ' in div_element_text_list[-1]) & ('OpenURL' == div_element_text_list[-2]) & ('First published: ' in div_element_text_list[-3]):
                                paper_publication = div_element_text_list[-4]
                            else:
                                a = 1

        # if 'Collections: ' in div_element_text_list[-2]:
        #     paper_publication = div_element_text_list[-5]
        # else:
        #     paper_publication = div_element_text_list[-4]
        # if paper_publication == 'Full Access':
        #     a = 1
        titles.append(title_name)
        paper_publications.append(paper_publication)
    return titles, paper_publications


def get_all_papers_from_Wiley(keywords_group1, keywords_group2, saved_dir='data/Wiley'):

    files = Utils.get_all_subfiles(saved_dir)
    # dict_keywords_to_papers = {'keyword': [], 'title': [], 'publication': []}
    url_template = "https://onlinelibrary.wiley.com/action/doSearch?Ppub=&field1=Title&field2=Title&publication=&startPage=#{pagenumber}#&text1=#{keyword1}#&text2=#{keyword2}#&pageSize=20"

    for keyword_g1 in tqdm.tqdm(keywords_group1):
        for keyword_g2 in keywords_group2:
            dict_keywords = {'keyword': [], 'title': [], 'publication': []}

            keywords = f'{keyword_g1}_{keyword_g2}'

            if saved_dir + '/' + keywords + '.csv' in files:
                continue

            url_with_keyword_1_2 = url_template.replace('#{keyword1}#', keyword_g1).replace('#{keyword2}#', keyword_g2)
            paper_number=0
            # titles_with_keyword_g1_g2 = []

            while True:
                # time.sleep(random.randint(2,5))
                url_with_page = url_with_keyword_1_2.replace('#{pagenumber}#', str(paper_number))
                titles, paper_publications = Wiley_Paper_Crawling(url_with_page)
                # titles_with_keyword_g1_g2 += titles
                paper_number += 1
                if titles == []:
                    break


                if len(titles) != len(paper_publications):
                    raise ValueError('number of papers not equal to publications!!!')

                for i in range(len(titles)):
                    title = titles[i]
                    publication = paper_publications[i]
                    dict_keywords['keyword'].append(keywords)
                    dict_keywords['title'].append(title)
                    dict_keywords['publication'].append(publication)
                    a = 1



            df_keywords_to_papers_publications = pd.DataFrame(dict_keywords)
            df_keywords_to_papers_publications.to_csv(saved_dir + '/' + keywords + '.csv', index=False)
            # if keywords in dict_keywords_to_papers:
            #     raise ValueError('more than twice matched!!! Check the code!!!')
            # else:
            #     dict_keywords_to_papers[keywords] = titles_with_keyword_g1_g2
            # print('titles: {}'.format(titles_with_keyword_g1_g2))
            # Utils.save_list_to_pkl(titles_with_keyword_g1_g2, 'Wiley/' + keywords + '.txt')

    # # Utils.dict_to_json(dict_keywords_to_papers, saved_json_path)
    # df_keywords_to_papers_publications = pd.DataFrame(dict_keywords_to_papers)
    # df_keywords_to_papers_publications.to_csv(saved_path, index=False)

if __name__ == '__main__':


    keywords_group1 = Utils.load_keywords('android_keywords.txt')
    keywords_group2 = Utils.load_keywords('pi_related_keywords.txt')

    get_all_papers_from_Wiley(keywords_group1, keywords_group2)