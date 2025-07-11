import pandas as pd
from utils import Utils
keyword_list_1 = ['android', 'mobile', 'phone', 'smartphone',]
keyword_list_2 = ['performance', 'resource', 'response', 'energy', 'memory', 'launch', 'freeze',
                  'lag', 'battery', 'responsiveness', 'cpu', 'gpu', 'storage', 'latency', 'issue']


def all_papers_in_single_library(library_result_dir):
    all_csv_files = Utils.get_all_subfiles(library_result_dir)
    all_papers = pd.DataFrame()

    for csv_file in all_csv_files:
        df = pd.read_csv(csv_file)
        all_papers = pd.concat([all_papers, df], ignore_index=True)

    all_papers = all_papers.drop_duplicates(subset=['title'])

    # 判断 title 是否同时包含 keyword_list_1 中至少一个 和 keyword_list_2 中至少一个关键词
    def title_matches(row):
        title = row['title']
        if not isinstance(title, str):
            return False
        title_lower = title.lower()
        match_1 = any(kw in title_lower for kw in keyword_list_1)
        match_2 = any(kw in title_lower for kw in keyword_list_2)
        return match_1 and match_2

    mask = all_papers.apply(title_matches, axis=1)

    all_papers_in_single_library = all_papers[mask].reset_index(drop=True)
    removed_papers = all_papers[~mask].reset_index(drop=True)

    return all_papers_in_single_library

if __name__ == '__main__':
    ACM_library_result_dir = 'data/ACM_library'
    IEEE_library_result_dir = 'data/IEEE_library'
    ScienceDirect_library_result_dir = 'data/Science_Direct'
    Springer_library_result_dir = 'data/Springer'
    Wiley_library_result_dir = 'data/Wiley'

    all_ACM_papers = all_papers_in_single_library(ACM_library_result_dir)
    all_IEEE_papers = all_papers_in_single_library(IEEE_library_result_dir)
    all_ScienceDirect_papers = all_papers_in_single_library(ScienceDirect_library_result_dir)
    all_Springer_papers = all_papers_in_single_library(Springer_library_result_dir)
    all_Wiley_papers = all_papers_in_single_library(Wiley_library_result_dir)

    all_ACM_papers.to_csv('data/searched_papers_from_ACM_library.csv', index=False)
    all_IEEE_papers.to_csv('data/searched_papers_from_IEEE_library.csv', index=False)
    all_ScienceDirect_papers.to_csv('data/searched_papers_from_Science_Direct.csv', index=False)
    all_Springer_papers.to_csv('data/searched_papers_from_Springer.csv', index=False)
    all_Wiley_papers.to_csv('data/searched_papers_from_Wiley.csv', index=False)

    all_papers = pd.concat([all_ACM_papers, all_IEEE_papers, all_ScienceDirect_papers, all_Springer_papers, all_Wiley_papers], ignore_index=True)
    all_papers = all_papers.drop_duplicates(subset=['title'])
    all_papers.to_csv('data/merged_searched_papers.csv', index=False)


    df = pd.read_csv('data/searched_papers_filtered_by_venues.csv')

    # 把 all_papers 和 df 中的 title 全部转为小写，构建小写标题集合
    all_titles_lower = set(all_papers['title'].dropna().str.lower())


    # 判断每一行的 title（转小写后）是否在 all_titles_lower 中
    def title_in_all_papers(row):
        title = row['title']
        if not isinstance(title, str):
            return False
        return title.lower() in all_titles_lower


    mask = df.apply(title_in_all_papers, axis=1)

    searched_papers_in_all_papers = df[mask].reset_index(drop=True)
    searched_papers_not_in_all_papers = df[~mask].reset_index(drop=True)
    a =1
