import  urllib.request
import re
url = "https://tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&ie=utf-8&pn=350"
"""
Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36
"""
headers = {
    "User-Agnet":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}

#设置一个请求体，一般都叫req
req = urllib.request.Request(url,headers=headers)



response = urllib.request.urlopen(req)

data = response.read().decode("utf-8")
#取到数据 进行数据处理 re

with open("Crawer.html","w",encoding='utf-8') as f:
    f.write(data)




