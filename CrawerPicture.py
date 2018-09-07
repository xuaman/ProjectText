import urllib.response
import  urllib.request
import re
import os
import pickle


def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径

toPath = r"D:\picture"
listPath = r"D:\picture\crawerList.data"
mkdir(toPath)

# if os.path.getsize(listPath) > 0:  # 判断文件是为空，如果为空就创建一个空字典 如果不为空就读取数据
#     f = open(listPath, "rb")
#     crawerList = pickle.load(f)
# else:
#
# print(crawerList[-1])
crawerList = ['//tieba.baidu.com/f?kw=%BA%DA%CB%BF&fr=ala0&tpl=5']
number =0
#设置一个请求体，一般都叫req
for root,dirname,filenames in os.walk(listPath):
       for filename in filenames:
            # os.path.splitext()是一个元组,类似于('188739', '.jpg')，索引1可以获得文件的扩展名
            if os.path.splitext(filename)[1]=='.jpg':
                number += 1

headers = {
    "User-Agnet": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
}
"""
11143
557150
<a href="//tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&amp;ie=utf-8&amp;pn=50" class="next pagination-item ">下一页&gt;</a>
<a href="//tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&amp;ie=utf-8&amp;pn=100" class="next pagination-item ">下一页&gt;</a>
<span class="pagination-current pagination-item ">8</span>
<a href="//tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&amp;ie=utf-8&amp;pn=400" class=" pagination-item ">9</a>
"""
def nextUrl(url):                    #得到下一个页面的路径 得到所有url
        req = urllib.request.Request(url, headers=headers)
        global number
        try:
            response = urllib.request.urlopen(req,timeout=5)
            data = response.read().decode("utf-8")
            re_next = re.compile(r'<a href="(.*?)" class="next pagination-item "')
            next_url = re_next.findall(data)  # 得到数据
            re_allUrl = re.compile(r'<a rel="noreferrer" href="/p/(.*?)"')
            print(next_url)
            url = r"https:"+next_url[0]
            crawerList.append(next_url[0])
            f = open(listPath, "wb")
            pickle.dump(crawerList, f)
            f.close()
            all_url = re_allUrl.findall(data)  # 得到数据
            for x in all_url:
                urls = r"https://tieba.baidu.com/p/" + x

                reqs = urllib.request.Request(urls, headers=headers)
                try:
                    responses = urllib.request.urlopen(reqs,timeout=5)
                    datas = responses.read().decode("utf-8")
                    re_picter = re.compile(r'class="BDE_Image" src="(.*?)"')
                    picter_list = re_picter.findall(datas)
                    print(picter_list)
                    for i in picter_list:
                        path = os.path.join(toPath, str(number) + ".jpg")
                        urllib.request.urlretrieve(i, filename=path)
                        number += 1
                except Exception as e:
                    print("出现异常-->" + str(e))
            nextUrl(url)
        except Exception as e:
            print("出现异常-->" + str(e))
            nextUrl(url)
url = r"https:"+crawerList[-1]
nextUrl(url)