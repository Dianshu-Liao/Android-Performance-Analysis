import tqdm
import random
import time
from utils import Util
from selenium import webdriver
from selenium.webdriver.common.by import By
import re
import pandas as pd

def Science_Direct_Paper_Crawling(url):
    titles = []
    paper_publications = []

    browser = webdriver.Chrome()
    browser.get(url)
    time.sleep(5)
    try:
        div_element = browser.find_element(By.CLASS_NAME, "search-result-wrapper")
        pass
    except:
        return [], []
    # div_error_400 = browser.find_element(By.CLASS_NAME, "error-400")
    # if div_error_400.text == 'Sorry – your search could not be run.':
    #     return []

    div_element = browser.find_element(By.CLASS_NAME, "search-result-wrapper")
    all_papers_text = div_element.text

    strat_id = int(all_papers_text.split('\n')[0])
    all_papers_text = "\n" + all_papers_text
    for paper_id in range(strat_id, strat_id+100):
        if str(paper_id) + '\n' in all_papers_text:
            pass
        else:
            break
            print('break at id: {}'.format(paper_id))
        pattern = "\n" + str(paper_id) + "\n(.*?)\n" + str(paper_id + 1) + '\n'

        matched_blocks = re.findall(pattern, all_papers_text, re.DOTALL)
        #the last one
        if len(matched_blocks) == 0:
            paper_block = all_papers_text.split('\n{}\n'.format(paper_id))[-1]
        elif len(matched_blocks) == 1:
            paper_block = matched_blocks[0]
        else:
            raise ValueError('matched blocks more than 1!!!')
        paper_title = paper_block.strip().split('\n')[1]
        paper_publication_and_date = paper_block.split('\n')[2]
        titles.append(paper_title)
        if paper_title == 'View PDFAbstractFiguresExport':
            a = 1
        paper_publications.append(paper_publication_and_date)

    return titles, paper_publications


def get_all_papers_from_Science_Direct(keywords_group1, keywords_group2, saved_path):
    dict_keywords_to_papers = {'keyword': [], 'title': [], 'publication': []}
    url_template = "https://www.sciencedirect.com/search?title=#{keyword1}#%#{keyword2}#&show=100&offset=#{paperid}#"


    for keyword_g1 in tqdm.tqdm(keywords_group1):
        for keyword_g2 in keywords_group2:
            keywords = keyword_g1 + ' ' + keyword_g2
            url_with_keyword_1_2 = url_template.replace('#{keyword1}#', keyword_g1).replace('#{keyword2}#', keyword_g2)
            paperid=0
            # titles_with_keyword_g1_g2 = []

            while True:
                time.sleep(random.randint(2,5))
                url_with_page = url_with_keyword_1_2.replace('#{paperid}#', str(paperid))
                titles, paper_publications = Science_Direct_Paper_Crawling(url_with_page)
                # titles_with_keyword_g1_g2 += titles
                paperid += 100
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
                    a = 1


            # if keywords in dict_keywords_to_papers:
            #     raise ValueError('more than twice matched!!! Check the code!!!')
            # else:
            #     dict_keywords_to_papers[keywords] = titles_with_keyword_g1_g2
            # print('titles: {}'.format(titles_with_keyword_g1_g2))
            # Utils.save_list_to_pkl(titles_with_keyword_g1_g2, 'Science_Direct_Paper_Crawling/' + keywords + '.txt')
    df_keywords_to_papers_publications = pd.DataFrame(dict_keywords_to_papers)
    df_keywords_to_papers_publications.to_csv(saved_path, index=False)
    # Utils.dict_to_json(dict_keywords_to_papers, saved_json_path)


if __name__ == '__main__':


    keywords_group1 = ['android', 'mobile', 'phone', 'phones', 'smartphone', 'smartphones']
    keywords_group2 = ['performance', 'resource', 'energy', 'responsiveness', 'issue', 'issues']
    get_all_papers_from_Science_Direct(keywords_group1, keywords_group2, saved_path="data/Science_Direct_Paper_Crawling.csv")