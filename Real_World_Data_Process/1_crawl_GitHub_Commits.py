import requests
from bs4 import BeautifulSoup
import csv
import os
import pandas as pd
import time
import tqdm
import pickle

# 获取所有app的commits/main/的链接
def get_app_commits_main_url(path = './data/GitHub_Repo_Data/FDdata'):
    # 获取路径下所有CSV文件
    csv_files = [f for f in os.listdir(path) if f.endswith('.csv')]
    commits_links_list = []
    # 遍历所有CSV文件
    for file in csv_files:
        # 完整的文件路径
        full_path = os.path.join(path, file)
        # 读取CSV文件
        df = pd.read_csv(full_path)
        # 检查是否有 'gitlink' 列
        if 'gitLink' in df.columns:
            df['gitLink'].apply(lambda x: commits_links_list.append(x + '/commits/main/'))
        else:
            print(f"文件：{file} 中没有 'gitLink' 属性")

    return list(set(commits_links_list))


def get_commits(commits_links_list):
    commit_data = []
    commit_file_id = 0
    unsuccessful_url_links_list = []
    unsuccessful_commit_links_list = []
    # 获取每一个app的commit list
    for commits_link in tqdm.tqdm(commits_links_list):
        has_next = True
        next_url = commits_link
        print('url:{}, commit_file_id: {}'.format(next_url, commit_file_id))
        # page_num = 0
        while has_next:  # 如果有下一页，则翻页继续爬取
            # if page_num >= 10:
            #     break
            # page_num += 1
            # print(f'commits_link: {next_url}\n')


            # 去除非github链接
            if not next_url.startswith("https://github.com/"):
                break
            response = None
            for attempt in range(2):
                response = requests.get(next_url)
                try:
                    response.raise_for_status()
                    break
                except requests.exceptions.HTTPError as e:
                    print(f"尝试 {attempt + 1}/3 失败: {e}")
                    if attempt < 1:
                        print(f"等待2秒后重试...")
                        time.sleep(2)  # 等待指定的秒数后再次尝试
                    else:
                        has_next = False
                        print("重试次数用尽，停止尝试。")
                        unsuccessful_url_links_list.append(next_url)
            if (has_next == False):
                break
            # 使用BeautifulSoup解析HTML内容
            soup = BeautifulSoup(response.content, 'html.parser')
            a_next = soup.find('a', attrs={'data-testid': 'pagination-next-button'})
            if a_next != None:
                if 'disabled' in a_next.get('style', 'disabled'):
                    has_next = False
                else:
                    next_url = f'https://github.com/' + a_next.get('href')
            else:
                break

            divs = soup.find_all('div', attrs={'data-testid': 'listview-item-title-container'})
            for div in divs:
                # 获取div中的所有a标签
                a_tags = div.find_all('a')
                commit_title = ''
                commit_link = ''
                issue_id = ''
                issue_link = ''
                # 检查a标签的数量并相应处理
                if len(a_tags) == 1:
                    commit_title = a_tags[0].text
                    commit_link = 'https://github.com' + a_tags[0]['href']
                    # print(f"Commit Title: {commit_title}\nCommit Link: {commit_link}\n")
                elif len(a_tags) >= 3:
                    commit_title = a_tags[0].text
                    commit_link = 'https://github.com' + a_tags[0]['href']
                    issue_id = a_tags[-2].text
                    issue_link = a_tags[-2]['href']
                    # print(f"Commit Title: {commit_title}\nCommit Link: {commit_link}\n"
                    #       f"Issue ID: {issue_id}\nIssue Link: {issue_link}\n")
                else:
                    print('wrong number of a tags')
                    continue


                commit_response = None

                try:
                    commit_response = requests.get(commit_link)
                except requests.exceptions.HTTPError as e:
                    print(f"尝试失败: {e}")
                    unsuccessful_commit_links_list.append(commit_link)


                # for attempt in range(3):
                #     commit_response = requests.get(commit_link)
                #     try:
                #         commit_response.raise_for_status()
                #         # 如果请求成功，跳出循环
                #         break
                #     except requests.exceptions.HTTPError as e:
                #         print(f"尝试 {attempt + 1}/3 失败: {e}")
                #         if attempt < 2:
                #             print(f"等待2秒后重试...")
                #             time.sleep(2)  # 等待指定的秒数后再次尝试
                #         else:
                #             print("重试次数用尽，停止尝试。")

                commit_soup = BeautifulSoup(commit_response.content, 'html.parser')
                # 获取class = commit-desc的div中的pre标签的文本内容
                commit_desc_div = commit_soup.find('div', class_='commit-desc')
                commit_desc = ''
                if (commit_desc_div != None):
                    commit_desc = commit_desc_div.find('pre').get_text(strip=True)
                commit_data.append({
                    'commit_Link': commit_link,
                    'commit_Title': commit_title,
                    'commit_Description': commit_desc,
                    'issue_Id': issue_id,
                    'issue_link': issue_link
                })
        save_as_csv(commit_data, commit_file_id)
        commit_file_id += 1
    return commit_data, unsuccessful_url_links_list, unsuccessful_commit_links_list


def save_as_csv(commit_data, file_name):
    path = './data/GitHub_Repo_Data/FDCommit/'
    df = pd.DataFrame(commit_data)
    # print("saving...")
    df.to_csv(path + f'FD_commit_{file_name}.csv', index=False)

def save_unsuccessful_lists(unsuccessful_url_links_list, unsuccessful_commit_links_list):
    with open('./data/GitHub_Repo_Data/FDCommit/unsuccessful_url_links_list.pkl', 'wb') as f:
        pickle.dump(unsuccessful_url_links_list, f)

    with open('./data/GitHub_Repo_Data/FDCommit/unsuccessful_commit_links_list.pkl', 'wb') as f:
        pickle.dump(unsuccessful_commit_links_list, f)

if __name__ == "__main__":
    commits_links_list = get_app_commits_main_url()
    commit_data, unsuccessful_url_links_list, unsuccessful_commit_links_list = get_commits(commits_links_list)
    save_as_csv(commit_data, 'all')

