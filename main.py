from xml.etree import ElementTree
import os
import pandas as pd
import matplotlib.pyplot as plt


def plot_bar(df, xlabel, ylabel, rotation=0):
    '''
    画图
    :param df:一个DataFrame
    :param xlabel:横轴文字
    :param ylabel:纵轴文字
    :param rotation:横轴文字显示旋转角度，默认为0，即不旋转
    '''
    plt.figure(figsize=(20, 10))
    plt.xticks(fontsize=10, rotation=rotation)
    plt.yticks(fontsize=10)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    x = df.iloc[:, 0]
    y = df.iloc[:, 1]
    plt.bar(x, y)
    # plt.show()
    plt.savefig(f'./pic/{xlabel}_{ylabel}.png', dpi=300, bbox_inches='tight')


'''
xml文件需要自行收集并放到data下面，同时此脚本以dblp为准，其他位置收集的xml可能不能用
收集完后就可以跑出3个图和3个表格
'''
xmlfile_list = os.listdir('./data')
xmlcontlist = [open(f'./data/{file}', 'r').read() for file in xmlfile_list]
xmllist = [ElementTree.fromstring(xml) for xml in xmlcontlist]

'''
解析xml并转换成字典
'''
name2cnt = dict()
year2cnt = dict()
book2cnt = dict()
for xml in xmllist:
    ls = xml.iter("author")
    for x in ls:
        name = x.text
        if name not in name2cnt:
            name2cnt[name] = 1
        else:
            name2cnt[name] += 1
    ls = xml.iter("booktitle")
    for x in ls:
        book = x.text
        if book not in book2cnt:
            book2cnt[book] = 1
        else:
            book2cnt[book] += 1
    ls = xml.iter("journal")
    for x in ls:
        book = x.text
        if book not in book2cnt:
            book2cnt[book] = 1
        else:
            book2cnt[book] += 1
    ls = xml.iter("year")
    for x in ls:
        year = int(x.text)
        if year not in year2cnt:
            year2cnt[year] = 1
        else:
            year2cnt[year] += 1
namecnt = pd.DataFrame({'作者名字': list(name2cnt.keys()), '论文数量': list(name2cnt.values())})
namecnt = namecnt.sort_values(by="论文数量", ascending=False)
namecnt.to_excel('./excel/作者名字与论文数量.xlsx')
bookcnt = pd.DataFrame({'会议/期刊名字': list(book2cnt.keys()),
                        '论文数量': list(book2cnt.values())}).sort_values(by="论文数量", ascending=False)
bookcnt.to_excel("./excel/会议期刊名字与论文数量.xlsx")
yearcnt = pd.DataFrame({'年份': list(year2cnt.keys()),
                        '论文数量': list(year2cnt.values())}).sort_values(by="年份")
yearcnt.to_excel("./excel/年份与论文数量.xlsx")

'''
如果有哪个图的横坐标文字太长可以加一个旋转角度，类似下面的机构与论文数量作图
'''
plot_bar(namecnt.iloc[:10], 'Author Name', 'Paper Number')
plot_bar(bookcnt.iloc[:10], 'Book&Journal Name', 'Paper Number')
plot_bar(yearcnt.iloc[:10], 'Year', 'Paper Number')

'''
以下两个表格需要自己建立，且格式需要和示例保持一致
'''
if os.path.exists('./excel/国家与论文数量.xlsx'):
    countrycnt = pd.read_excel("./excel/国家与论文数量.xlsx").sort_values(by="论文数量", ascending=False)
    plot_bar(countrycnt.iloc[:10], 'Country', 'Paper Number')
if os.path.exists('./excel/机构与论文数量.xlsx'):
    orgcnt = pd.read_excel("./excel/机构与论文数量.xlsx").sort_values(by="论文数量", ascending=False)
    plot_bar(orgcnt.iloc[:10], 'Orgnization', 'Paper Number', 90)
