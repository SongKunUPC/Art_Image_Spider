import pandas as pd
import time
import requests
from pyquery import PyQuery as pq

headers = {'user-agent':
               'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36'
           }

url = 'https://commons.wikimedia.org/wiki/Category:Google_Art_Project_works_by_Abd_al-Rahim'

base_url = 'https://commons.wikimedia.org'
# 图片地址的中间路径
middle_url = '#/media/File:'

# -----页面的css路径抽取-----begin--------
# 定义初始url的css路径
Base_CSS = 'body #content #bodyContent #mw-content-text .gallerytext a'
# 定义获取图片初始地址的css路径
Imag_Css = 'body #content #bodyContent #mw-content-text .fullImageLink a img'
# 定义寻找整个tbody的css路径,后面需要跟上.children('div').children('table').children('tbody')
Tbody_CSS = 'body #content #bodyContent #mw-content-text #mw-imagepage-content .mw-parser-output'
# 定义寻找Artist的CSS路径
Artist_CSS = 'tr td[id=fileinfotpl_aut]'
# 定义寻找Titled的CSS路径
Title_CSS = 'tr td div[class=fn] span i'
# 定义寻找Object_type的CSS路径,需要在之后加入next()以查找兄弟节点，item('tr td[id=fileinfotpl_art_object_type]').next().text()
Object_type_CSS = 'tr td[id=fileinfotpl_art_object_type]'
# 定义寻找Date的CSS，同样使用next()
Date_CSS = 'tr td[id=fileinfotpl_date]'
# Medium，next
Medium_CSS = 'tr td[id=fileinfotpl_art_medium]'
# Dimensions ,next
Dimensions_CSS = 'tr td[id=fileinfotpl_art_dimensions]'
# Collection 'tr td[id=fileinfotpl_art_gallery]'  next  'div table tbody tr bdi a'
Collection_CSS = [
    'tr td[id=fileinfotpl_art_gallery]',
    'div table tbody tr bdi a'
]
# Accession_number next
Accession_number_CSS = 'tr td[id=fileinfotpl_art_id]'
# Source next
Source_CSS = 'tr td[id=fileinfotpl_src]'
Imag_Orign_CSS = ''


# -----页面的css路径抽取-----end--------


def get_doc(url, headers):
    try:
        response = requests.get(url=url, headers=headers)
        response.encoding = response.apparent_encoding
        content = response.text
        doc = pq(content)
        return doc
    except Exception as e:
        print('Error', e.args)
        doc = None
        return doc

# 定义写入日志文件
def write_to_log(content):
    with open('log.cvs', 'a', encoding='utf-8') as f:
        for item in content:
            f.write(item + ',')
        f.write('\n')

# 定义写入summary文件
def write_to_summary(content):
    with open('summary.cvs', 'a', encoding='utf-8') as f:
        for item in content:
            f.write(item + ',')
        f.write('\n')


df = pd.read_csv('Art_List.cvs', names=['home', 'URL'], encoding='utf-8')
for url in df['URL'].head():
    doc = get_doc(url, headers)
    # 获取summary中的内容
    # summary所在a节点的css路径''body #content #bodyContent #mw-content-text .gallerytext a''
    for item in doc(Base_CSS).items():
        print(item.attr('href'))
        # 获取summary的相对地址
        url_sum_temp = item.attr('href')
        # 拼接summary的绝对地址
        url_sum = base_url + url_sum_temp
        print(url_sum)
        # 获取summary所在的页面doc
        doc_summary = get_doc(url_sum, headers)
        # 获取Tbody的qp对象
        Tbody_doc = doc_summary(Tbody_CSS).children('div').children('table').children('tbody')
        # 获得Artist
        Artist = Tbody_doc(Artist_CSS).next()('div').text().split('Detail', 1)[0].replace('\n', '')
        Title = Tbody_doc(Title_CSS).text()
        object_type = Tbody_doc(Object_type_CSS).next().text()
        Date = Tbody_doc(Date_CSS).next().text()
        Medium = Tbody_doc(Medium_CSS).next().text()
        Dimensions = Tbody_doc(Dimensions_CSS).next().text()
        Collection = Tbody_doc(Collection_CSS[0]).next()(Collection_CSS[1]).text()
        Accession_number = Tbody_doc(Accession_number_CSS).next().text()
        Source = Tbody_doc(Source_CSS).next().text()

        # 定位图片所在的CSS路径
        item_img = doc_summary(Imag_Css)

        str_temp = item_img.attr('src')
        # 删除地址中的 /thumb
        str_temp_re = str_temp.replace('/thumb', '')
        # 以 .jpg切割地址
        str_imga_url = str_temp_re.split('.jpg', 1)[0] + '.jpg'

        # 定位图片的filename
        # file_name_ex = df['home'].loc[df['URL']==url][0]
        file_name_ad = doc_summary('body #content h1').text().replace('File:', '')  # 去除File:
        # path = 'img/' + file_name_ex
        # file_name = path + '/' + file_name_ad
        # print(file_name)

        try:
            # # 判断路径是否存在，不存在创建
            # if not os.path.exists(path):
            #     os.makedirs(path)
            with open(file_name_ad, 'wb') as f:
                f.write(requests.get(str_imga_url, headers=headers).content)
                time.sleep(2)
                print('写入文件成功：', file_name_ad)
            Summary_List = [
                file_name_ad,Artist, Title, object_type, Date, Medium, Dimensions, Collection, Accession_number, Source,
            ]
            write_to_summary(Summary_List)
        except Exception as e:
            print('发生错误，', e.args)
            write_to_log([url])
        continue
    continue
