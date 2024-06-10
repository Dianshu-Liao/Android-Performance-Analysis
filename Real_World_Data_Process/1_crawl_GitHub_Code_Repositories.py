import requests
from bs4 import BeautifulSoup
import csv
import tqdm
import os
import pandas as pd


def get_categories_link():
    response = requests.get("https://f-droid.org/en/packages/")
    response.raise_for_status()


    soup = BeautifulSoup(response.content, 'html.parser')
    a_tags = soup.select('div.post-content p a')
    links = [a.get('href') for a in a_tags]
    links = ['https://f-droid.org/' + link for link in links]

    return links


def get_list_by_categories(category):

    response = requests.get(category)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')


    category_name = soup.select_one('div.post-content > h3').text
    print(f'Category name: {category_name}')


    nav_next_li = soup.find('li', class_='nav next')

    previous_li = nav_next_li.find_previous_sibling('li')

    a_tag = previous_li.find('a')

    pages = int(a_tag.text) if a_tag else '0'
    # print(f'pages of {category} is {pages}')
    app_list = []

    for i in range(pages):
        link = f'{category}{i + 1 if i > 0 else ""}/index.html'
        # print(link)

        response_p = requests.get(link)
        content_p = response_p.text
        soup_p = BeautifulSoup(content_p, 'html.parser')


        package_list_div = soup_p.find('div', id='package-list')


        a_tags = package_list_div.find_all('a', recursive=False)
        # print(len(a_tags))


        app_list_p = [(f'https://f-droid.org/{a["href"]}', a.find('h4').text.strip()) for a in a_tags if a.find('h4')]
        # for package in packages:
        #     print(package)
        app_list.extend(app_list_p)

    return category_name, app_list


def get_git_link_by_app(app):
    app_link, app_name = app
    response = requests.get(app_link)
    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    source_code_link = soup.find('a', string='Source Code')['href']
    print(f'{app_name} git url: {source_code_link}')
    return (app_name, source_code_link, app_link)


def save_as_csv(FDdata_directory, category, app_list):

    csv_file = f'{FDdata_directory}/{category}.csv'
    # csv_file = f'./data/GitHub_Repo_Data/FDdata/{category}.csv'


    with open(csv_file, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        writer.writerow(['AppName', 'gitLink', 'FDstoreLink'])

        for app in app_list:
            writer.writerow(app)

    print(f'{category} saved to {csv_file}')


def get_FDdata(FDdata_directory):
    categories_link = get_categories_link()
    for category_link in categories_link:
        category, app_list = get_list_by_categories(category_link)
        all_git_links = []
        for app in tqdm.tqdm(app_list):
            try:
                git_links_by_app = get_git_link_by_app(app)
                all_git_links.append(git_links_by_app)
            except:
                pass
        save_as_csv(FDdata_directory, category, all_git_links)


def get_issues(owner, repo, token):
    issues_data = []
    url = f'https://api.github.com/repos/{owner}/{repo}/issues'
    headers = {'Authorization': f'token {token}', 'Accept': 'application/vnd.github.v3+json'}

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        issues = response.json()
        for issue in issues:
            # print('Title:', issue['title'])
            # print('Body:', issue['body'])
            # print('Labels:', [label['name'] for label in issue['labels']])
            # print('--------------------------------------------------------')
            issues_data.append({
                'HTML_URL': issue['html_url'],
                'Title': issue['title'],
                'Body': issue['body'],
                'Labels': [label['name'] for label in issue['labels']]
            })
    else:
        print('Failed to retrieve issues')

    return issues_data


def get_GitHub_issues(FDdata_directory, GitHub_issues_directory):
    # GitHub token
    token = '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'


    if not os.path.exists(FDdata_directory):
        print(f"Folder '{FDdata_directory}' does not exist.")
    else:
        issues = []

        for file_name in os.listdir(FDdata_directory):
            if file_name.endswith('.csv'):
                file_path = os.path.join(FDdata_directory, file_name)
                try:
                    df = pd.read_csv(file_path)

                    for git_link in df['gitLink'].dropna().unique():

                        parts = git_link.split('/')
                        if len(parts) > 4:
                            owner = parts[3]
                            repo = parts[4]
                            print(f"GitLink: {git_link}, Owner: {owner}, Repo: {repo}")
                            issue = get_issues(owner, repo, token)
                            issues.extend(issue)
                    issues_df = pd.DataFrame(issues)
                    output_csv_path = f'{GitHub_issues_directory}/{file_name}'
                    # output_csv_path = f'./FDissues/{file_name}'
                    print(f'Saving {file_name}...')
                    issues_df.to_csv(output_csv_path, index=False, encoding='utf-8')
                    print(f'Saved!')
                    issues = []
                except Exception as e:
                    print(f"Error reading file {file_name}: {e}")


if __name__ == "__main__":


    FDdata_directory = './data/GitHub_Repo_Data/FDdata'
    GitHub_issues_directory = './data/GitHub_Repo_Data/FDissues'

    # get_FDdata(FDdata_directory)
    get_GitHub_issues(FDdata_directory, GitHub_issues_directory)
