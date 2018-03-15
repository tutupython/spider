from urllib import request,parse
from typedecorator import params, returns, setup_typecheck
# https://github.com/dobarkod/typedecorator/
# pip install typedecorator
import re
import time
import os

# -*- coding: UTF-8 -*-
# typedecorator初始化
setup_typecheck()
# 自定义异常
# class Error(Exception):
#     pass
# class Pic_item_get_error(Error):
#     # 图片获取异常
#     def __init__(self, expression, message):
#         self.expression = "图片获取异常"
#         self.message = "图片获取异常"
#获取页面，使用typedecorator校验传入参数是否合法
#typedecorator使用方式请参考https://github.com/dobarkod/typedecorator/
@params(key_word=str,page_num=int)
def get_page(key_word,page_num):
    #构建URL
    url_page_num=page_num*20
    url="http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+parse.quote(key_word) +"&pn="+str(url_page_num)+"&gsm=50&ct=&ic=0&lm=-1&width=0&height=0"
    print(url)
    resp=request.urlopen(url)
    # 需要调用decode将bytes类型的返回值转为字符串，便于后续正则匹配
    html=resp.read().decode("utf-8")
    return html

#解析页面获取图片url列表
def parse_page(html_by_str):
    #匹配图片ulr为："objURL"："图片url",
    parttern=re.compile('"objURL":"(.*?)",')
    pic_url_list=re.findall(parttern,html_by_str)
    return pic_url_list

#创建目录
def make_dir(keyword):
    path = "E:/百度图片爬虫/"
    #存储路径为关键字+时间戳
    path = path+keyword+time.strftime("%Y-%m-%d", time.localtime())
    if os.path.exists(path):
        print(path + '目录已存在')
        return path
    else:
        os.makedirs(path)
        return path

def get_pic_to_file(keyword,page_num,path):
    i=0
    # 获取第page_num页
    html_by_str = get_page(keyword, page_num)
    # 解析页面获取图片url列表
    pic_url_list = parse_page(html_by_str)
    for pic_items in pic_url_list:
        try:
            #获取图片数据
            pic_data_response = request.urlopen(pic_items)
            pic_data = pic_data_response.read()
            #写入文件，采用wb用二进制模式写入，文件名为E:/百度图片爬虫/关键字+时间-页码-图片号.jpg
            with open(path+'/'+keyword+time.strftime("%Y%m%d%H%M%S", time.localtime())+"-"+str(page_num)+"-"+str(i)+'.jpg','wb') as file:
                file.write(pic_data)
                file.closed
            i=i+1
        except Exception as e:
            #在相同目录写入错误日志
            with open(path+'/'+'error_log.txt','a') as error_file:
                error_file.write(pic_items+'下载失败。。。'+'异常原因：'+repr(e)+'\n')
            continue

if __name__=="__main__":
    keyword = input("input keyword about images you want to download: ")
    page_num= int(input("how many pages you want to download "))
    # 创建目录
    path = make_dir(keyword)
    #页码从1开始，所以实际下载的页面为page_num+1
    for i in range(1,page_num+1):
        print("downloading page:"+str(i)+"....")
        get_pic_to_file(keyword,i,path)
    exit()