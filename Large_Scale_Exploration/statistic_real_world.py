import pandas as pd
from collections import defaultdict, Counter
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import cohen_kappa_score

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
        if "" in factors:
            a = 1
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

def performance_issues_and_factors_statistic(user_review_path, so_data_path, github_commit_path, github_issue_path):

    user_review_issue_df = count_user_review_performance_issues(user_review_path)

    so_issues_df, so_factors_df = count_performance_issues_and_factors(so_data_path)
    so_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=so_data_path)

    commit_issues_df, commit_factors_df = count_performance_issues_and_factors(csv_file=github_commit_path)
    commit_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(
        csv_file=github_commit_path)

    issue_issues_df, issue_factors_df = count_performance_issues_and_factors(csv_file=github_issue_path)
    issue_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(
        csv_file=github_issue_path)

    return (user_review_issue_df, so_issues_df, so_factors_df, so_issue_and_corresponding_factors, commit_issues_df,
            commit_factors_df, commit_issue_and_corresponding_factors, issue_issues_df, issue_factors_df,
            issue_issue_and_corresponding_factors)


def statistic_performance_issue_contributions(user_review_labeled_result_path, so_labeled_result_path,
                                              github_commit_labeled_result_path, github_issue_labeled_result_path):
    user_review_issue_df = count_user_review_performance_issues(user_review_labeled_result_path)
    so_issues_df, so_factors_df = count_performance_issues_and_factors(so_labeled_result_path)
    commit_issues_df, commit_factors_df = count_performance_issues_and_factors(github_commit_labeled_result_path)
    issue_issues_df, issue_factors_df = count_performance_issues_and_factors(github_issue_labeled_result_path)

    # 创建一行四个子图
    fig, axes = plt.subplots(1, 4, figsize=(24, 6), gridspec_kw={'wspace': 0.05})

    pie_chart_for_performance_issues(user_review_issue_df, axes[0], title='User Review')
    pie_chart_for_performance_issues(so_issues_df, axes[1], title='Stack Overflow')
    pie_chart_for_performance_issues(commit_issues_df, axes[2], title='GitHub Commits')
    pie_chart_for_performance_issues(issue_issues_df, axes[3], title='GitHub Issues')

    # 添加全局图例
    color_dict = {
        'Responsiveness': '#1f77b4',
        'Memory Consumption': '#ff7f0e',
        'Energy Consumption': '#2ca02c',
        'Storage Consumption': '#9467bd',
        'CPU Usage': '#d62728',
        'Internet Data Usage': '#17becf',
        'GPU Usage': '#bcbd22'
    }
    labels = list(color_dict.keys())
    handles = [plt.Line2D([0], [0], color=color, lw=4) for color in color_dict.values()]
    fig.legend(handles, labels, loc='center left', ncol=1, fontsize=16, bbox_to_anchor=(0.02, 0.5))

    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('data/statistic_result/performance_issues_pie_charts.pdf', format='pdf')
    plt.show()


def pie_chart_for_performance_issues(df, ax, title, fontsize=12, radius=0.4):
    # 定义每个 performance issue 的颜色字典
    color_dict = {
        'Responsiveness': '#1f77b4',
        'Memory Consumption': '#ff7f0e',
        'Energy Consumption': '#2ca02c',
        'Storage Consumption': '#9467bd',
        'CPU Usage': '#d62728',
        'Internet Data Usage': '#17becf',
        'GPU Usage': '#bcbd22'
    }

    total_num = df['Count'].sum()

    # 计算百分比并排序
    df = df.assign(Percentage=(df['Count'] / total_num) * 100).sort_values(by='Percentage', ascending=False)

    sizes = df['Count']
    size_percentage = df['Percentage']

    # 获取每个 performance issue 对应的颜色
    colors = [color_dict.get(label, '#000000') for label in df['performance issue']]  # 如果没有匹配到颜色，则使用默认黑色

    # 如果比例小于5%，则手动分配额外显示空间
    display_sizes = [max(size, 5) for size in size_percentage]

    # 设置 Explode 参数，小于5%的部分移出
    explode = [0.05 if size < 5 else 0 for size in size_percentage]

    # 创建饼图，设置相关参数
    wedges, _, autotexts = ax.pie(display_sizes, autopct='%1.1f%%', startangle=90,
                                  explode=explode, pctdistance=0.85, labeldistance=1.1, colors=colors,
                                  radius=radius)

    # 保证饼图为圆形
    ax.axis('equal')

    # 设置标题

    ax.set_xlabel(title, fontsize=fontsize, labelpad=20)

    # 调整百分比标签字体大小
    for autotext, percentage in zip(autotexts, df['Percentage']):
        autotext.set_text(f'{percentage:.1f}%')
        autotext.set_fontsize(fontsize)

    plt.tight_layout()


def statistic_factors_contributions(so_factors_df, commit_factors_df, issue_factors_df):
    all_factors = set(so_factors_df['factor']).union(set(commit_factors_df['factor'])).union(
        set(issue_factors_df['factor']))
    data = {'factor': list(all_factors)}
    result_df = pd.DataFrame(data)
    result_df['so_count'] = result_df['factor'].map(so_factors_df.set_index('factor')['Count']).fillna(0)
    result_df['commit_count'] = result_df['factor'].map(commit_factors_df.set_index('factor')['Count']).fillna(0)
    result_df['issue_count'] = result_df['factor'].map(issue_factors_df.set_index('factor')['Count']).fillna(0)

    # 计算总和并排序
    result_df['total_count'] = result_df['so_count'] + result_df['commit_count'] + result_df['issue_count']

    # 为result_df画一个bar图，横坐标是factor，纵坐标是total_count。
    result_df = result_df.sort_values(by='total_count', ascending=False)

    fig, ax = plt.subplots(figsize=(14, 5))
    x = np.arange(len(result_df))
    bar_width = 0.8
    bars_so = ax.bar(x, result_df['so_count'], color='#D99695', width=bar_width, label='SO Discussion')
    bars_commit = ax.bar(x, result_df['commit_count'], bottom=result_df['so_count'], color='#C0D69B', width=bar_width, label='GitHub Commit')
    bars_issue = ax.bar(x, result_df['issue_count'], bottom=result_df['so_count'] + result_df['commit_count'], color='#95B3D8', width=bar_width, label='GitHub Issue')

    ax.set_ylabel('Count', fontsize=20)
    ax.set_xticks(x)
    ax.set_xticklabels(result_df['factor'], rotation=60, fontsize=15, ha='right')
    ax.legend(fontsize=15)
    plt.tight_layout()
    plt.show()
    a = 1


def bar_for_three_data_df(ax1, ax2, so_factors_df, commit_factors_df, issue_factors_df):
    all_factors = set(so_factors_df['factor']).union(set(commit_factors_df['factor'])).union(set(issue_factors_df['factor']))



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



#判断每一个类型的performance issue对应的factor出现的次数。不是每一类performance issue有多少个factor，而是每一个performance issue对应的factor出现了多少次。
def performance_issue_to_factor_relationships(commit_issue_and_corresponding_factors, issue_issue_and_corresponding_factors, so_issue_and_corresponding_factors):

    dict_performance_issue_factor_count = {'performance issue': [], 'factor': [], 'count': []}
    for _, row in commit_issue_and_corresponding_factors.iterrows():
        issues = row['performance issue'].split('\n')
        factors = row['factor'].split('\n')
        for issue in issues:
            for factor in factors:
                dict_performance_issue_factor_count['performance issue'].append(issue)
                dict_performance_issue_factor_count['factor'].append(factor)
                dict_performance_issue_factor_count['count'].append(row['count'])

    for _, row in issue_issue_and_corresponding_factors.iterrows():
        issues = row['performance issue'].split('\n')
        factors = row['factor'].split('\n')
        for issue in issues:
            for factor in factors:
                dict_performance_issue_factor_count['performance issue'].append(issue)
                dict_performance_issue_factor_count['factor'].append(factor)
                dict_performance_issue_factor_count['count'].append(row['count'])

    for _, row in so_issue_and_corresponding_factors.iterrows():
        issues = row['performance issue'].split('\n')
        factors = row['factor'].split('\n')
        for issue in issues:
            for factor in factors:
                dict_performance_issue_factor_count['performance issue'].append(issue)
                dict_performance_issue_factor_count['factor'].append(factor)
                dict_performance_issue_factor_count['count'].append(row['count'])

    df_performance_issue_factor_count = pd.DataFrame(dict_performance_issue_factor_count)
    # find the rows that the performance issue and factor are the same, and sum the count
    df_performance_issue_factor_count = df_performance_issue_factor_count.groupby(['performance issue', 'factor']).sum().reset_index()
    df_performance_issue_factor_count = df_performance_issue_factor_count.sort_values(by='count', ascending=False)

    return df_performance_issue_factor_count

def statistic_taxonomy(commit_issue_and_corresponding_factors, issue_issue_and_corresponding_factors, so_issue_and_corresponding_factors):
    df_real_world_performance_issue_factor_count = performance_issue_to_factor_relationships(
        commit_issue_and_corresponding_factors, issue_issue_and_corresponding_factors,
        so_issue_and_corresponding_factors)
    real_world_unique_performance_issues = set(df_real_world_performance_issue_factor_count['performance issue'])
    real_world_unique_factors = set(df_real_world_performance_issue_factor_count['factor'])

    literature_performance_issue_and_factor = {
        'Energy Consumption': ['Resource', 'Background Thread', 'Database Operation', 'Loop', 'Redundant Frames',
                               'Multi-Threads',
                               'HTTP Request', 'Obsolete Task', 'Image', 'Service', 'Wakelock', 'Dynamic UI Loading',
                               'UI Rendering', 'AsyncTask', 'Inefficient Method', 'Display Screen',
                               'Programming Language',
                               'Advertisements', 'Machine Learning Algorithm', 'View'],
        'Responsiveness': ['Resource', 'Image', 'Dynamic UI Loading', 'UI Rendering', 'HTTP Request', 'Main Thread', 'Activity', 'AsyncTask',
                           'View', 'Obsolete Task', 'SQL Statement', 'Advertisements', 'Message', 'Loop'],
        'Memory Consumption': ['Image', 'Service', 'Resource', 'AsyncTask', 'View', 'Third-Party Library',
                               'UI Rendering', 'Data Type', 'Obsolete Task'],
        'CPU Usage': ['UI Rendering'],
        'GPU Usage': ['UI Rendering']
    }

    literature_performance_issue_and_factor_count = {'performance issue': [], 'factor': [], 'count': []}
    for issue, factors in literature_performance_issue_and_factor.items():
        for factor in factors:
            literature_performance_issue_and_factor_count['performance issue'].append(issue)
            literature_performance_issue_and_factor_count['factor'].append(factor)
            literature_performance_issue_and_factor_count['count'].append(1)

    df_literature_performance_issue_factor_count = pd.DataFrame(literature_performance_issue_and_factor_count)
    literature_performance_issues = set(df_literature_performance_issue_factor_count['performance issue'])
    literature_factors = set(df_literature_performance_issue_factor_count['factor'])

    total_performance_issue_factor = pd.concat(
        [df_real_world_performance_issue_factor_count, df_literature_performance_issue_factor_count],
        ignore_index=True).drop(columns='count').drop_duplicates()

    total_performance_issues = set(total_performance_issue_factor['performance issue'])
    total_factors = set(total_performance_issue_factor['factor'])


    #get a intersection of real world and literature
    relations_in_real_world_and_literature = df_real_world_performance_issue_factor_count.merge(df_literature_performance_issue_factor_count, on=['performance issue', 'factor'], how='inner')

    # use len(relations_in_real_world_and_literature) / len(df_real_world_performance_issue_factor_count) to calculate the percentage of real world relations that are also in literature
    print('intersection relations / real-world relations: ', len(relations_in_real_world_and_literature) / len(df_real_world_performance_issue_factor_count))




    print('Real-World Unique Performance Issues: ', len(real_world_unique_performance_issues))
    print('Real-World Unique Factor-to-Performance Relations: ', len(df_real_world_performance_issue_factor_count))
    print('Literature Unique Performance Issues: ', len(literature_performance_issues))
    print('Literature Unique Factor-to-Performance Relations: ', len(df_literature_performance_issue_factor_count))

    print('Total Unique Performance Issues: ', len(total_performance_issues))
    print('Total Unique Factor-to-Performance Relations: ', len(total_performance_issue_factor))




if __name__ == '__main__':
    user_review_labeled_result_path = 'Manually_Checked_Data/UserReviews_with_label.csv'
    so_labeled_result_path = 'Manually_Checked_Data/SO_data_with_label.csv'
    github_commit_labeled_result_path = 'Manually_Checked_Data/GitHub_commits_with_labels.csv'
    github_issue_labeled_result_path = 'Manually_Checked_Data/GitHub_issues_with_labels.csv'

    statistic_performance_issue_contributions(user_review_labeled_result_path, so_labeled_result_path,
                                              github_commit_labeled_result_path, github_issue_labeled_result_path)

    (user_review_issue_df, so_issues_df, so_factors_df, so_issue_and_corresponding_factors, commit_issues_df,
     commit_factors_df, commit_issue_and_corresponding_factors, issue_issues_df, issue_factors_df,
     issue_issue_and_corresponding_factors) = performance_issues_and_factors_statistic(user_review_labeled_result_path,
                                                                                       so_labeled_result_path,
                                                                                       github_commit_labeled_result_path,
                                                                                       github_issue_labeled_result_path)
