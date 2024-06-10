import requests
from bs4 import BeautifulSoup
import csv


class Question:
    def __init__(self, title, tags, answered, link):

        self.title = title
        self.tags = tags
        self.answered = answered
        self.link = link

def get_pages():
    url = "https://stackoverflow.com/questions/tagged/android?tab=newest&pagesize=50"
    response = requests.get(url)
    response.raise_for_status()

    soup = BeautifulSoup(response.content, 'html.parser')

    next_tag = soup.find('a', string=" Next")
    pages = 0

    if next_tag and next_tag.find_previous_sibling('a'):
        pages = next_tag.find_previous_sibling('a').get_text()
        print("pages in total: ", pages)
    else:
        print("page number not found!")

    return pages


def process_question(question):
    title = question.find('h3').find('a').get_text()
    link = question.find('h3').find('a').get('href')
    tags = [li.find('a').get_text() for li in question.find_all('li') if li.find('a')]
    answer_div = question.find('div', class_='s-post-summary--stats js-post-summary-stats')
    answered = bool(answer_div.find('div', title="one of the answers was accepted as the correct answer"))

    return Question(title, tags, answered, link)




def detect_questions(questions):
    detected_questions = []
    for question in questions:
        if question.answered:
            detected_questions.append(question)

    return detected_questions


def get_questions_list():
    questions_list = []
    pages = int(get_pages())
    for page in range(18200, pages):
        url = f"https://stackoverflow.com/questions/tagged/android?tab=newest&page={page}&pagesize=50"
        response = requests.get(url)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        questions_list_div = soup.find('div', id='questions')

        questions_divs = questions_list_div.find_all('div', recursive=False)
        processed_questions = [process_question(question) for question in questions_divs]
        print(f'processing...')
        detected_questions = detect_questions(processed_questions)
        print(f'detecting...')
        questions_list.extend(detected_questions)
        print(f'page {page + 1} / {pages} finished')
        if (page + 1) % 200 == 0:
            print(f'saving data {page - 199}-{page + 1}')
            save_as_csv(questions_list, f'./data/SOdata/SOdataList/SOdataList {page - 199}-{page + 1}.csv')
            questions_list = []
            print('save finished!')



def save_as_csv(questions, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:

        writer = csv.writer(file)

        writer.writerow(['Title', 'Tags', 'Answered', 'Link'])

        for question in questions:
            writer.writerow([question.title, ','.join(question.tags), question.answered, question.link])


def main():
    get_questions_list()



if __name__ == "__main__":
    main()
