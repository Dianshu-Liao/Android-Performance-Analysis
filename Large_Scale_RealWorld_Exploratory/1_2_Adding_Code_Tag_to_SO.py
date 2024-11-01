import requests
from bs4 import BeautifulSoup
import csv
import time
import os
import pandas as pd


class Question:
    def __init__(self, title, tags, answered, link):
        # 初始化属性
        self.title = title
        self.tags = tags.split(',')
        self.answered = answered
        self.link = link
        self.with_code = False


def detect_answer_with_code(url):
    for _ in range(10):
        try:
            response = requests.get(url)
            response.raise_for_status()

            break
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print('Waiting due to HTTP 429 Too Many Requests')
                time.sleep(10)
            elif e.response.status_code == 404:
                print("404 Not Found")
                return False
            else:
                print(f'Something wrong with {e.response.status_code}!')
                return False


    soup = BeautifulSoup(response.content, 'html.parser')
    answer_div = soup.find('div', id='answers')

    # Check that answer_div is not None and contains a <code> tag.
    return answer_div is not None and bool(answer_div.find('code'))


def code_filter(path):
    questions = []
    save_interval = 2000

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            print(f'Processing row {i + 1}')
            question = Question(row['Title'], row['Tags'], row['Answered'] == 'True', row['Link'])
            question.with_code = detect_answer_with_code(f'https://stackoverflow.com{question.link}')
            questions.append(question)
            time.sleep(1)

            # Save every 2000 rows of data
            if i % save_interval == 0:
                with open(f'./data/SOdata/filtered_SO_data_{i // save_interval}.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Tags', 'Answered', 'Link', 'With code'])
                    for question in questions:
                        writer.writerow([question.title, ','.join(question.tags), question.answered, question.link, question.with_code])
                questions = []

    if questions:
        with open(f'./SOdata/filtered_SO_data_last.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Tags', 'Answered', 'Link', 'With code'])
            for question in questions:
                writer.writerow([question.title, ','.join(question.tags), question.answered, question.link, question.with_code])


def merge_file():
    # Define the directory containing the files
    directory = 'SOdata'

    # List all files in the directory
    all_files = os.listdir(directory)

    # Filter out files that start with 'filtered_SO_data_' and end with '.csv'
    filtered_files = [file for file in all_files if file.startswith('filtered_SO_data_') and file.endswith('.csv')]

    # Read and concatenate all filtered CSV files
    combined_csv = pd.concat([pd.read_csv(f'{directory}/{file}') for file in filtered_files])

    # Save the combined CSV to a new file
    output_file = f'{directory}/SO_data_with_code.csv'
    combined_csv.to_csv(output_file, index=False)

    # for f in filtered_files:
    #     os.remove(os.path.join(directory, f))


def main():
    path = 'SOdata/SO_data.csv'
    code_filter(path)
    merge_file()


if __name__ == "__main__":
    main()
