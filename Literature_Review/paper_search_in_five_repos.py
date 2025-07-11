import pandas as pd

from utils import Utils
from Paper_search_ACM import get_all_papers_from_ACM_library
from paper_search_IEEE import get_all_papers_from_IEEE_library
from paper_search_science_direct import get_all_papers_from_Science_Direct
from paper_search_springer import get_all_papers_from_springer
from paper_search_wiley import get_all_papers_from_Wiley

def merge_all_papers(ACM_paper_saved_dir, IEEE_paper_saved_dir, Science_Direct_paper_saved_dir,
                     Springer_paper_saved_dir, Wiley_paper_saved_dir, search_paper_saved_path):
    all_ACM_papers = Utils.get_all_subfiles(ACM_paper_saved_dir)
    all_IEEE_papers = Utils.get_all_subfiles(IEEE_paper_saved_dir)
    all_Science_Direct_papers = Utils.get_all_subfiles(Science_Direct_paper_saved_dir)
    all_Springer_papers = Utils.get_all_subfiles(Springer_paper_saved_dir)
    all_Wiley_papers = Utils.get_all_subfiles(Wiley_paper_saved_dir)

    # merge all papers
    all_paper_csvs = all_ACM_papers + all_IEEE_papers + all_Science_Direct_papers + all_Springer_papers + all_Wiley_papers

    # 所有csv读成一个df，最终合并起来
    all_papers = pd.DataFrame()
    for paper_csv in all_paper_csvs:
        df = pd.read_csv(paper_csv)
        all_papers = pd.concat([all_papers, df], ignore_index=True)

    # # remove rows that the 'title' column is the same. 不区分大小写
    # all_papers = all_papers.drop_duplicates(subset=['title'], keep='first', ignore_index=True)

    # Convert the "title" column to lowercase to ignore case
    all_papers['title_lower'] = all_papers['title'].str.lower()

    # Drop duplicates based on the lowercase version of the "title" column
    all_papers = all_papers.drop_duplicates(subset='title_lower')

    # Drop the helper "title_lower" column
    all_papers = all_papers.drop(columns=['title_lower'])



    should_remove = []

    for index, row in all_papers.iterrows():
        title = row['title'].lower()  # 将title转换为小写

        keywords_group1 = [keyword.lower() for keyword in Utils.load_keywords('android_keywords.txt')]  # 将关键词转换为小写
        keywords_group2 = [keyword.lower() for keyword in Utils.load_keywords('pi_related_keywords.txt')]  # 将关键词转换为小写

        # 检查title中是否包含keywords_group1中的至少一个关键词（不区分大小写）
        contains_keyword1 = any(keyword in title for keyword in keywords_group1)

        # 检查title中是否包含keywords_group2中的至少一个关键词（不区分大小写）
        contains_keyword2 = any(keyword in title for keyword in keywords_group2)

        # 如果title中同时包含keywords_group1和keywords_group2中的关键词，则保留，否则记录行号
        if not (contains_keyword1 and contains_keyword2):
            should_remove.append(index)


    all_papers = all_papers.drop(should_remove, axis=0)
    all_papers.to_csv(search_paper_saved_path, index=False)


def filter_papers_based_on_venues(search_paper_saved_path, search_paper_filtered_by_venues_path):
    searched_papers = pd.read_csv(search_paper_saved_path)

    # 删除 publication 是 NaN 的行
    searched_papers = searched_papers.dropna(subset=['publication'])

    venues = Utils.load_keywords('venue_list.txt')
    venues = [venue.lower() for venue in venues]  # 将关键词转换为小写

    matched_venues = []  # 用于存储匹配到的venue
    should_remove = []

    for index, row in searched_papers.iterrows():
        publication = row['publication'].lower()

        # 查找所有匹配的 venues
        matched_venue = [venue for venue in venues if venue in publication]

        if matched_venue:
            # 将匹配到的 venues 用逗号隔开并存储到 matched_venues 列表中
            matched_venues.append('\n'.join(matched_venue))
        else:
            should_remove.append(index)  # 如果没有匹配到，则记录要删除的行号

    # 删除没有匹配到 venue 的行
    searched_papers = searched_papers.drop(should_remove, axis=0)

    # 将匹配到的 venue 列添加到 searched_papers 中
    searched_papers['matched_venue'] = matched_venues
    searched_papers['remain'] = ''
    # 保存结果
    searched_papers.to_csv(search_paper_filtered_by_venues_path, index=False)


if __name__ == '__main__':

    ACM_paper_saved_dir = 'data/ACM_Library'
    IEEE_paper_saved_dir = 'data/IEEE_Library'
    Science_Direct_paper_saved_dir = 'data/Science_Direct'
    Springer_paper_saved_dir = 'data/Springer'
    Wiley_paper_saved_dir = 'data/Wiley'

    search_paper_saved_path = 'data/searched_papers_from_five_repos.csv'
    search_paper_filtered_by_venues_path = 'data/searched_papers_filtered_by_venues.csv'

    keywords_group1 = Utils.load_keywords('android_keywords.txt')
    keywords_group2 = Utils.load_keywords('pi_related_keywords.txt')

    # get_all_papers_from_ACM_library(keywords_group1, keywords_group2, ACM_paper_saved_dir)
    # get_all_papers_from_IEEE_library(keywords_group1, keywords_group2, IEEE_paper_saved_dir)
    # get_all_papers_from_Science_Direct(keywords_group1, keywords_group2, Science_Direct_paper_saved_dir)
    # get_all_papers_from_springer(keywords_group1, keywords_group2, Springer_paper_saved_dir)
    # get_all_papers_from_Wiley(keywords_group1, keywords_group2, Wiley_paper_saved_dir)

    merge_all_papers(ACM_paper_saved_dir, IEEE_paper_saved_dir, Science_Direct_paper_saved_dir,
                     Springer_paper_saved_dir, Wiley_paper_saved_dir, search_paper_saved_path)

    filter_papers_based_on_venues(search_paper_saved_path, search_paper_filtered_by_venues_path)