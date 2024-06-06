import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict, Counter
import numpy as np
from matplotlib.colors import ListedColormap

import seaborn as sns





Existing_Factors = ['Database Operation', 'Loop', 'Redundant Frames', 'Multi-Threads', 'HTTP Request',
                    'Background Thread',
                    'Obsolete Task', 'Image', 'Service', 'Wakelock', 'Resource', 'Dynamic UI Loading', 'UI Rendering',
                    'AsyncTask',
                    'Inefficient Method', 'View', 'Hashmap', 'SQL Statement', 'Message',
                    'Main Thread', 'Activity']

def count_user_review_performance_issues(csv_file):
    user_reviews = pd.read_csv(csv_file)
    user_reviews = user_reviews[user_reviews['performance issue'] != 'No']
    # 将所有 Performance Issues 合并成一个列表
    all_issues = []
    for issues in user_reviews['performance issue'].dropna():
        all_issues.extend(issues.split('\n'))

    # 统计每个 Performance Issue 的出现次数
    issue_counts = Counter(all_issues)

    # 将统计结果转换为 DataFrame 以便更容易查看
    issue_counts_df = pd.DataFrame.from_dict(issue_counts, orient='index', columns=['Count']).reset_index()
    issue_counts_df = issue_counts_df.rename(columns={'index': 'performance issue'})
    sorted_issue_counts_df = issue_counts_df.sort_values(by='Count', ascending=False).reset_index(drop=True)
    print('User Review Statistic: \n')
    print(sorted_issue_counts_df)
    return sorted_issue_counts_df


def count_performance_issues_and_factors(csv_file):
    data = pd.read_csv(csv_file)
    issue_column = 'performance issue'
    factor_column = 'factor'

    # 删除 performance issue 列为 'No' 的行
    df = data[data[issue_column] != 'No']
    # 删除 'factor' 列中不是空值的行
    df = df[df[factor_column] != 'No']

    # 初始化 Counter 对象来统计 issues 和 factors
    issue_counter = Counter()
    factor_counter = Counter()

    # 遍历每一行，统计 performance issues 和 factors
    for _, row in df.iterrows():
        issues = row[issue_column].split('\n')
        factors = row[factor_column].split('\n')

        issue_counter.update(issues)
        factor_counter.update(factors)

    # 将统计结果转换为 DataFrame
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

    # 遍历每一行，拆分 performance issues 和 factors，并建立映射关系
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



def bar_for_three_data_df(ax1, ax2, so_factors_df, commit_factors_df, issue_factors_df):
    # 统计所有出现的factors
    all_factors = set(so_factors_df['factor']).union(set(commit_factors_df['factor'])).union(set(issue_factors_df['factor']))

    new_factors = all_factors - set(Existing_Factors)
    literature_and_realworld_factors = all_factors | set(Existing_Factors)
    print('all factors in both literature and real-world: {}'.format(len(literature_and_realworld_factors)))
    # 创建一个新的 DataFrame，包含所有factors和三个来源的计数
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

    # # Top plot (60 to max)
    # bars_issue = ax1.bar(x, result_df['issue_count'], color='#AAAAAA', width=bar_width, label='GitHub Issue')
    # bars_commit = ax1.bar(x, result_df['commit_count'], bottom=result_df['issue_count'], color='#555555', width=bar_width, label='GitHub Commit')
    # bars_so = ax1.bar(x, result_df['so_count'], bottom=result_df['issue_count'] + result_df['commit_count'], color='#000000', width=bar_width, label='SO Discussion')
    # ax1.set_ylim(60, result_df['total_count'].max() + 25)
    #
    # # Bottom plot (0 to 30)
    # bars_issue_bottom = ax2.bar(x, result_df['issue_count'], color='#AAAAAA', width=bar_width)
    # bars_commit_bottom = ax2.bar(x, result_df['commit_count'], bottom=result_df['issue_count'], color='#555555', width=bar_width)
    # bars_so_bottom = ax2.bar(x, result_df['so_count'], bottom=result_df['issue_count'] + result_df['commit_count'], color='#000000', width=bar_width)
    # ax2.set_ylim(0, 30)

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


    # # Top plot (100 to max)
    # bars_user_review_top = ax3.bar(x, result_df['user_review_count'], color='#EBEBEB', width=bar_width, label='User Review')
    # bars_issue_top = ax3.bar(x, result_df['issue_count'], bottom=result_df['user_review_count'], color='#AAAAAA', width=bar_width, label='GitHub Issue')
    # bars_commit_top = ax3.bar(x, result_df['commit_count'], bottom=result_df['user_review_count'] + result_df['issue_count'], color='#555555', width=bar_width, label='GitHub Commit')
    # bars_so_top = ax3.bar(x, result_df['so_count'], bottom=result_df['user_review_count'] + result_df['issue_count'] + result_df['commit_count'], color='#000000', width=bar_width, label='SO Discussion')
    # ax3.set_ylim(100, result_df['total_count'].max() + 90)  # 增加顶部图表的y轴上限
    #
    # # Bottom plot (0 to 60)
    # bars_user_review_bottom = ax4.bar(x, result_df['user_review_count'], color='#EBEBEB', width=bar_width)
    # bars_issue_bottom = ax4.bar(x, result_df['issue_count'], bottom=result_df['user_review_count'], color='#AAAAAA', width=bar_width)
    # bars_commit_bottom = ax4.bar(x, result_df['commit_count'], bottom=result_df['user_review_count'] + result_df['issue_count'], color='#555555', width=bar_width)
    # bars_so_bottom = ax4.bar(x, result_df['so_count'], bottom=result_df['user_review_count'] + result_df['issue_count'] + result_df['commit_count'], color='#000000', width=bar_width)
    # ax4.set_ylim(0, 60)

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


def match_new_factors(df_factor):

    factors = df_factor['factor'].tolist()
    new_factors = list(set(factors) - set(Existing_Factors))
    return new_factors

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

    # 转换为集合
    literature_set = set(literature_factors)
    realworld_set = set(all_realworld_factors)

    # 找到独有和共有的元素
    unique_to_literature = literature_set - realworld_set
    unique_to_realworld = realworld_set - literature_set
    common_elements = literature_set & realworld_set


    all_factors = list(set(all_literature_factors + so_factors + commit_factors + issue_factors))
    a = 1



def all_relations(so_issue_and_corresponding_factors, commit_issue_and_corresponding_factors,
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

    # get all performance issues and factors relationships.
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

    # 将字典展开为一个包含performance issue和对应factor的列表
    data = []
    for issue, factors in performance_issue_and_factor.items():
        for factor in factors:
            data.append([issue, factor])

    # 将列表转换为DataFrame
    df = pd.DataFrame(data, columns=['performance issue', 'factor'])
    df['tools_num'] = ''
    df.to_csv('all_relations_and_how_many_tools_addressed.csv', index=False)



def hot_figure():
    df = pd.read_csv('all_relations_and_how_many_tools_addressed.csv')
    df['performance issue'] = df['performance issue'].str.replace('Distorted UI Display', 'Distorted\nUI Display').replace('Data Loss', 'Data\nLoss').replace('Energy Consumption', 'Energy\nConsumption').replace('Memory Consumption', 'Memory\nConsumption')

    # 创建一个透视表，以便将数据转换为heatmap的格式，使用-1替换NaN
    pivot_table = df.pivot_table(index='performance issue', columns='factor', values='tools_num', fill_value=-1)

    # 添加一行 'Data Storage'，所有值为-1
    pivot_table.loc['Data\nConsumption'] = -1

    # 对行进行排序：有factors越多的行放在越下面
    pivot_table = pivot_table.loc[pivot_table.isin([0, 1, 2, 3, 4, 5]).sum(axis=1).sort_values().index]

    # 对列进行排序：有performance issues越多的列放在最左边
    pivot_table = pivot_table[pivot_table.isin([0, 1, 2, 3, 4, 5]).sum(axis=0).sort_values(ascending=False).index]

    # 自定义颜色映射，将-1映射为白色
    cmap = ListedColormap(['white'] + sns.color_palette("YlGnBu", n_colors=256).as_hex())

    # 使用heatmap绘制图表，显示-1为白色
    plt.figure(figsize=(25, 7))  # 增加图表高度
    ax = sns.heatmap(pivot_table, annot=False, cmap=cmap, linewidths=.5, linecolor='black',
                     cbar_kws={'label': 'tools_num'},
                     cbar=True, vmin=-1, vmax=pivot_table.max().max())

    # 设置标签和标题
    ax.set_xlabel('Factors', fontsize=20, fontweight='bold')
    ax.set_ylabel('Performance Issues', fontsize=20, fontweight='bold')

    # 调整x轴标签字体大小和旋转角度
    plt.xticks(rotation=35, ha='right', fontsize=20)

    # 调整y轴标签字体大小
    plt.yticks(fontsize=20)

    # 在最右边添加竖线
    last_col_index = len(pivot_table.columns)
    ax.axvline(x=last_col_index, color='black', linewidth=1.5)


    # 显示图表
    plt.tight_layout()


    plt.savefig('performance_issues_heatmap.pdf', format='pdf', bbox_inches='tight')



    plt.show()


if __name__ == '__main__':
    so_data_path = 'filtered_SO_data.csv'
    github_commit_path = 'GitHub_Commit.csv'
    github_issue_path = 'GitHub_Issues.csv'
    user_review_path = 'filtered_UserReviews.csv'



    user_review_issue_df = count_user_review_performance_issues(csv_file=user_review_path)




    so_issues_df, so_factors_df = count_performance_issues_and_factors(csv_file=so_data_path)
    so_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=so_data_path)
    new_factors_in_SO = match_new_factors(so_factors_df)

    commit_issues_df, commit_factors_df = count_performance_issues_and_factors(csv_file=github_commit_path)
    commit_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=github_commit_path)
    new_factors_in_commit = match_new_factors(commit_factors_df)

    issue_issues_df, issue_factors_df = count_performance_issues_and_factors(csv_file=github_issue_path)
    issue_issue_and_corresponding_factors = relations_between_issues_and_factors_in_github_commits(csv_file=github_issue_path)
    new_factors_in_issue = match_new_factors(issue_factors_df)

    statistic_performance_issue_and_factors(so_issue_and_corresponding_factors, commit_issue_and_corresponding_factors,
                                            issue_issue_and_corresponding_factors)


    fig, ((ax1, ax3), (ax2, ax4)) = plt.subplots(2, 2, sharex=False, figsize=(25, 8),
                                                 gridspec_kw={'height_ratios': [1, 2], 'width_ratios': [1, 3.5]})

    bar_for_three_data_df(ax3, ax4, so_factors_df, commit_factors_df, issue_factors_df)
    bar_for_4_issues_data_df(ax1, ax2, user_review_issue_df, so_issues_df, commit_issues_df, issue_issues_df)


    fig.savefig('performance_issues_and_factors_distribution.pdf')

    hot_figure()