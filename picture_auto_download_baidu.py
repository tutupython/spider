from urllib import request,parse
# -*- coding: UTF-8 -*-
def get_page():
    page_num=0
    url_page_num=page_num*20
    key_word='暴走'
    url="http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word="+parse.quote(key_word) +"&pn="+str(url_page_num)+"&gsm=50&ct=&ic=0&lm=-1&width=0&height=0"
    print(url)
    resp=request.urlopen(url)
    html=resp.read()
    print(html)

if __name__=="__main__":
    get_page()