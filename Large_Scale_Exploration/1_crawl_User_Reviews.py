import time

import requests
import tqdm
from bs4 import BeautifulSoup
from bs4 import Tag
import os
import pandas as pd
from google_play_scraper import Sort, reviews_all
from datetime import datetime

import csv
import numpy as np





def fetch_app_list(app_link):
    try:
        request_link = app_link
        # AppBrain
        response = requests.get(app_link)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # find ranking_table
        ranking_table = soup.find('table', id='rankings-table')

        # check if ranking_table is finded
        if not ranking_table:
            return "Specified div not found."


        link_text_list = []
        num = 0

        for index, tr in enumerate(ranking_table.find('tbody').children):
            if index == 0 or not isinstance(tr, Tag):
                continue
            num += 1
            app_cell = tr.find('td', class_='ranking-app-cell')
            if not app_cell:
                print('Not found!')
                break

            app_link = app_cell.find_all('a')[0]['href']
            app_id = app_link.split("/")[-1]
            app_name = app_cell.find_all('a')[0].text.strip()

            #  Get developer links and text
            developer_link = app_cell.find_all('a')[1]['href']
            developer_name = app_cell.find_all('a')[1].text.strip()

            # Get category links and text
            category_cell = tr.find('td', class_='ranking-app-cell').find_next_sibling('td')
            if not category_cell:
                print("no category!")
                break
            category_link = category_cell.find('a')['href']
            category_name = category_cell.find('a').text.strip()

            link_text_list.append(
                [app_id, app_name, developer_link, developer_name, category_link, category_name, request_link])



        return link_text_list
    except requests.RequestException as e:
        print(f"Error fetching page: {e}")
        print('link: {}'.format(app_link))
        return []



def fetch_app_reviews(app_id):
    result = reviews_all(
        app_id,
        sleep_milliseconds=0,  # defaults to 0
        lang='en',  # defaults to 'en'
        country='us',  # defaults to 'us'
        sort=Sort.MOST_RELEVANT,  # defaults to Sort.MOST_RELEVANT
        filter_score_with=5  # defaults to None(means all score)
    )

    reformate_reviews = []
    for review in result:
        reformate_review = {
            'content': review['content'],
            'reviewCreatedVersion': review['reviewCreatedVersion'],
            'at': review['at'].strftime("%Y%m%d"),
            'appVersion': review.get('appVersion', None)
        }

        reformate_reviews.append(reformate_review)

    return reformate_reviews






def get_app_link_list():

    countries = ['au', 'at', 'be', 'br', 'ca', 'cz', 'dk', 'fi', 'fr', 'de', 'in', 'id', 'ir', 'it', 'jp',
                 'mx', 'nl', 'no', 'pl', 'pt', 'ru', 'sa', 'sk', 'kr', 'es', 'se', 'ch', 'tr', 'gb', 'us']
    a = 1
    rank_types = ['top_free', 'top_paid', 'top_grossing', 'top_new_free', 'top_new_paid']

    app_link_list = []
    for country in countries:
        for rank_type in rank_types:
            app_link1 = 'https://www.appbrain.com/stats/google-play-rankings/{}/all/{}/1'.format(rank_type, country)
            app_link2 = 'https://www.appbrain.com/stats/google-play-rankings/{}/all/{}/2'.format(rank_type, country)
            app_link_list.append(app_link1)
            app_link_list.append(app_link2)
    return app_link_list


def all_needed_apps(app_link_list, saved_path):
    if os.path.exists(saved_path):

        all_apps = list(np.load(saved_path))
    else:
        all_apps = []

    all_app_link = []
    for app in all_apps:
        link = app[-1]
        all_app_link.append(link)
    all_app_link = list(set(all_app_link))


    for app_link in tqdm.tqdm(app_link_list):
        if app_link in all_app_link:
            continue
        time.sleep(2)
        apps = fetch_app_list(app_link)
        all_apps += apps
    np.save(saved_path, all_apps)

def main():
    app_link_list = get_app_link_list()
    all_needed_apps(app_link_list, saved_path='saved_app_list.npy')

    all_apps = list(np.load('saved_app_list.npy'))
    unique_app_ids = []
    app_list = []
    for app in all_apps:
        app = list(app)
        app_id = app[0]
        if app_id in unique_app_ids:
            pass
        else:
            unique_app_ids.append(app_id)
            app_list.append(app)

    # set the file path
    AppRankList_path = './data/UserReviewData/AppRankList.csv'
    UserReviews_path = './data/UserReviewData/UserReviews.csv'
    Reviews_path = './data/UserReviewData/Reviews.csv'
    current_rank_path = './data/UserReviewData/current_rank.txt'
    # get application list


    # if the file existed, do not rewrite it
    # please delete all files, if you want to rewrite them
    if not os.path.exists(AppRankList_path):
        # Save AppRankList, set head
        with (open(AppRankList_path, 'w', newline='', encoding='utf-8') as file):
            writer = csv.writer(file)
            writer.writerow(['rank', 'AppId', 'AppName', 'Developer', 'Category'])
            for rank, app in enumerate(app_list, start=1):
                app_id = app[0]
                app_name = app[1]
                developer_name = app[3]
                category_name = app[5]
                writer.writerow([rank, app_id, app_name, developer_name, category_name])
    if not os.path.exists(current_rank_path):
        with open(current_rank_path, 'w', newline='', encoding='utf-8') as file:
            file.write('0')
    if not os.path.exists(UserReviews_path):
        with open(UserReviews_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['ReviewId', 'AppId', 'Content', 'ReviewCreatedVersion', 'ReviewTime'])
    if not os.path.exists(Reviews_path):
        with open(Reviews_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(
                ['ReviewId', 'AppId', 'AppName', 'Developer', 'Category', 'Content', 'ReviewCreatedVersion',
                 'ReviewTime'])

    with open(current_rank_path, 'r') as cur_rank_txt:
        content = cur_rank_txt.read()
        current_rank = eval(content)
    # For every Application
    for i in range(current_rank, len(app_list)):
        print(f'rank: {i + 1}\n'
              f'App Id: {app_list[i][0]}\n'
              f'Application Name: {app_list[i][1]}\n'
              f'Developer Info: {app_list[i][3]}\n'
              f'Category: {app_list[i][5]}')
        # update current rank
        with open(current_rank_path, 'w', newline='', encoding='utf-8') as file:
            file.write(str(i))
        reviews_all = fetch_app_reviews(app_list[i][0])
        # filtered_reviews = reviews_filter(reviews_all)

        if len(reviews_all) > 0:
            print(f'Number of filtered reviews: {len(reviews_all)}\n')
            # Save UserReviews
            with open('./data/UserReviewData/UserReviews.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for review_id, review in enumerate(reviews_all, start=1):
                    content = review['content']
                    review_created_version = review['reviewCreatedVersion']
                    review_time = review['at']
                    app_id = app_list[i][0]
                    writer.writerow([review_id, app_id, content, review_created_version, review_time])
            # Save Reviews
            with open('./data/UserReviewData/Reviews.csv', 'a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                for review_id, review in enumerate(reviews_all, start=1):
                    content = review['content']
                    review_created_version = review['reviewCreatedVersion']
                    review_time = review['at']
                    app_id = app_list[i][0]

                    app_info = next((app for app in app_list if app[0][0] == app_id), None)
                    if app_info:
                        app_name = app_info[1]
                        developer_name = app_info[3]
                        category_name = app_info[5]
                        writer.writerow([review_id, app_id, app_name, developer_name, category_name, content,
                                         review_created_version, review_time])
        else:
            print("No related review!")
    with open(current_rank_path, 'w', newline='', encoding='utf-8') as file:
        file.write('0')

if __name__ == "__main__":

    main()
