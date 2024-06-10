from utils import Util
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict, Counter
import numpy as np
from matplotlib.colors import ListedColormap


Existing_Factors = ['Database Operation', 'Loop', 'Redundant Frames', 'Multi-Threads', 'HTTP Request',
                    'Background Thread',
                    'Obsolete Task', 'Image', 'Service', 'Wakelock', 'Resource', 'Dynamic UI Loading',
                    'UI Rendering',
                    'AsyncTask',
                    'Inefficient Method', 'View', 'Hashmap', 'SQL Statement', 'Message',
                    'Main Thread', 'Activity']

def statistic_csvs_under_a_folder(directory):
    all_csv_files = Util.find_files(directory, '.csv')
    csvs = [pd.read_csv(csv_file) for csv_file in all_csv_files]
    combined_csv = pd.concat(csvs, ignore_index=True)
    deduplicated_csv = combined_csv.drop_duplicates()
    return deduplicated_csv

def statistic_for_Github_data():
    reduplicated_FD_data_csv = statistic_csvs_under_a_folder('real_world_study/GitHub_Repo_Data/FDdata')
    redunplicated_FD_issues = statistic_csvs_under_a_folder('real_world_study/GitHub_Repo_Data/FDissues')
    keyword_filtered_issues = pd.read_csv('real_world_study/GitHub_Repo_Data/filtered_FD_issues.csv')
    commits = pd.read_csv('real_world_study/GitHub_Repo_Data/merged_csv_commit.csv')
    deduplicated_commits = commits.drop_duplicates()
    keyword_filtered_commits = pd.read_csv('real_world_study/GitHub_Repo_Data/filtered_FD_commits.csv')
    commit_data_after_manually_checking = pd.read_csv('real_world_study/Manually_Checked_Data/GitHub_Commit.csv')
    final_commit_data = commit_data_after_manually_checking[(commit_data_after_manually_checking['performance issue'] != 'No')
                                                    & (commit_data_after_manually_checking['factor'] != 'No')]

    issue_data_after_manually_checking = pd.read_csv('real_world_study/Manually_Checked_Data/GitHub_Issues.csv')
    final_issue_data = issue_data_after_manually_checking[(issue_data_after_manually_checking['performance issue'] != 'No')
                                                    & (issue_data_after_manually_checking['factor'] != 'No')]
    print('======================================GitHub Data Collection=====================================')
    print('The number of apps : {}'.format(len(reduplicated_FD_data_csv)))
    print('The number of issues : {}'.format(len(redunplicated_FD_issues)))
    print('The number of issues after keyword filter: {}'.format(len(keyword_filtered_issues)))
    print('The number of issues after manually checking: {}'.format(len(final_issue_data)))
    print('The number of commits: {}'.format(len(deduplicated_commits)))
    print('The number of commits after keyword filter: {}'.format(len(keyword_filtered_commits)))
    print('The number of commits after manually checking: {}'.format(len(final_commit_data)))
    print('=================================================================================================')

def statistic_for_SO_data():
    so_data = pd.read_csv('real_world_study/SOdata/SO_data.csv')
    so_data_with_code = pd.read_csv('real_world_study/SOdata/SO_data_with_code.csv')
    filtered_so_data = pd.read_csv('real_world_study/SOdata/filtered_SO_data.csv')
    so_data_after_manually_checking = pd.read_csv('real_world_study/Manually_Checked_Data/StackOverflow.csv')
    final_so_data = so_data_after_manually_checking[(so_data_after_manually_checking['performance issue'] != 'No')
                                                    & (so_data_after_manually_checking['factor'] != 'No')]
    print('===================================Stack Overflow Data Collection================================')
    print('The number of so questions : {}'.format(len(so_data)))
    print('The number of so questions with code: {}'.format(len(so_data_with_code)))
    print('The number of filtered SO questions: {}'.format(len(filtered_so_data)))
    print('The number of SO questions after manually checking: {}'.format(len(final_so_data)))
    print('=================================================================================================')
def statistic_for_user_review():
    user_reviews = pd.read_csv('real_world_study/UserReviewData/UserReviews.csv')
    user_reviews = user_reviews.drop(columns=['ReviewId'])
    user_reviews = user_reviews.drop_duplicates()
    negative_reviews = pd.read_csv('real_world_study/UserReviewData/saved_negative_reviews.csv')
    filtered_user_reviews = pd.read_csv('real_world_study/UserReviewData/filtered_UserReviews.csv')
    manually_checked_reviews = pd.read_csv('real_world_study/Manually_Checked_Data/UserReviews.csv')
    final_reviews = manually_checked_reviews[manually_checked_reviews['performance issue'] != 'No']
    print('===================================User Review Data Collection===================================')
    print('The number of user reviews: {}'.format(len(user_reviews)))
    print('The number of negative reviews: {}'.format(len(negative_reviews)))
    print('The number of filtered user reviews: {}'.format(len(filtered_user_reviews)))
    print('The number of user reviews after manually checking: {}'.format(len(final_reviews)))
    print('=================================================================================================')

def format_label(label):
    if label == '':
        return label
    # elif label == 'Distorted UI Display':
    #     return 'Distorted\nUI Display'
    elif label == 'Memory Consumption':
        return 'Memory\nConsumption'
    # elif label == 'Energy Consumption':
    #     return 'Energy\nConsumption'
    # elif label == 'Dynamic UI Loading':
    #     return 'Dynamic UI\nLoading'
    # elif label == 'Inefficient Method':
    #     return 'Inefficient\nMethod'
    # elif label == 'Third-party Library':
    #     # return 'Third-party\nLibrary'
    #     return '3rd-party Lib'
    #
    # elif label == 'Database Operation':
    #     return 'Database\nOperation'
    # elif label == 'Object Creation':
    #     return 'Object\nCreation'
    # elif 'Other ' in label:
    #     return label.replace('Other ', 'Other\n')
    else:
        return label



def match_new_factors(df_factor):



    factors = df_factor['factor'].tolist()
    new_factors = list(set(factors) - set(Existing_Factors))
    return new_factors

def match_new_performance_issue(df_performance_issue):
    Existing_performance_issues = ['Memory Consumption', 'Responsiveness', 'Data Loss', 'Energy Consumption', 'Distorted UI Display']
    performance_issues = df_performance_issue['performance issue'].tolist()
    new_performance_issues = list(set(performance_issues) - set(Existing_performance_issues))
    return new_performance_issues


def count_user_review_performance_issues(csv_file):
    user_reviews = pd.read_csv(csv_file)
    user_reviews = user_reviews[user_reviews['performance issue'] != 'No']

    all_issues = []
    for issues in user_reviews['performance issue'].dropna():
        all_issues.extend(issues.split('\n'))

    # Count the number of occurrences of each Performance Issue
    issue_counts = Counter(all_issues)

    # Convert the statistics to a DataFrame for easier viewing
    issue_counts_df = pd.DataFrame.from_dict(issue_counts, orient='index', columns=['Count']).reset_index()
    issue_counts_df = issue_counts_df.rename(columns={'index': 'performance issue'})
    sorted_issue_counts_df = issue_counts_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
    # print('User Review Statistic: \n')
    # print(sorted_issue_counts_df)
    return sorted_issue_counts_df


def count_performance_issues_and_factors(csv_file):
    data = pd.read_csv(csv_file)
    issue_column = 'performance issue'
    factor_column = 'factor'

    # Delete rows with 'No' in the 'performance issue' column
    df = data[data[issue_column] != 'No']
    # Delete rows in the 'factor' column that are not null values
    df = df[df[factor_column] != 'No']

    # Initialise the Counter object to count issues and factors.
    issue_counter = Counter()
    factor_counter = Counter()

    # Iterate through each row, counting performance issues and factors
    for _, row in df.iterrows():
        issues = row[issue_column].split('\n')
        factors = row[factor_column].split('\n')

        issue_counter.update(issues)
        factor_counter.update(factors)

    # Convert the statistics to a DataFrame
    issues_df = pd.DataFrame.from_dict(issue_counter, orient='index', columns=['Count']).reset_index()
    issues_df = issues_df.rename(columns={'index': 'performance issue'})

    factors_df = pd.DataFrame.from_dict(factor_counter, orient='index', columns=['Count']).reset_index()
    factors_df = factors_df.rename(columns={'index': 'factor'})

    return issues_df, factors_df

def relations_between_issues_and_factors_in_github_commits(csv_file):
    issue_column = 'performance issue'
    factor_column = 'factor'
    df = pd.read_csv(csv_file)
    df = df[df[issue_column] != 'No']
    df = df[df[factor_column] != 'No']

    issue_to_factors = defaultdict(list)

    for _, row in df.iterrows():
        issues = row[issue_column].split('\n')
        factors = row[factor_column].split('\n')

        for issue in issues:
            issue_to_factors[issue].extend(factors)

    # 创建一个 DataFrame 存储结果
    rows = []
    for issue, factors in issue_to_factors.items():
        factor_count = Counter(factors)
        for factor, count in factor_count.items():
            rows.append({'performance issue': issue, 'factor': factor, 'count': count})

    result_df = pd.DataFrame(rows)
    result_df = result_df.sort_values(by=['performance issue', 'count'], ascending=[True, False])

    return result_df


def hot_figure():
    df = pd.read_csv('real_world_study/Manually_Checked_Data/all_relations_and_how_many_tools_addressed.csv')
    df['performance issue'] = df['performance issue'].str.replace('Distorted UI Display', 'Distorted\nUI Display').replace('Data Loss', 'Data\nLoss').replace('Energy Consumption', 'Energy\nConsumption').replace('Memory Consumption', 'Memory\nConsumption')

    # Create a pivot table to convert the data to heatmap format, replacing NaN with -1
    pivot_table = df.pivot_table(index='performance issue', columns='factor', values='tools_num', fill_value=-1)

    # Add a line for 'Data Consumption' with all values -1
    pivot_table.loc['Data\nConsumption'] = -1

    # Sort the rows: rows with more factors are placed lower down
    pivot_table = pivot_table.loc[pivot_table.isin([0, 1, 2, 3, 4, 5]).sum(axis=1).sort_values().index]

    # Sort the columns: columns with more performance issues are placed on the leftmost side
    pivot_table = pivot_table[pivot_table.isin([0, 1, 2, 3, 4, 5]).sum(axis=0).sort_values(ascending=False).index]

    # Custom colour mapping, mapping -1 to white
    cmap = ListedColormap(['white'] + sns.color_palette("YlGnBu", n_colors=256).as_hex())

    # Plot the chart using heatmap to show -1 as white
    plt.figure(figsize=(25, 7))
    ax = sns.heatmap(pivot_table, annot=False, cmap=cmap, linewidths=.5, linecolor='black',
                     cbar_kws={'label': 'tools_num'},
                     cbar=True, vmin=-1, vmax=pivot_table.max().max())


    ax.set_xlabel('Factors', fontsize=20, fontweight='bold')
    ax.set_ylabel('Performance Issues', fontsize=20, fontweight='bold')

    # Adjust x-axis label font size and rotation angle
    plt.xticks(rotation=35, ha='right', fontsize=19)

    # Adjust y-axis label font size
    plt.yticks(fontsize=20)

    # Add vertical lines to the far right
    last_col_index = len(pivot_table.columns)
    ax.axvline(x=last_col_index, color='black', linewidth=1.5)

    # Increase color bar scale font size
    cbar = ax.collections[0].colorbar
    cbar.ax.tick_params(labelsize=20)
    cbar.set_label('Tools Num', size=20)

    plt.tight_layout()


    plt.savefig('performance_issues_heatmap.pdf', format='pdf', bbox_inches='tight')



    plt.show()

def statistic_performance_issue_and_factors(so_issue_and_corresponding_factors, commit_issue_and_corresponding_factors,
                                            issue_issue_and_corresponding_factors):
    performance_issue_and_factor = {
        'Energy Consumption': ['Database Operation', 'Loop', 'Redundant Frames', 'Multi-Threads', 'HTTP Request',
                               'Background Thread', 'Obsolete Task', 'Image', 'Service', 'Wakelock', 'Resource',
                               'Dynamic UI Loading', 'UI Rendering', 'AsyncTask', 'Inefficient Method', 'View',
                               'Hashmap'],
        'Responsiveness': ['Obsolete Task', 'Image', 'Dynamic UI Loading', 'UI Rendering', 'SQL Statement',
                           'Message', 'Main Thread', 'Activity', 'AsyncTask', 'View'],
        # 'App Crash': ['Image', 'Wakelock', 'Resource', 'Activity', 'AsyncTask'],
        'Memory Consumption': ['Obsolete Task', 'Image', 'Service', 'Resource', 'AsyncTask', 'View',
                               'Hashmap'],
        'Data Loss': ['Activity', 'AsyncTask'],
        'Distorted UI Display': ['Activity']
    }
    literature_factors = []
    for values in performance_issue_and_factor.values():
        literature_factors.extend(values)
    literature_factors = list(set(literature_factors))


    #get all performance issues and factors relationships.
    for _, row in so_issue_and_corresponding_factors.iterrows():
        performance_issue = row['performance issue']
        factor = row['factor']
        if performance_issue in performance_issue_and_factor:
            performance_issue_and_factor[performance_issue].append(factor)
        else:
            performance_issue_and_factor[performance_issue] = [factor]
    for _, row in commit_issue_and_corresponding_factors.iterrows():
        performance_issue = row['performance issue']
        factor = row['factor']
        if performance_issue in performance_issue_and_factor:
            performance_issue_and_factor[performance_issue].append(factor)
        else:
            performance_issue_and_factor[performance_issue] = [factor]
    for _, row in issue_issue_and_corresponding_factors.iterrows():
        performance_issue = row['performance issue']
        factor = row['factor']
        if performance_issue in performance_issue_and_factor:
            performance_issue_and_factor[performance_issue].append(factor)
        else:
            performance_issue_and_factor[performance_issue] = [factor]

    for key, value in performance_issue_and_factor.items():
        performance_issue_and_factor[key] = list(set(value))
    total_relations = sum(len(value) for value in performance_issue_and_factor.values())

    all_literature_factors = []
    for values in performance_issue_and_factor.values():
        all_literature_factors.extend(values)

    so_factors = so_issue_and_corresponding_factors['factor'].tolist()
    commit_factors = commit_issue_and_corresponding_factors['factor'].tolist()
    issue_factors = issue_issue_and_corresponding_factors['factor'].tolist()
    all_realworld_factors = list(set(so_factors+commit_factors+issue_factors))


    literature_set = set(literature_factors)
    realworld_set = set(all_realworld_factors)


    unique_to_literature = literature_set - realworld_set
    unique_to_realworld = realworld_set - literature_set
    common_elements = literature_set & realworld_set


    all_factors = list(set(all_literature_factors + so_factors + commit_factors + issue_factors))
    print('unique literature review factors: {}, num: {}'.format(unique_to_literature, len(unique_to_literature)))
    print('unique real-world factors: {}, num: {}'.format(unique_to_realworld, len(unique_to_realworld)))
    print('common factors: {}, num: {}'.format(common_elements, len(common_elements)))
    print('all factors in both literature review and real-world: {}'.format(len(all_factors)))




def performance_issues_and_factors_statistic(user_review_path, so_data_path, github_commit_path, github_issue_path):
    user_review_issue_df = count_user_review_performance_issues(csv_file=user_review_path)
    new_performance_issues_in_user_review = match_new_performance_issue(user_review_issue_df)

    so_issues_df, so_factors_df = count_performance_issues_and_factors(csv_file=so_data_path)
    so_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=so_data_path)
    new_factors_in_SO = match_new_factors(so_factors_df)
    new_performance_issues_in_stack_overflow = match_new_performance_issue(so_issues_df)

    commit_issues_df, commit_factors_df = count_performance_issues_and_factors(csv_file=github_commit_path)
    commit_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=github_commit_path)
    new_factors_in_commit = match_new_factors(commit_factors_df)
    new_performance_issues_in_commit = match_new_performance_issue(commit_issues_df)


    issue_issues_df, issue_factors_df = count_performance_issues_and_factors(csv_file=github_issue_path)
    issue_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=github_issue_path)
    new_factors_in_issue = match_new_factors(issue_factors_df)
    new_performance_issues_in_github_issue = match_new_performance_issue(issue_issues_df)










    print('Large-Scale Exploration of Real-World Apps Results:')
    print('==================User Review Performance Issues=======================')
    user_review_performance_issues_count = user_review_issue_df.set_index('performance issue')['Count'].to_dict()
    print('performance issues categories: {}, new performance issue: {}'.format(len(user_review_performance_issues_count), len(new_performance_issues_in_user_review)))
    print(user_review_performance_issues_count)
    print()


    print('==================Stack Overflow Performance Issues and Factors========')
    so_performance_issues_count = so_issues_df.set_index('performance issue')['Count'].to_dict()
    so_factor_count = so_factors_df.set_index('factor')['Count'].to_dict()
    print('performance issues categories: {}, factor categories: {}, new performance issue: {}, new factors: {}'.
          format(len(so_performance_issues_count), len(so_factor_count),
                 len(new_performance_issues_in_stack_overflow), len(new_factors_in_SO)))
    print(so_performance_issues_count)
    print(so_factor_count)
    print()


    print('==================GitHub Commit Performance Issues and Factors========')
    github_commit_performance_issues_count = commit_issues_df.set_index('performance issue')['Count'].to_dict()
    github_commit_factor_count = commit_factors_df.set_index('factor')['Count'].to_dict()
    print('performance issues categories: {}, factor categories: {}, new performance issue: {}, new factors: {}'.
          format(len(github_commit_performance_issues_count), len(github_commit_factor_count),
                 len(new_performance_issues_in_commit), len(new_factors_in_commit)))
    print(github_commit_performance_issues_count)
    print(github_commit_factor_count)
    print()



    print('==================GitHub Issue Performance Issues and Factors=========')
    github_issue_performance_issues_count = issue_issues_df.set_index('performance issue')['Count'].to_dict()
    github_issue_factor_count = issue_factors_df.set_index('factor')['Count'].to_dict()
    print('performance issues categories: {}, factor categories: {}, new performance issue: {}, new factors: {}'.
          format(len(github_issue_performance_issues_count), len(github_issue_factor_count),
                 len(new_performance_issues_in_github_issue), len(new_factors_in_issue)))
    print(github_issue_performance_issues_count)
    print(github_issue_factor_count)
    print()

    return (so_issue_and_corresponding_factors, commit_issue_and_corresponding_factors,
            issue_issue_and_corresponding_factors, so_factors_df, commit_factors_df, issue_factors_df,
            user_review_issue_df, so_issues_df, commit_issues_df, issue_issues_df)







def bar_for_three_data_df(ax1, ax2, so_factors_df, commit_factors_df, issue_factors_df):
    all_factors = set(so_factors_df['factor']).union(set(commit_factors_df['factor'])).union(set(issue_factors_df['factor']))

    new_factors = all_factors - set(Existing_Factors)
    literature_and_realworld_factors = all_factors | set(Existing_Factors)
    # print('all factors in both literature and real-world: {}'.format(len(literature_and_realworld_factors)))

    data = {'factor': list(all_factors)}
    result_df = pd.DataFrame(data)
    result_df['so_count'] = result_df['factor'].map(so_factors_df.set_index('factor')['Count']).fillna(0)
    result_df['commit_count'] = result_df['factor'].map(commit_factors_df.set_index('factor')['Count']).fillna(0)
    result_df['issue_count'] = result_df['factor'].map(issue_factors_df.set_index('factor')['Count']).fillna(0)

    # 计算总和并排序
    result_df['total_count'] = result_df['so_count'] + result_df['commit_count'] + result_df['issue_count']

    # 将count为2以下的factors变成other
    other_factors = result_df[result_df['total_count'] <= 2]

    low_count_factors = result_df[result_df['total_count'] <= 2].sum()
    low_count_factor_count = len(result_df[result_df['total_count'] <= 2])
    result_df = result_df[result_df['total_count'] > 2]

    result_df = result_df.sort_values(by='total_count', ascending=False)

    other_row = pd.DataFrame({
        'factor': [f'{low_count_factor_count} Other Factors'],
        'so_count': [low_count_factors['so_count']],
        'commit_count': [low_count_factors['commit_count']],
        'issue_count': [low_count_factors['issue_count']],
        'total_count': [low_count_factors['total_count']]
    })

    result_df = pd.concat([result_df, other_row], ignore_index=True)

    # 画堆积柱状图
    bar_width = 0.8
    x = np.arange(len(result_df))


    # Top plot (60 to max)
    bars_issue = ax1.bar(x, result_df['issue_count'], color='#95B3D8', width=bar_width, label='GitHub Issue')
    bars_commit = ax1.bar(x, result_df['commit_count'], bottom=result_df['issue_count'], color='#C0D69B', width=bar_width, label='GitHub Commit')
    bars_so = ax1.bar(x, result_df['so_count'], bottom=result_df['issue_count'] + result_df['commit_count'], color='#D99695', width=bar_width, label='SO Discussion')
    ax1.set_ylim(60, result_df['total_count'].max() + 40)

    # Bottom plot (0 to 30)
    bars_issue_bottom = ax2.bar(x, result_df['issue_count'], color='#95B3D8', width=bar_width)
    bars_commit_bottom = ax2.bar(x, result_df['commit_count'], bottom=result_df['issue_count'], color='#C0D69B', width=bar_width)
    bars_so_bottom = ax2.bar(x, result_df['so_count'], bottom=result_df['issue_count'] + result_df['commit_count'], color='#D99695', width=bar_width)
    ax2.set_ylim(0, 30)


    # Hide the spines between ax1 and ax2
    ax1.spines['bottom'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax1.xaxis.tick_top()

    ax1.tick_params(labeltop=False)  # don't put tick labels at the top
    ax2.xaxis.tick_bottom()

    d = .005  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=ax1.transAxes, color='k', clip_on=False)
    ax1.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    ax1.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax2.transAxes)  # switch to the bottom axes
    ax2.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax2.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # 添加总数到每个柱状图上方
    for i, total in enumerate(result_df['total_count']):
        if total > 60:
            ax1.text(x[i], total + 2, str(int(total)), ha='center', va='bottom', fontsize=25)
        else:
            ax2.text(x[i], total + 0.5, str(int(total)), ha='center', va='bottom', fontsize=25)  # 调整此处的vertical alignment

    # ax2.set_ylabel('Count', fontsize=30)
    ax1.tick_params(axis='y', labelsize=25)
    ax2.tick_params(axis='y', labelsize=25)


    ax2.set_xticks(x)
    # ax2.set_xticklabels(result_df['factor'], rotation=60, fontsize=23, ha='right')
    ax2.set_xticklabels([format_label(factor) for factor in result_df['factor']], rotation=45, ha='right', fontsize=22)
    ax1.margins(x=0.01)
    ax2.margins(x=0.01)

    ax1.legend(fontsize=20)


def bar_for_4_issues_data_df(ax3, ax4, user_review_issue_df, so_issues_df, commit_issues_df, issue_issues_df):
    # 统计所有出现的performance issues
    all_issues = set(user_review_issue_df['performance issue']).union(set(so_issues_df['performance issue'])).union(set(commit_issues_df['performance issue'])).union(set(issue_issues_df['performance issue']))

    # 创建一个新的 DataFrame，包含所有performance issues和四个来源的计数
    data = {'performance issue': list(all_issues)}
    result_df = pd.DataFrame(data)
    result_df['user_review_count'] = result_df['performance issue'].map(user_review_issue_df.set_index('performance issue')['Count']).fillna(0)
    result_df['so_count'] = result_df['performance issue'].map(so_issues_df.set_index('performance issue')['Count']).fillna(0)
    result_df['commit_count'] = result_df['performance issue'].map(commit_issues_df.set_index('performance issue')['Count']).fillna(0)
    result_df['issue_count'] = result_df['performance issue'].map(issue_issues_df.set_index('performance issue')['Count']).fillna(0)

    # 计算总和并排序
    result_df['total_count'] = result_df['user_review_count'] + result_df['so_count'] + result_df['commit_count'] + result_df['issue_count']
    result_df = result_df.sort_values(by='total_count', ascending=False)

    # 画堆积柱状图
    bar_width = 0.8
    x = np.arange(len(result_df))

    # Top plot (100 to max)
    bars_user_review_top = ax3.bar(x, result_df['user_review_count'], color='#FDDE92', width=bar_width, label='User Review')
    bars_issue_top = ax3.bar(x, result_df['issue_count'], bottom=result_df['user_review_count'], color='#95B3D8', width=bar_width, label='GitHub Issue')
    bars_commit_top = ax3.bar(x, result_df['commit_count'], bottom=result_df['user_review_count'] + result_df['issue_count'], color='#C0D69B', width=bar_width, label='GitHub Commit')
    bars_so_top = ax3.bar(x, result_df['so_count'], bottom=result_df['user_review_count'] + result_df['issue_count'] + result_df['commit_count'], color='#D99695', width=bar_width, label='SO Discussion')
    ax3.set_ylim(100, result_df['total_count'].max() + 140)  # 增加顶部图表的y轴上限

    # Bottom plot (0 to 60)
    bars_user_review_bottom = ax4.bar(x, result_df['user_review_count'], color='#FDDE92', width=bar_width)
    bars_issue_bottom = ax4.bar(x, result_df['issue_count'], bottom=result_df['user_review_count'], color='#95B3D8', width=bar_width)
    bars_commit_bottom = ax4.bar(x, result_df['commit_count'], bottom=result_df['user_review_count'] + result_df['issue_count'], color='#C0D69B', width=bar_width)
    bars_so_bottom = ax4.bar(x, result_df['so_count'], bottom=result_df['user_review_count'] + result_df['issue_count'] + result_df['commit_count'], color='#D99695', width=bar_width)
    ax4.set_ylim(0, 60)

    # Hide the spines between ax1 and ax2
    ax3.spines['bottom'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax3.xaxis.tick_top()
    ax3.tick_params(labeltop=False)  # don't put tick labels at the top
    ax4.xaxis.tick_bottom()

    d = .010  # how big to make the diagonal lines in axes coordinates
    kwargs = dict(transform=ax3.transAxes, color='k', clip_on=False)
    ax3.plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
    ax3.plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

    kwargs.update(transform=ax4.transAxes)  # switch to the bottom axes
    ax4.plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
    ax4.plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

    # 添加总数到每个柱状图上方
    for i, total in enumerate(result_df['total_count']):
        if total > 60:
            ax3.text(x[i], total + 2, str(int(total)), ha='center', va='bottom', fontsize=25)
        else:
            ax4.text(x[i], total + 0.5, str(int(total)), ha='center', va='bottom', fontsize=25)

    ax4.set_ylabel('Count', fontsize=25)
    ax3.tick_params(axis='y', labelsize=25)
    ax4.tick_params(axis='y', labelsize=25)

    ax4.set_xticks(x)
    # ax4.set_xticklabels(result_df['performance issue'], rotation=60, ha='right', fontsize=23)
    ax4.set_xticklabels([format_label(issue) for issue in result_df['performance issue']], rotation=45, ha='right', fontsize=22)

    ax3.margins(x=0.03)
    ax4.margins(x=0.03)

    ax3.legend(fontsize=17.5)

    plt.tight_layout()
    plt.show()



if __name__ == '__main__':
    statistic_for_user_review()
    statistic_for_SO_data()
    statistic_for_Github_data()
    user_review_path = 'real_world_study/Manually_Checked_Data/UserReviews.csv'
    so_data_path = 'real_world_study/Manually_Checked_Data/StackOverflow.csv'
    github_commit_path = 'real_world_study/Manually_Checked_Data/GitHub_Commit.csv'
    github_issue_path = 'real_world_study/Manually_Checked_Data/GitHub_Issues.csv'
    all_relations_and_tools_num_path = 'real_world_study/Manually_Checked_Data/all_relations_and_how_many_tools_addressed.csv',
    saved_heatmap_path = 'performance_issues_heatmap.pdf'
    saved_real_world_distribution_path = 'performance_issues_and_factors_distribution.pdf',

    (so_issue_and_corresponding_factors, commit_issue_and_corresponding_factors, issue_issue_and_corresponding_factors,
     so_factors_df, commit_factors_df, issue_factors_df,user_review_issue_df, so_issues_df, commit_issues_df, issue_issues_df) \
        =  performance_issues_and_factors_statistic(user_review_path, so_data_path, github_commit_path, github_issue_path)


    print('=================Statistic for Literature Review and Real-World Results=========')
    statistic_performance_issue_and_factors(so_issue_and_corresponding_factors, commit_issue_and_corresponding_factors,
                                            issue_issue_and_corresponding_factors)
    fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(2, 2, sharex=False, figsize=(25, 8),
                                                 gridspec_kw={'height_ratios': [1, 2], 'width_ratios': [1, 3.5]})

    bar_for_three_data_df(ax3, ax4, so_factors_df, commit_factors_df, issue_factors_df)
    bar_for_4_issues_data_df(ax1, ax2, user_review_issue_df, so_issues_df, commit_issues_df, issue_issues_df)


    fig.savefig('performance_issues_and_factors_distribution.pdf')


    hot_figure()