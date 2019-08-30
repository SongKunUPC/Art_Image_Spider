# a line
# 我正在工作aaaaaaaaaaaaaa
# master分支添加一行
# dev中添加一行
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
# 添加一行注释
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


doc = get_doc(url,headers)
# 获取summary中的内容
# summary所在a节点的css路径''body #content #bodyContent #mw-content-text .gallerytext a''
for item in doc(Base_CSS).items():
    print(item.attr('href'))
    # 获取summary的相对地址
    url_sum_temp = item.attr('href')
    # 拼接summary的绝对地址
    url_sum =  base_url+url_sum_temp
    print(url_sum)
    # 获取summary所在的页面doc
    doc_summary = get_doc(url_sum,headers)
    # 获取Tbody的qp对象
    Tbody_doc = doc_summary(Tbody_CSS).children('div').children('table').children('tbody')
    # 获得Artist
    Artist = Tbody_doc(Artist_CSS).next()('div').text().split('Detail',1)[0].replace('\n','')
    Title = Tbody_doc(Title_CSS).text()
    object_type = Tbody_doc(Object_type_CSS).next().text()
    Date = Tbody_doc(Date_CSS).next().text()
    Medium = Tbody_doc(Medium_CSS).next().text()
    Dimensions = Tbody_doc(Dimensions_CSS).next().text()
    Collection = Tbody_doc(Collection_CSS[0]).next()(Collection_CSS[1]).text()
    Accession_number = Tbody_doc(Accession_number_CSS).next().text()
    Source = Tbody_doc(Source_CSS).next().text()
    # 合并列表
    Summary_List = [
        Artist,Title,object_type,Date,Medium,Dimensions,Collection,Accession_number,Source,
    ]
    print(Summary_List)


    # 定位图片所在的CSS路径
    item_img = doc_summary(Imag_Css)
    str_temp = item_img.attr('src')
    # 删除地址中的 /thumb
    str_temp_re = str_temp.replace('/thumb', '')
    # 以 .jpg切割地址
    # 定位图片的filename
    file_name = doc_summary('body #content h1').text().replace('File:','')  # 去除File:
    print(file_name)
    str_imga_url = str_temp_re.split('.jpg', 1)[0] + '.jpg'
    try:
        with open(file_name,'wb') as f:
            f.write(requests.get(str_imga_url,headers=headers).content)
            time.sleep(3)
            print('写入文件成功：',file_name)
    except Exception as e:
        print('发生错误，',e.args)
    continue
# for item in doc(Imag_Css).items():
#     # url_img_tmp = item.attr('alt')
#     # # 拼接进入图片的url地址
#     # # url_img = url + middle_url + url_img_tmp
#     # # # 获取img所在页面的doc
#     # # doc_img = get_doc(url_img,headers)
#     # 由于图片采用Ajax异步加载，无法通过网页代码直接获取图片的下载地址
#     # 根据规律拼接网页的图片下载地址
#     str_temp = item.attr('src')
#     # 删除地址中的 /thumb
#     str_temp_re = str_temp.replace('/thumb','')
#     # 以 .jpg切割地址
#     str_imga_url = str_temp_re.split('.jpg',1)[0] + '.jpg'
#     with open('%s.jpg'%Summary_List[])
