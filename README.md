

# Android-Performance-Analysis

This artifact package includes all the data and code in the paper **''Automatic Android Performance Analysis: How Far Are We?''**.
Due to GitHub's limited capacity, we have uploaded all our source code and data to Google Cloud Drive. You can access this link to our source code and data: https://drive.google.com/file/d/13Gidayqi1hyYMIfRGXVG07aoXQ0hMM3U/view?usp=sharing


## Source Code

1. **Crawling Data**:
   - **Run** **`Real_World_Data_Process/1_crawl_GitHub_Code_Repositories.py`**, **`Real_World_Data_Process/1_crawl_GitHub_Commits.py`**, **`Real_World_Data_Process/1_crawl_User_Reviews.py`**, **`Real_World_Data_Process/1_1_crawl_StackOverflow.py`**, **`Real_World_Data_Process/1_2_Adding_Code_Tag_to_SO.py`** to crawl GitHub issues and commits, user reviews, and Stack Overflow discussions.

2. **Filtering Data**:
   **- Run **`Real_World_Data_Process/2_data_processor.py`** to filter out user reviews, GitHub issues, commits, and Stack Overflow discussions related to performance issues based on keywords.**

3. **Statistic Data**:
   **- **Run** **`statistic_literature_review.py`** and **`statistic_real_world.py`** to gather all the data involved in the paper and their statistics.

### Data Files

- **User Reviews**:
  - **`real_world_study/UserReviewData/AppRankList.csv`**: Contains data on 7,681 apps.
  - **`real_world_study/UserReviewData/UserReviews.csv`**: Contains 909,430 user reviews we collected.
  - **`real_world_study/UserReviewData/saved_negative_reviews.csv`**: Contains 60,684 negative reviews identified through sentiment analysis.
  - **`real_world_study/UserReviewData/filtered_UserReviews.csv`**: Contains 132 user reviews filtered by keywords.

- **Stack Overflow Discussions**:
  - **`real_world_study/SOdata/SO_data.csv`**: Contains 448,977 Stack Overflow discussions.
  - **`real_world_study/SOdata/SO_data_with_code.csv`**: Contains 360,372 Stack Overflow discussions containing the `code` tag.
  - **`real_world_study/SOdata/filtered_SO_Data.csv`**: Contains 773 discussions filtered by keywords.

- **GitHub Issues**:
  - **`real_world_study/GitHub_Repo_Data/FD_issues.csv`**: Contains 35,278 GitHub issues.
  - **`real_world_study/GitHub_Repo_Data/filtered_FD_issues.csv`**: Contains 297 issues filtered by keywords.

- **GitHub Commits**:
  - **`real_world_study/GitHub_Repo_Data/merged_csv_commit.csv`**: Contains 550,973 GitHub commits.
  - **`real_world_study/GitHub_Repo_Data/filtered_FD_commits.csv`**: Contains 645 commits filtered by keywords.



## Concluding Data in Our Paper

1. **`literature_review/Performance_Analysis_literature_review.xlsx`**: Contains detailed information on the 48 papers reviewed in our literature analysis, including Year, Cites, Pages, URL, Venue Type, Performance Issue, Factor, Approach Type, dataset link, and more.

2. **`literature_review/Keywords.txt`**: A list of 82 keywords related to performance issues that we gathered during the snowballing process.

3. **Real-World Data**:
   - **`real_world_study/Manually_Checked_Data/UserReviews.csv`**
   - **`real_world_study/Manually_Checked_Data/StackOverflow.csv`**
   - **`real_world_study/Manually_Checked_Data/GitHub_Issues.csv`**
   - **`real_world_study/Manually_Checked_Data/GitHub_Commit.csv`**

   These files contain data collected and manually checked from user reviews, Stack Overflow, GitHub issues, and GitHub commits, as described in Section 3 "A LARGE-SCALE EXPLORATION OF REAL-WORLD APPS". They include performance issues identified in the real world, corresponding factors, root causes, and potential solutions.

4. **`real_world_study/common_patterns.txt`**: Lists the common performance issue code patterns identified from our real-world exploration.

5. **`real_world_study/Manually_Checked_Data/all_relations_and_how_many_tools_addressed.csv`** lists the number of tools available to address each performance issue caused by specific factors.

