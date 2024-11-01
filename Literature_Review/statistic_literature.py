
from wordcloud import WordCloud
import pandas as pd
import matplotlib.pyplot as plt

import plotly.graph_objects as go
from matplotlib.sankey import Sankey
import plotly.io as pio
pio.kaleido.scope.mathjax = None


def word_cloud():

    df = pd.read_excel('Performance_Analysis_papers.xlsx')
    all_abstracts = df['Abstract'].tolist()
    abstract_texts = ''
    for abstract in all_abstracts:
        abstract_texts += ' ' + abstract


    # Create a word cloud
    wordcloud = WordCloud(width = 800, height = 400, background_color ='white').generate(abstract_texts)

    # Display the generated image:
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # Save the image in SVG format
    wordcloud.to_file("wordcloud.pdf")



# 自定义函数替换字符串中的空格
def replace_space(s):
    words = s.split()
    if len(words) == 3:
        return words[0] + '\n' + ' '.join(words[1:])
    return s

def performance_issues_per_year(data_path='data/Performance_Analysis_literature_review.xlsx'):
    # 从Excel文件中读取数据
    df = pd.read_excel(data_path)

    # 拆分 performance issue 列中的多个问题
    df_expanded = df.assign(performance_issue=df['Performance Issue'].str.split('\n')).explode('performance_issue')

    # 统计每个年份每个问题的数量
    issue_counts = df_expanded.groupby(['performance_issue', 'Year']).size().unstack(fill_value=0)

    # 将计数结果转换为所需的格式
    issue_counts.reset_index(inplace=True)
    issue_counts.columns.name = None
    issue_counts.columns = issue_counts.columns.astype(str)

    # 计算每行的总和，并添加到 DataFrame 中
    issue_counts['total'] = issue_counts.iloc[:, 1:].sum(axis=1)

    # 按总和对行进行排序
    issue_counts = issue_counts.sort_values(by='total', ascending=False).drop(columns='total').reset_index(drop=True)

    # 打印结果
    print(issue_counts)

    # 准备颜色映射
    colors = {
        '2012': '#FFFFFF',
        '2013': '#B8B6C6',
        '2014': '#C4BFC3',
        '2015': '#E2D7D8',
        '2016': '#EBDBDA',
        '2017': '#C899A2',
        '2018': '#D4C15D',
        '2019': '#754D45',
        '2020': '#D4AB82',
        '2021': '#AEAD8E',
        '2022': '#98BF95',
        '2023': '#508A63',
        '2024': '#6496B2',
    }

    # 移除无关年份的颜色
    available_years = issue_counts.columns[1:]  # 排除 'performance_issue' 列
    colors = {year: colors[year] for year in available_years if year in colors}

    # 将 performance issue 中的空格替换为换行符
    issue_counts['performance_issue'] = issue_counts['performance_issue'].str.replace('Distorted UI Display', 'Distorted\nUI Display').replace('Data Loss', 'Data\nLoss').replace('Memory Consumption', 'Memory\nConsumption').replace('Energy Consumption', 'Energy\nConsumption')

    # 绘制图表
    fig, ax = plt.subplots(figsize=(14, 6))

    categories = issue_counts['performance_issue']
    bottoms = [0] * len(categories)  # 用于堆叠条形图
    bar_height = 0.6  # 设置条形图的高度，调整此值以增加空隙

    for year in available_years:
        values = issue_counts[year]
        bars = ax.barh(categories, values, left=bottoms, height=bar_height, color=colors[year], edgecolor='black',
                       label=year)

        # 在每个条形图上添加对应的数字
        for bar, value in zip(bars, values):
            if value > 0:  # 仅在值大于0时添加文本
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                        str(value), ha='center', va='center', fontsize=25, color='black', fontweight='bold')

        bottoms = [i + j for i, j in zip(bottoms, values)]

    # 添加浅色的竖线
    ax.grid(axis='x', color='lightgray', linestyle='--', linewidth=0.5)

    # 设置标签和标题
    ax.set_xlabel('Number of publications', fontsize=30, fontweight='bold')

    # 设置纵坐标的标签字体加粗并倾斜
    ax.set_yticklabels(ax.get_yticklabels(), fontsize=25, fontweight='bold', style='italic')

    # 设置横坐标的标签字体加粗并倾斜
    ax.set_xticklabels(ax.get_xticklabels(), fontsize=25, fontweight='bold', style='italic')

    # 调整图例
    legend = ax.legend(title='Year', prop={'size': 25}, handlelength=2, handleheight=1, ncol=2)
    plt.setp(legend.get_title(), fontsize=20, fontweight='bold')  # 设置图例标题字体大小

    # 调整布局以避免空白
    plt.tight_layout()

    plt.savefig('performance_issues_per_year.pdf', bbox_inches='tight')
    # 显示图表
    plt.show()

def performance_issues_to_factors_relations():
    performance_issue_and_factor = {
        'Energy Consumption': ['Resource', 'Background Thread', 'Database Operation', 'Loop', 'Redundant Frames', 'Multi-Threads',
                               'HTTP Request', 'Obsolete Task', 'Image', 'Service', 'Wakelock', 'Dynamic UI Loading',
                               'UI Rendering', 'AsyncTask', 'Inefficient Method', 'Display Screen', 'Programming Language',
                               'Advertisements', 'Machine Learning Algorithm', 'View'],
        'Responsiveness': ['Image', 'Dynamic UI Loading', 'UI Rendering', 'Main Thread', 'Activity', 'AsyncTask',
                           'View', 'Obsolete Task', 'SQL Statement', 'Advertisements', 'Message'],
        'Memory Consumption': ['Image', 'Service', 'Resource', 'AsyncTask', 'View', 'Third-Party Library',
                               'UI Rendering', 'Data Type', 'Obsolete Task'],
        'CPU Usage': ['UI Rendering'],
        'GPU Usage': ['UI Rendering']
    }




    # Create lists for the source, target, and value for the Sankey diagram
    source = []
    target = []
    value = []

    for issue, factors in performance_issue_and_factor.items():
        for factor in factors:
            source.append(issue)
            target.append(factor)
            value.append(1)  # Each connection is counted once

    # Convert to indices for the Sankey diagram
    all_nodes = list(set(source + target))
    source_indices = [all_nodes.index(issue) for issue in source]
    target_indices = [all_nodes.index(factor) for factor in target]

    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=5,
            thickness=15,  # Reduce thickness
            line=dict(color="black", width=0.5),
            label=all_nodes,
        ),
        link=dict(
            source=source_indices,
            target=target_indices,
            value=value,
        )
    )])

    fig.update_layout(
        font_size=10,
        margin=dict(l=10, r=10, t=10, b=10),  # Reduce margins to minimize white space

        # margin=dict(l=200, r=200, t=10, b=30), # Adjust margins to reduce distance
        height = 600,  # Adjust height to fit content
        width = 400,  # Adjust width to fit content
    )
    # fig.show()
    fig.write_image("Performance_Issues_and_Factors.pdf", format='pdf')


if __name__ == '__main__':
    data_path = 'data/Performance_Analysis_literature_review.xlsx'
    performance_issues_per_year(data_path)
    performance_issues_to_factors_relations()







