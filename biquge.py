import requests
from bs4 import BeautifulSoup
import time
import random

site = 'www.xbiquge.la'
headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36'}
ad = '亲,点击进去,给个好评呗,分数越高更新越快,据说给新笔趣阁打满分的最后都找到了漂亮的老婆哦!手机站全新改版升级地址：https://wap.xbiquge.la，数据和书签与电脑站同步，无广告清新阅读！'
def searchBook(bookName):
    searchurl = 'https://' + site + '/modules/article/waps.php'
    payload = {"searchkey": bookName}
    r = requests.post(searchurl,headers=headers,data=payload)
    r.encoding = 'utf-8'
    return r
def getBookPage(url): #所有get访问都从这个函数走
    r = requests.get(url,headers=headers)
    r.encoding = 'utf-8'
    return r
def get_text(href):
    r = getBookPage(href)
    soup = BeautifulSoup(r.content, 'lxml')
    artist = soup.find('div', id='content')
    return artist.text
def checkBook(html):
    ##checkform > table > tbody > tr:nth-child(2) > td:nth-child(1)
    soup = BeautifulSoup(html,'lxml')
    list_name = soup.select('.even > a')
    itemlen = len(list_name)
    if itemlen != 0:
        for n,i in enumerate(list_name):
            if i['href'] != None:
                print(n,i.text,i['href'])
        x = eval(input('输入要下载的书籍序号(输入8888重新开始搜索)：'))
        print(type(x),x)
        while int(x) >n or int(x) < 0-n or int(x) ==8888 :
            if int(x) == 8888:
                return -2
            x = int(input('输入有误，请输入要下载的书籍序号：'))
        if x != None:
            print('您选择的是：',list_name[x].text)
            f = open(list_name[x].text+'.txt', 'w', encoding='utf8')
            ret = getBookPage(list_name[x]['href'])#取回章节列表
            downloadBook(ret.content,f)#分析并下载所有页面
            f.close()
        else:print('输入错误，请重新运行程序！')
    else:return -1
def downloadBook(html,f):
    soup = BeautifulSoup(html, 'lxml')
    list_name = soup.select('.box_con > #list > dl > dd > a')
    itemlen = len(list_name)
    for n,i in enumerate(list_name):
        checknum = -1
        if n > checknum:
            link = 'https://'+ site + i['href']
            title = i.text
            print('%s 正在下载:[%d/%d]【%s】' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                n,
                itemlen,
                title))
            # 获取章节内容函数
            text = get_text(link).strip(ad) #利用strip清理首位广告
            # 写入文件
            res = f.write('【' + title + '】\n' + text + '\n')
            if res < 1:
                print('[%d]写入失败！')
                break
            print('%s 结束下载:[%d/%d]【%s】[写入字节数]%d' % (
                time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
                n,
                itemlen,
                title,
                res))
            time.sleep(random.uniform(0, 1))
def happy():
    bookname = input('请输入你要下载的书名:')
    ret = searchBook(bookName=bookname)
    res = checkBook(ret.content)
    if  res <= -1 :
        if res == -1:
            print('http://www.xbiquge.la/ 站内搜不到相关书籍！')
        if res == -2:
            print('请重新输入要搜索的书籍名，关键字请遵循 宁缺毋错 的原则')
        happy()
if __name__ == '__main__':
    happy()