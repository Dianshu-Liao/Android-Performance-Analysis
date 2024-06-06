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
        self.tags = tags.split(',')  # 假设tags是以逗号分隔的字符串
        self.answered = answered
        self.link = link
        self.with_code = False


def detect_answer_with_code(url):
    for _ in range(10):  # 尝试最多十次
        try:
            response = requests.get(url)
            response.raise_for_status()  # 如果请求有问题则抛出异常
            # 如果没有错误，退出循环
            break
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 429:
                print('Waiting due to HTTP 429 Too Many Requests')
                time.sleep(10)  # 等待10秒
            elif e.response.status_code == 404:
                print("404 Not Found")
                return False  # 如果页面不存在，直接返回False
            else:
                print(f'Something wrong with {e.response.status_code}!')
                return False # 如果出现其他异常，直接返回False

    # 使用BeautifulSoup解析HTML内容
    soup = BeautifulSoup(response.content, 'html.parser')
    # 查找id为'answer'的div元素
    answer_div = soup.find('div', id='answers')

    # 检查answer_div是否不是None并且是否含有<code>标签
    return answer_div is not None and bool(answer_div.find('code'))


def code_filter(path):
    questions = []
    save_interval = 2000  # 设置保存间隔

    with open(path, newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for i, row in enumerate(reader, start=1):
            print(f'Processing row {i + 1}')
            # 创建Question实例并添加到列表中
            question = Question(row['Title'], row['Tags'], row['Answered'] == 'True', row['Link'])
            question.with_code = detect_answer_with_code(f'https://stackoverflow.com{question.link}')
            questions.append(question)
            time.sleep(1)  # 等待1秒

            # 每2000行数据保存一次
            if i % save_interval == 0:
                with open(f'./data/SOdata/filtered_SO_data_{i // save_interval}.csv', 'w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)
                    writer.writerow(['Title', 'Tags', 'Answered', 'Link', 'With code'])
                    for question in questions:
                        writer.writerow([question.title, ','.join(question.tags), question.answered, question.link, question.with_code])
                questions = []  # 清空列表以便重新开始

    # 处理完所有数据后，保存最后一批（如果有）
    if questions:
        with open(f'./data/SOdata/filtered_SO_data_last.csv', 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Title', 'Tags', 'Answered', 'Link', 'With code'])
            for question in questions:
                writer.writerow([question.title, ','.join(question.tags), question.answered, question.link, question.with_code])


def merge_file():
    # Define the directory containing the files
    directory = './data/SOdata'

    # List all files in the directory
    all_files = os.listdir(directory)

    # Filter out files that start with 'filtered_SO_data_' and end with '.csv'
    filtered_files = [file for file in all_files if file.startswith('filtered_SO_data_') and file.endswith('.csv')]

    # Read and concatenate all filtered CSV files
    combined_csv = pd.concat([pd.read_csv(f'{directory}/{file}') for file in filtered_files])

    # Save the combined CSV to a new file
    output_file = f'{directory}/filtered_SO_data_with_code.csv'
    combined_csv.to_csv(output_file, index=False)

    # for f in filtered_files:
    #     os.remove(os.path.join(directory, f))


def main():
    path = './data/SOdata/filtered_SO_data.csv'
    code_filter(path)
    merge_file()


if __name__ == "__main__":
    main()
