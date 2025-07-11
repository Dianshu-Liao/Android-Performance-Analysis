import requests
import time
import csv
import os
import pandas as pd

class Question:
    def __init__(self, title, tags, link, body):
        self.title = title
        self.tags = tags
        self.link = link
        self.with_code = "<code>" in body.lower()  # 判断是否包含代码


API_KEY = "rl_ptJCV2jXviMxP6u7ywjBh4k6i"  # 替换为你的 Stack Exchange API key


def get_questions_from_api(page):
    url = "https://api.stackexchange.com/2.3/questions"
    params = {
        "order": "desc",
        "sort": "creation",
        "tagged": "android",
        "site": "stackoverflow",
        "pagesize": 100,
        "page": page,
        "key": API_KEY,
        "filter": "withbody"  # 关键参数：获取正文 body
    }

    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.json()


def process_questions(data):
    questions = []
    for item in data.get("items", []):
        body = item.get("body", "")
        question = Question(
            title=item["title"],
            tags=item["tags"],
            link=item["link"],
            body=body
        )
        questions.append(question)
    return questions


def save_as_csv(questions, filename):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(['Title', 'Tags', 'Link', 'With Code'])
        for q in questions:
            writer.writerow([q.title, ','.join(q.tags), q.link, q.with_code])


def get_questions_list():
    page = 1
    batch = 200
    questions_list = []

    while True:
        print(f"Fetching page {page}")
        try:
            data = get_questions_from_api(page)
        except requests.exceptions.HTTPError as e:
            print("HTTP Error:", e)
            break

        questions = process_questions(data)
        questions_list.extend(questions)

        if page % batch == 0:
            filename = f'data/SOdata/SOdataList/SOdataList_{page - batch + 1}-{page}.csv'
            save_as_csv(questions_list, filename)
            print(f"Saved batch {page - batch + 1}-{page}")
            questions_list = []

        if not data.get("has_more", False):
            break

        page += 1
        # time.sleep(1)  # 建议保留，避免触发速率限制

    if questions_list:
        filename = f'data/SOdata/SOdataList/SOdataList_{page - (page % batch)}-{page}.csv'
        save_as_csv(questions_list, filename)
        print("Saved final batch")


def merge_file():
    # Define the directory containing the files
    directory = 'data/SOdata/SOdataList'

    # List all files in the directory
    all_files = os.listdir(directory)

    # Filter out files that start with 'filtered_SO_data_' and end with '.csv'
    filtered_files = [file for file in all_files if file.startswith('SOdataList_') and file.endswith('.csv')]

    # Read and concatenate all filtered CSV files
    combined_csv = pd.concat([pd.read_csv(f'{directory}/{file}') for file in filtered_files])

    # Save the combined CSV to a new file
    output_file = f'data/SOdata/SO_data_raw.csv'
    combined_csv.to_csv(output_file, index=False)


def main():
    # get_questions_list()
    merge_file()

if __name__ == "__main__":
    main()
