

# Android-Performance-Analysis

This artifact package includes all the data and code in the paper **''Give a Tinker’s Cuss: A Comparative Study of Android Performance Issues in Real-world Applications and Literature''**.
Due to GitHub's limited capacity, we have uploaded all our source code and data to Google Cloud Drive. You can access this link to our source code and data: [https://drive.google.com/file/d/1Fo0_aQPIpAfS6C_Ra19lPulH00m6HhlH/view?usp=drive_link](https://drive.google.com/file/d/1Fo0_aQPIpAfS6C_Ra19lPulH00m6HhlH/view?usp=drive_link)


## Data during the data collection process.

- **User Reviews**:
  - **`Large_Scale_Exploration/data/UserReviewData/AppRankList.csv`**: Contains data on 7,681 apps.
  - **`Large_Scale_Exploration/data/UserReviewData/UserReviews.csv`**: Contains 909,430 user reviews we collected.
  - **`Large_Scale_Exploration/data/UserReviewData/saved_negative_reviews.csv`**: Contains 60,684 negative reviews identified through sentiment analysis.
  - **`Large_Scale_Exploration/data/UserReviewData/filtered_UserReviews.csv`**: Contains 165 user reviews filtered by keywords.

- **Stack Overflow Discussions**:
  - **`Large_Scale_Exploration/data/SOdata/SO_data_raw.csv`**: Contains 960,758 Stack Overflow discussions.
  - **`Large_Scale_Exploration/data/SOdata/SO_data_with_code.csv`**: Contains 749,067 Stack Overflow discussions containing the `code` tag.
  - **`Large_Scale_RealWorld_Exploratory/SOData/filtered_SO_Data.csv`**: Contains 2,158 discussions filtered by keywords.

- **GitHub Issues**:
  - **`data/GitHub_Repo_Data/FD_issues_with_google_play_link.csv`**: Contains 16,977 GitHub issues.
  - **`Large_Scale_Exploration/data/GitHub_Repo_Data/filtered_FD_issues.csv`**: Contains 149 issues filtered by keywords.

- **GitHub Commits**:
  - **`Large_Scale_Exploration/data/GitHub_Repo_Data/FD_commits_with_google_play_link.csv`**: Contains 344,922 GitHub commits.
  - **`Large_Scale_Exploration/data/GitHub_Repo_Data/filtered_FD_commits.csv`**: Contains 558 commits filtered by keywords.

- **Literature Review**:
  - **`Literature_Review/data/searched_papers_from_ACM_library.csv`**, **`Literature_Review/data/searched_papers_from_IEEE_library.csv`**, **`Literature_Review/data/searched_papers_from_Science_Direct.csv`**, **`Literature_Review/data/searched_papers_from_Springer.csv`**, **`Literature_Review/data/searched_papers_from_Wiley.csv`**:  These files contain the papers we searched in five libraries, including ACM, IEEE, Science Direct, Springer, and Wiley.
  - **`Literature_Review/data/merged_searched_papers.csv`**: Merges the above five files into one, containing 15,574 papers.
  - **`Literature_Review/data/searched_papers_filtered_by_venues.csv`**: Contains 441 papers filtered by venue types, including journals, conferences, and workshops.
  - **`Literature_Review/data/papers_after_exclusion.txt`**: Contains 60 papers after manual exclusion based on the criteria.
  - **`Literature_Review/data/snowball_papers.txt`**: Contains 25 papers obtained through snowballing from the 60 papers.



## Concluding Data in Our Paper

1. **`Literature_Review/data/Performance_Analysis_literature_review.xlsx`**: Contains detailed information on the 66 papers reviewed in our literature analysis, including Year, Cites, Pages, URL, Venue Type, Performance Issue, Factor, Approach Type, dataset link, and more.

2. **`Large_Scale_Exploration/Keywords.txt`**: A list of 87 keywords related to performance issues that we gathered from 100 websites and several foundation papers, supporting for our filtering step in the Large-Scale Exploration of Real-World Discussions on Android Performance Issues. 

3. **Real-World Data**:
   - **`Large_Scale_Exploration/Manually_Checked_Data/UserReviews_with_label.csv`**
   - **`Large_Scale_Exploration/Manually_Checked_Data/SO_data_with_label.csv`**
   - **`Large_Scale_Exploration/Manually_Checked_Data/GitHub_commits_with_labels.csv`**
   - **`Large_Scale_Exploration/Manually_Checked_Data/GitHub_issues_with_labels.csv`**

   These files contain data collected and manually checked from user reviews, Stack Overflow, GitHub issues, and GitHub commits, as described in Section 2 "A LARGE-SCALE EXPLORATION OF REAL-WORLD APPS". They include performance issues identified in the real world, corresponding factors, root causes, and potential solutions.

4. **`Large_Scale_Exploration/common_patterns.txt`**: Lists the common performance issue code patterns identified from our real-world exploration.

## Source Code

1. **Crawling Data**:
   - **Run** **`Large_Scale_Exploration/1_crawl_GitHub_Code_Repositories.py`**, **`Large_Scale_Exploration/1_crawl_GitHub_Commits.py`**, **`Large_Scale_Exploration/1_crawl_User_Reviews.py`**, **`Large_Scale_Exploration/1_crawl_StackOverflow.py`**,  to crawl GitHub issues and commits, user reviews, and Stack Overflow discussions.
   - **Run** **`Literature_Review/paper_search_in_five_repos.py`** to crawl and filter papers in five libraries.
   
2. **Filtering Data**:
   **- Run **`Large_Scale_Exploration/2_data_processor.py`** to filter out user reviews, GitHub issues, commits, and Stack Overflow discussions related to performance issues based on keywords.**

3. **Statistic Data**:
   **- **Run** **`Literature_Review/statistic_literature.py`** and **`Large_Scale_RealWorld_Exploratory/statistic_real_world.py`** to gather all the data involved in the paper and their statistics.
