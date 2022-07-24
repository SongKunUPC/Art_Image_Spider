import pandas as pd
import time
import requests
from pyquery import PyQuery as pq

# 定义一个字母列表
Fam_List = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k',
            'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
            'w', 'x', 'y', 'z']

# 定义基础网站地址
base_url = 'https://commons.wikimedia.org'

# 定义查询的HTML
middle_url = '/w/index.php?title=Category:Google_Art_Project_works_by_artist&from='
# 定义headers
headers = {'user-agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
           }
# 定义首页的css查询路径
css_path = '#content #mw-content-text .mw-category-generated .mw-content-ltr li'
# 定义二级界面image查询路径
css_path_image = None
# 定义二级界面summary查询路径
css_path_summary = None
# 定义一个csv文件用来存放所有需要爬取的html的地址
file_name = 'Art_List.cvs'


# 定义一个写入文件的函数
def write_to_file(content):
    with open(file_name, 'a', encoding='utf-8') as f:
        f.write(content[0] + ',' + content[1] + '\n')


# 定义一个写成excel的函数
def creat_excel(file_name):
    df = pd.DataFrame(pd.read_csv(file_name, encoding='utf-8', names=['Name', 'URL']))
    # 丢弃重复的URL地址行
    df.drop_duplicates(subset='URL', keep='last', inplace=True)
    df.to_excel('Art_List.xlsx')

# 定义一个获取单页html的函数
def get_one_page(i):
    try:
        # request获取网页的响应
        url = base_url + middle_url + i
        response = requests.get(url, headers=headers)
        # 将响应的解码方式转换为自身
        print("成功进入页面")
        response.encoding = response.apparent_encoding
        # 获取网页本身的html文本
        content = response.text
        # 将获取的html文本传递给pyquery
        doc = pq(content)
        # 返回一个所有页面的生成器
        for item in doc(css_path).items():
            yield (
                i,
                base_url + (item('a').attr('href')),
            )
    except Exception as e:
        print('Error', e.args)

def main():
    for i in Fam_List:
        print('即将下载:%s页' % i)
        for content in get_one_page(i):
            print(content)
            write_to_file(content)
        time.sleep(1)
    creat_excel(file_name)

if __name__ == '__main__':
    main()