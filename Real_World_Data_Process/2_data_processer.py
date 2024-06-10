import pandas as pd
from utils import Utils
import tqdm
from transformers import BertTokenizer, BertForSequenceClassification
from torch.nn.functional import softmax
import torch

from transformers import pipeline



def find_keywords_in_text(text, keywords):
    matched = [keyword for keyword in keywords if keyword.lower() in text.lower()]
    return matched


def filter_GitHub_Repo_data(FD_issues_data_path, filtered_FD_issues_data_path, FD_commits_data_path, filtered_FD_commits_data_path):
    keywords = Utils.load_keywords()

    FD_issues = pd.read_csv(FD_issues_data_path)
    matched_keywords_list = []
    for index, row in tqdm.tqdm(FD_issues.iterrows(), total=len(FD_issues)):
        title_matches = find_keywords_in_text(row['Title'], keywords)
        if pd.isna(row['Body']):
            body_matches = []
        else:
            body_matches = find_keywords_in_text(row['Body'], keywords)
        matched_keywords = list(set(title_matches + body_matches))
        if matched_keywords:
            matched_keywords_list.append('\n'.join(matched_keywords))
        else:
            matched_keywords_list.append('')

    FD_issues['matched_keywords'] = matched_keywords_list
    filtered_FD_issues = FD_issues[FD_issues['matched_keywords'] != '']


    FD_commits = pd.read_csv(FD_commits_data_path)
    FD_commits = FD_commits.drop_duplicates()
    matched_keywords_list = []
    for index, row in tqdm.tqdm(FD_commits.iterrows(), total=len(FD_commits)):
        if pd.isna(row['commit_Title']):
            title_matches = []
        else:
            title_matches = find_keywords_in_text(row['commit_Title'], keywords)
        if pd.isna(row['commit_Description']):
            body_matches = []
        else:
            body_matches = find_keywords_in_text(row['commit_Description'], keywords)
        matched_keywords = list(set(title_matches + body_matches))
        if matched_keywords:
            matched_keywords_list.append('\n'.join(matched_keywords))
        else:
            matched_keywords_list.append('')

    FD_commits['matched_keywords'] = matched_keywords_list
    filtered_FD_commits = FD_commits[FD_commits['matched_keywords'] != '']

    filtered_FD_issues.to_csv(filtered_FD_issues_data_path, index=False)
    filtered_FD_commits.to_csv(filtered_FD_commits_data_path, index=False)
def filter_SO(SO_path, filterd_SO_path):
    keywords = Utils.load_keywords()

    SO_data = pd.read_csv(SO_path)
    SO_data = SO_data.drop_duplicates()
    filter_with_code_tag_yes = SO_data[SO_data['With code'] == True]



    matched_keywords_list = []
    for index, row in tqdm.tqdm(filter_with_code_tag_yes.iterrows(), total=len(filter_with_code_tag_yes)):

        title_matches = find_keywords_in_text(row['Title'], keywords)
        matched_keywords = list(set(title_matches))
        if matched_keywords:
            matched_keywords_list.append('\n'.join(matched_keywords))
        else:
            matched_keywords_list.append('')

    filter_with_code_tag_yes['matched_keywords'] = matched_keywords_list
    filter_questions = filter_with_code_tag_yes[filter_with_code_tag_yes['matched_keywords'] != '']


    filter_questions.to_csv(filterd_SO_path, index=False)

def filter_UserReview(UserReview_path, filtered_UserReview_path):
    keywords = Utils.load_keywords()

    UserReview = pd.read_csv(UserReview_path)
    UserReview = UserReview.drop(columns=['ReviewId'])
    UserReview = UserReview.drop_duplicates()


    matched_keywords_list = []
    for index, row in tqdm.tqdm(UserReview.iterrows(), total=len(UserReview)):

        content_matches = find_keywords_in_text(row['Content'], keywords)
        matched_keywords = list(set(content_matches))
        if matched_keywords:
            matched_keywords_list.append('\n'.join(matched_keywords))
        else:
            matched_keywords_list.append('')

    UserReview['matched_keywords'] = matched_keywords_list
    filter_UserReview = UserReview[UserReview['matched_keywords'] != '']


    filter_UserReview.to_csv(filtered_UserReview_path, index=False)


def process_GitHubRepoData():
    # 1. merge all csv files into one csv and remove duplicates
    # 2. filter
    folder_path = '../real_world_study/GitHub_Repo_Data/FDissues'
    FD_issues_data_path = '../real_world_study/GitHub_Repo_Data/FD_issues.csv'
    filtered_FD_issues_data_path = '../real_world_study/GitHub_Repo_Data/filtered_FD_issues.csv'
    # Utils.merge_all_csvs_under_a_folder(folder_path, FD_issues_data_path)
    FD_commits_data_path = '../real_world_study/GitHub_Repo_Data/merged_csv_commit.csv'
    filtered_FD_commits_data_path = '../real_world_study/GitHub_Repo_Data/filtered_FD_commits.csv'
    filter_GitHub_Repo_data(FD_issues_data_path, filtered_FD_issues_data_path, FD_commits_data_path, filtered_FD_commits_data_path)

def process_SOData():
    # 1. merge csv files into a single csv and remove duplicates
    # 2. use keywords to filter
    folder_path = '../real_world_study/SOdata/SOdataList'
    merged_SO_data_path = '../real_world_study/SOdata/SO_data.csv'
    filtered_SO_data_path = '../real_world_study/SOdata/filtered_SO_data.csv'
    # Utils.merge_all_csvs_under_a_folder(folder_path, merged_SO_data_path)

    filter_SO(merged_SO_data_path, filtered_SO_data_path)

def classify_review(review, sentiment_analysis):
    result = sentiment_analysis(review)[0]['label']
    if result == 'NEGATIVE':
        return False
    elif result == 'POSITIVE':
        return True
    else:
        raise ValueError('new result!!!')



def get_negative_user_reviews(UserReview_path, saved_negative_review_path):
    user_reviews = pd.read_csv(UserReview_path)
    sentiment_analysis = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")

    negative_reviews = []

    for index, row in tqdm.tqdm(user_reviews.iterrows(), total=user_reviews.shape[0]):
        review = row['Content']
        try:
            if not classify_review(review, sentiment_analysis):
                negative_reviews.append(row)
        except:
            pass
    negative_reviews_df = pd.DataFrame(negative_reviews, columns=user_reviews.columns)
    negative_reviews_df.to_csv(saved_negative_review_path, index=False)

def process_UserReviewData():
    UserReview_path = '../real_world_study/UserReviewData/UserReviews.csv'
    saved_negative_reviews_path = '../real_world_study/UserReviewData/saved_negative_reviews.csv'
    filtered_UserReview_path = '../real_world_study/UserReviewData/filtered_UserReviews.csv'
    # get_negative_user_reviews(UserReview_path, saved_negative_reviews_path)
    filter_UserReview(saved_negative_reviews_path, filtered_UserReview_path)


if __name__ == '__main__':
    process_GitHubRepoData()
    process_SOData()
    process_UserReviewData()