import urllib.request



#向指定的url地址发起请求，并返回服务器的相应数据（文件的对象）
response = urllib.request.urlopen("https://tieba.baidu.com/f?kw=%E9%BB%91%E4%B8%9D&ie=utf-8&pn=350")


# 读取文件的全度内容，会把读取的数据复制给一个字符串变量
data = response.read().decode("utf-8")
print(data)
print(type(data))

#读取一行，循环读取
#data = response.readline()
#list类型的。
# data = response.readlines().decode("utf-8")
# print(data)
# print(type(data))

with open("baidu.html","w",encoding='utf-8') as f:
    f.write(data)

print(response.geturl())  #返回正在爬取的url地址


# 网址里有汉字的 也就是解码
url = ""
newUrl = urllib.request.unquote(url)
print(newUrl)

#编码
newUrl2 = urllib.request.quote(newUrl)
print(newUrl2)
#我们在编码的时候

