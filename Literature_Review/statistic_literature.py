
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




def replace_space(s):
    words = s.split()
    if len(words) == 3:
        return words[0] + '\n' + ' '.join(words[1:])
    return s

def performance_issues_per_year(data_path='data/Performance_Analysis_literature_review.xlsx'):

    df = pd.read_excel(data_path)


    df_expanded = df.assign(performance_issue=df['Performance Issue'].str.split('\n')).explode('performance_issue')


    issue_counts = df_expanded.groupby(['performance_issue', 'Year']).size().unstack(fill_value=0)


    issue_counts.reset_index(inplace=True)
    issue_counts.columns.name = None
    # issue_counts.columns = issue_counts.columns.astype(str)

    issue_counts.columns = [
        str(int(col)) if col != 'performance_issue' else col
        for col in issue_counts.columns
    ]


    issue_counts['total'] = issue_counts.iloc[:, 1:].sum(axis=1)


    issue_counts = issue_counts.sort_values(by='total', ascending=False).drop(columns='total').reset_index(drop=True)


    print(issue_counts)


    colors = {
        ''
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


    available_years = issue_counts.columns[1:]  # 排除 'performance_issue' 列
    colors = {year: colors[year] for year in available_years if year in colors}


    issue_counts['performance_issue'] = issue_counts['performance_issue'].str.replace('Internet Data Usage', 'Internet Data\nUsage').replace('Data Loss', 'Data\nLoss').replace('Memory Consumption', 'Memory\nConsumption').replace('Energy Consumption', 'Energy\nConsumption')


    fig, ax = plt.subplots(figsize=(14, 6))

    categories = issue_counts['performance_issue']
    bottoms = [0] * len(categories)
    bar_height = 0.6

    for year in available_years:
        values = issue_counts[year]
        bars = ax.barh(categories, values, left=bottoms, height=bar_height, color=colors[year], edgecolor='black',
                       label=year)


        for bar, value in zip(bars, values):
            if value > 0:
                ax.text(bar.get_x() + bar.get_width() / 2, bar.get_y() + bar.get_height() / 2,
                        str(value), ha='center', va='center', fontsize=25, color='black', fontweight='bold')

        bottoms = [i + j for i, j in zip(bottoms, values)]


    # ax.grid(axis='x', color='lightgray', linestyle='--', linewidth=0.5)


    ax.set_xlabel('Number of publications', fontsize=30, fontweight='bold')


    ax.set_yticklabels(ax.get_yticklabels(), fontsize=25, fontweight='bold', style='italic')


    ax.set_xticklabels(ax.get_xticklabels(), fontsize=25, fontweight='bold', style='italic')


    legend = ax.legend(title='Year', prop={'size': 22}, handlelength=2, handleheight=1, ncol=2)
    plt.setp(legend.get_title(), fontsize=20, fontweight='bold')  # 设置图例标题字体大小


    plt.tight_layout()

    plt.savefig('performance_issues_per_year.pdf', bbox_inches='tight')

    plt.show()



if __name__ == '__main__':
    data_path = 'data/Performance_Analysis_literature_review.xlsx'
    performance_issues_per_year(data_path)






