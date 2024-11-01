

# Android-Performance-Analysis

This artifact package includes all the data and code in the paper **''Give a Tinker’s Cuss: A Comparative Study of Android Performance Issues in Real-world Applications and Literature''**.
Due to GitHub's limited capacity, we have uploaded all our source code and data to Google Cloud Drive. You can access this link to our source code and data: [https://drive.google.com/file/d/1l5cFb1ma3KgXWaGypPuJOHHP8xcokTP0/view?usp=sharing](https://drive.google.com/file/d/1l5cFb1ma3KgXWaGypPuJOHHP8xcokTP0/view?usp=sharing)


## Data during the data collection process.

- **User Reviews**:
  - **`Large_Scale_RealWorld_Exploratory/UserReviewData/AppRankList.csv`**: Contains data on 7,681 apps.
  - **`Large_Scale_RealWorld_Exploratory/UserReviewData/UserReviews.csv`**: Contains 909,430 user reviews we collected.
  - **`Large_Scale_RealWorld_Exploratory/UserReviewData/saved_negative_reviews.csv`**: Contains 60,684 negative reviews identified through sentiment analysis.
  - **`Large_Scale_RealWorld_Exploratory/UserReviewData/filtered_UserReviews.csv`**: Contains 165 user reviews filtered by keywords.

- **Stack Overflow Discussions**:
  - **`Large_Scale_RealWorld_Exploratory/SOData/SO_data.csv`**: Contains 448,977 Stack Overflow discussions.
  - **`Large_Scale_RealWorld_Exploratory/SOData/SO_data_with_code.csv`**: Contains 360,372 Stack Overflow discussions containing the `code` tag.
  - **`Large_Scale_RealWorld_Exploratory/SOData/filtered_SO_Data.csv`**: Contains 893 discussions filtered by keywords.

- **GitHub Issues**:
  - **`Large_Scale_RealWorld_Exploratory/GitHubRepoData/GitHub_issues.csv`**: Contains 35,278 GitHub issues.
  - **`Large_Scale_RealWorld_Exploratory/GitHubRepoData/filtered_GitHub_issues.csv`**: Contains 317 issues filtered by keywords.

- **GitHub Commits**:
  - **`Large_Scale_RealWorld_Exploratory/GitHubRepoData/GitHub_commit.csv`**: Contains 550,973 GitHub commits.
  - **`Large_Scale_RealWorld_Exploratory/GitHubRepoData/filtered_GitHub_commits.csv`**: Contains 780 commits filtered by keywords.



## Concluding Data in Our Paper

1. **`Literature_Review/data/Performance_Analysis_literature_review.xlsx`**: Contains detailed information on the 66 papers reviewed in our literature analysis, including Year, Cites, Pages, URL, Venue Type, Performance Issue, Factor, Approach Type, dataset link, and more.

2. **`Large_Scale_RealWorld_Exploratory/Keywords.txt`**: A list of 87 keywords related to performance issues that we gathered from 100 websites and several foundation papers, supporting for our filtering step in the Large-Scale Exploration of Real-World Discussions on Android Performance Issues. 

3. **Real-World Data**:
   - **`Large_Scale_RealWorld_Exploratory/Manually_Checked_Data/filtered_UserReviews.csv`**
   - **`Large_Scale_RealWorld_Exploratory/Manually_Checked_Data/filtered_SO_data.csv`**
   - **`Large_Scale_RealWorld_Exploratory/Manually_Checked_Data/filtered_GitHub_issues.csv`**
   - **`Large_Scale_RealWorld_Exploratory/Manually_Checked_Data/filtered_GitHub_commits.csv`**

   These files contain data collected and manually checked from user reviews, Stack Overflow, GitHub issues, and GitHub commits, as described in Section 2 "A LARGE-SCALE EXPLORATION OF REAL-WORLD APPS". They include performance issues identified in the real world, corresponding factors, root causes, and potential solutions.

4. **`Large_Scale_RealWorld_Exploratory/common_patterns.txt`**: Lists the common performance issue code patterns identified from our real-world exploration.

## Source Code

1. **Crawling Data**:
   - **Run** **`Large_Scale_RealWorld_Exploratory/1_crawl_GitHub_Code_Repositories.py`**, **`Large_Scale_RealWorld_Exploratory/1_crawl_GitHub_Commits.py`**, **`Large_Scale_RealWorld_Exploratory/1_crawl_User_Reviews.py`**, **`Large_Scale_RealWorld_Exploratory/1_1_crawl_StackOverflow.py`**, **`Large_Scale_RealWorld_Exploratory/1_2_Adding_Code_Tag_to_SO.py`** to crawl GitHub issues and commits, user reviews, and Stack Overflow discussions.
   - **Run** **`Literature_Review/paper_search_in_five_repos.py`** to crawl and filter papers in five libraries.
   
2. **Filtering Data**:
   **- Run **`Large_Scale_RealWorld_Exploratory/2_data_processor.py`** to filter out user reviews, GitHub issues, commits, and Stack Overflow discussions related to performance issues based on keywords.**

3. **Statistic Data**:
   **- **Run** **`Literature_Review/statistic_literature.py`** and **`Large_Scale_RealWorld_Exploratory/statistic_real_world.py`** to gather all the data involved in the paper and their statistics.
