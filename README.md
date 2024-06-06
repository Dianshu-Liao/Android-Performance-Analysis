

# Android-Performance-Analysis

This artifact package includes all the data and code in the paper **Automatic Android Performance Analysis: How Far Are We?**.
Due to GitHub's limited capacity, we have uploaded all our source code and data to Google Cloud Drive. You can access this link to our source code and data: https://drive.google.com/file/d/13Gidayqi1hyYMIfRGXVG07aoXQ0hMM3U/view?usp=sharing


## Concluding Data in Our Paper

1. **`Concluding_Data/Performance_Analysis_literature_review.xlsx`**: Contains detailed information on the 48 papers reviewed in our literature analysis, including Year, Cites, Pages, URL, Venue Type, Performance Issue, Factor, Approach Type, dataset link, and more.

2. **`Concluding_Data/Keywords.txt`**: A list of 82 keywords related to performance issues that we gathered during the snowballing process.

3. **Real-World Data**:
   - **`Concluding_Data/filtered_UserReviews.csv`**
   - **`Concluding_Data/filtered_SO_data.csv`**
   - **`Concluding_Data/GitHub_Issues.csv`**
   - **`Concluding_Data/GitHub_Commit.csv`**

   These files contain data collected and manually checked from user reviews, Stack Overflow, GitHub issues, and GitHub commits, as described in Section 3 "A LARGE-SCALE EXPLORATION OF REAL-WORLD APPS". They include performance issues identified in the real world, corresponding factors, root causes, and potential solutions.

4. **`Concluding_Data/common_patterns.txt`**: Lists the common patterns identified from our real-world exploration. While only five types are discussed in the paper, this file contains the complete list.



## How We Collected Data from the Real World

1. **Crawling Data**:
   - Run `Real_World_Data_Process/1_crawl_User_Reviews.py`, `Real_World_Data_Process/1_crawl_GitHub_Code_Repositories_and_Issues.py`, `Real_World_Data_Process/1_crawl_GitHub_Commits.py`, `Real_World_Data_Process/1_crawl_StackOverflow.py` to crawl user reviews, GitHub issues and commits, and Stack Overflow discussions.

2. **Filtering Data**:
   - Run `Real_World_Data_Process/1_SOData_code_filter.py` to find all discussions containing code tags.
   - Run `Real_World_Data_Process/2_data_processor.py` to filter out user reviews, GitHub issues, commits, and Stack Overflow discussions related to performance issues based on keywords.

### Data Files

- **User Reviews**:
  - `Real_World_Data_Process/data/UserReviewData/UserReviews.csv`: Contains data on 7,681 apps.
  - `Real_World_Data_Process/data/UserReviewData/UserReviews.csv`: Contains 909,430 user reviews we collected.
  - `Real_World_Data_Process/data/UserReviewData/saved_negative_reviews.csv`: Contains 60,684 negative reviews identified through sentiment analysis.
  - `Real_World_Data_Process/data/UserReviewData/filtered_UserReviews.csv`: Contains 132 user reviews filtered by keywords.

- **Stack Overflow Discussions**:
  - `Real_World_Data_Process/data/SOdata/SO_data.csv`: Contains 448,977 Stack Overflow discussions.
  - `Real_World_Data_Process/data/SOdata/filtered_SO_Data.csv`: Contains 773 discussions filtered by keywords.

- **GitHub Issues**:
  - `Real_World_Data_Process/data/GitHub_Repo_Data/FD_issues.csv`: Contains 35,278 GitHub issues.
  - `Real_World_Data_Process/data/GitHub_Repo_Data/filtered_FD_issues.csv`: Contains 297 issues filtered by keywords.

- **GitHub Commits**:
  - `Real_World_Data_Process/data/GitHub_Repo_Data/merged_csv_commit.csv`: Contains 550,973 GitHub commits.
  - `Real_World_Data_Process/data/GitHub_Repo_Data/filtered_FD_commits.csv`: Contains 645 commits filtered by keywords.
