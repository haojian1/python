from tkinter import *
import tkinter.messagebox
import requests
import re
from bs4 import BeautifulSoup as BS
import os
from wordcloud import WordCloud, ImageColorGenerator
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import jieba
import base64
from ppp import img
import sys

top = tkinter.Tk()
#标题
top.title("爬取b站视频弹幕")
#窗口放置屏幕中间
#得到屏幕的宽度和高度
sw = top.winfo_screenwidth()
sh = top.winfo_screenheight()
ww,wh=610,400
x=(sw-ww)/2
y=(sh-wh)/2
top.geometry("%dx%d+%d+%d" % (ww, wh-100, x, y))
#窗口颜色
top.configure(background='LightCyan')
#定义事件
def click():
    #视频信息
    av=entry1.get()
    url=f"https://www.bilibili.com/video/{av}/?spm_id_from=333.999.0.0&vd_source=ef2f2cc12f1c52e5b97fff68231213e0"
    header={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }

    r = requests.get(url=url,headers=header)
    r.encoding = "utf-8"
    pat = '"cid":(\d+)'
    cid = str(re.findall(pat, r.text)[1])
    url_base=f'http://comment.bilibili.com/{cid}.xml'
    r2 = requests.get(url=url_base,headers=header)
    r2.encoding='utf-8'
    soup = BS(r2.text, 'lxml')
    all_d = soup.find_all('d')
    #存到文件中
    with open('./result.txt','w',encoding="utf-8") as f:
        for d in all_d:
            f.write(d.get_text() + '\n')
    current_directory = os.getcwd()#os.path.dirname(os.path.realpath(sys.executable))
    tkinter.messagebox.showinfo("Message","文件保存目录为:"+current_directory+"\\result.txt")
#生成词云
def cloud():
    try:
        text = open("./result.txt",encoding="utf-8").readlines()
        text = [i.rstrip() for i in text]#去掉换行符
        str1 = ''
        for i in text:
            j = re.findall("([a-z\u4e00-\u9fa5]*)",i)
            for m in j:
                str1 = str1 + " " +m
        # words = jieba.lcut(str1)     #精确分词
        # newtxt = ' '.join(words)    #空格拼接
        # print(newtxt)
        # newtxt = newtxt.replace("doge","")
        newtxt = str1.replace("doge","")
        #生成对象
        tmp = open('one.png', 'wb')        #创建临时的文件
        tmp.write(base64.b64decode(img))    ##把这个one图片解码出来，写入文件中去。
        tmp.close()   
        mask = np.array(Image.open("one.png"))
        wordcloud = WordCloud(
                      font_path =  "./msyh.ttc",
                      mask = mask,
                      mode="RGBA",
                      background_color=None
                      ).generate(newtxt)
        # 从图片中生成颜色
        image_colors = ImageColorGenerator(mask)
        wordcloud.recolor(color_func=image_colors)
        #保存图片
        wordcloud.to_file('./词云图.png')
        current_directory = os.getcwd()#os.path.dirname(os.path.realpath(sys.executable))
        tkinter.messagebox.showinfo("Message","保存成功!\n词云保存目录为:"+current_directory+"\\词云图.png")
        os.remove('one.png')    #用完可以删除这个临时图片
    except Exception as e:
        tkinter.messagebox.showinfo("Message","请先爬取弹幕")

#划分模块
f1 = tkinter.Frame(top)
f2 = tkinter.Frame(top)
f3 = tkinter.Frame(top)
f4 = tkinter.Frame(top)

#f1模块放文本框
f1.pack()#蓝,bg='Aqua'
Label(f1, text="爬取视频的av号:",font=('宋体',20),fg='black',background='LightCyan',bd=5).pack(side=LEFT)
entry1 = Entry(f1,fg="black",bg="LightCyan",width=25,bd=4)
entry1.pack(side=RIGHT)

#f2模块放按钮
#定义按钮
f2.pack()
Button(f2,text="爬取",command=click,width=10,height=1,background="BurlyWood",font=("宋体",20)).pack(side=LEFT)
Button(f2,text="生成词云",width=10,height=1,command=cloud,background="BurlyWood",font=("宋体",20)).pack(side=LEFT)
# f3.pack()
# Button(f3,text="生成词云",command=cloud).pack()
#f3模块 注意
f4.pack()
Label(f4,text="说明",anchor="center",font=("宋体",20),background="LightCyan",width=50).pack()
Label(f4,text="例如https://www.bilibili.com/video/BV1T44y1R7sj/?spm_id_from=333.1007.tianma.1-3-3.click&vd_source=ef2f2cc12f1c52e5b97fff68231213e0,BV1T44y1R7sj即为av号",anchor="w",font=("宋体",15),bg="LightCyan",width=100,height=3,wraplength=600,justify="left").pack()

#主事件循环
top.mainloop()
