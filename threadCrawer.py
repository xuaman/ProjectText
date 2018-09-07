import urllib.response
import  urllib.request
import re
import os
import pickle
import threading
import queue

def mkdir(path):
    folder = os.path.exists(path)
    if not folder:  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)  # makedirs 创建文件时如果路径不存在会创建这个路径



headers = {
    "User-Agnet": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
 }   #头结点的伪装


def nextURL(url,crawerque):

    while True:
        req = urllib.request.Request(url, headers=headers)
        try:
            response = urllib.request.urlopen(req, timeout=5)
            data = response.read().decode("utf-8")
            re_next = re.compile(r'<a href="(.*?)" class="next pagination-item "')
            next_url = re_next.findall(data)  # 这个得到的下一个的
            print(next_url)
            re_allUrl = re.compile(r'<a rel="noreferrer" href="/p/(.*?)"')
            all_url = re_allUrl.findall(data)
            for pageUrl in all_url:
                crawerque.put(pageUrl)
            print("***************************")
            print(type(next_url))
            print(next_url)
            url = r'https:'+next_url[0]
        except Exception as e:
            print("出现异常11111-->" + str(e))


def allURL(crawerque,pictureque):
    while True:
        item = crawerque.get()
        print(item+"qqqqqqqqqqqqqqq")
        if item is None:
            break
        try:
            urls = r"https://tieba.baidu.com/p/" + item
            reqs = urllib.request.Request(urls, headers=headers)
            try:
                responses = urllib.request.urlopen(reqs, timeout=5)
                datas = responses.read().decode("utf-8")
                re_picter = re.compile(r'class="BDE_Image" src="(.*?)"')
                picter_list = re_picter.findall(datas)
                pictureque.put(picter_list)
            except Exception as e:
                    print("出现异常222222-->" + str(e))
        except:
            pass

def save_picture(x,toPath,num):
    path = os.path.join(toPath, str(num) + ".jpg")
    urllib.request.urlretrieve(x, filename=path)

def down_picture(pictureque):
    num=1
    while True:
        item = pictureque.get()
        if item is None:
            break
        for x in item:
            threading.Thread(target=save_picture ,args=(x,toPath,num)).start()
            num += 1





if __name__ == "__main__":
    toPath = r"D:\picture"
    mkdir(toPath)
    crawerque = queue.Queue(10)#这个是爬取的一个页面里的所有网页的
    pictureque = queue.Queue(100)#这个放的是每个图片
    url = r'https://tieba.baidu.com/f?kw=%BA%DA%CB%BF&fr=ala0&tpl=5'  # 爬取的首页
    ###三个线程一个线程是访问下一个主界面,一个是访问每个里面的每个网页,还有一个是存具体网页里的图片的
    th1 = threading.Thread(target=nextURL,args=(url,crawerque,))#这个线程一直是在得到数据 把爬的这个页面里内容队列中
    th2 = threading.Thread(target=allURL,args=(crawerque,pictureque,))
    th3 = threading.Thread(target=down_picture, args=(pictureque,))
    th1.start()
    th2.start()
    th3.start()
    th1.join()
    th2.join()
    th3.join()
