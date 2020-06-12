import os
import time
import string
import sys
import numpy
import re


#暂停词
def StpWrd():
    with open('./stop_words.txt', 'r') as f:
        stpwrd_content = f.read()
        # 将停用词表转换为list
        stpwrdlst = stpwrd_content.splitlines()
        # print(stpwrdlst)
        return stpwrdlst
'''
#读取微博文章文件
def ReadFile(flag):
    if int(flag)==1:
        # 读取文件夹中全部的训练集
        Cpath = './话题检测数据集/'
        fthlst = os.listdir(Cpath)  # 列出文件夹下所有的目录与文件
        # print(fthlst)
        # a = 0
        weibo_content = ''  #python本身对string长度无强制性限制。使用过程中主要需要考虑电脑性能和程序效率
        for p in fthlst:
            pthlst = os.listdir(Cpath + p)
            for txt in pthlst:
                try:
                    with open(Cpath + p + '/' + txt, 'r', encoding='gbk', errors='ignore') as f:
                        # 首先去除原文本中的空行
                        weibo_coontent = f.read()  # 编解码问题在这几次实验中一直存在，我实在有点不知道到底为什么不能用utf-8
                        # print("hhhhhh")
                        # a += 1
                        # print(a)
                        # print(weibo_coontent)
                        weibo_content += weibo_coontent
                except Exception:
                    with open(Cpath + p + '/' + txt, 'r', encoding='utf-8', errors='ignore') as f:
                        weibo_coontent = f.read()  # 编解码问题在这几次实验中一直存在，我实在有点不知道到底为什么不能用utf-8
                        weibo_content += weibo_coontent
                        # print("aaaa")
                        # a += 1
                        # print(a)
                        # print(weibo_coontent)
                        # return weibo_coontent
                    # print('读取失败！')
        # print(weibo_content)
        return weibo_content

    else:
        # 读取单个文件
        Fpath = flag
        try:
            with open(Fpath, 'r', encoding='gbk', errors='ignore') as f:
                weibo_cont = f.read()
                return weibo_cont
        except Exception:
            with open(Fpath, 'r', encoding='utf-8', errors='ignore') as f:
                weibo_cont = f.read()
                return weibo_cont
#train
def ReadTrain():
    Fpath = './train/C4-Literature/'
    fpath = os.listdir(Fpath)
    # print(fpath)
    con = ''
    for txt in fpath:
        try:
            with open(Fpath + txt, 'r', encoding='gbk', errors='ignore') as f:
                con += f.read()
        except Exception:
            with open(Fpath + txt, 'r', encoding='utf-8', errors='ignore') as f:
                con += f.read()
    # print(con)
    return con

#test
def ReadTest():
    Fpath = './test/C4-Literature/'
    fpath = os.listdir(Fpath)
    con = ''
    for txt in fpath:
        try:
            with open(Fpath + txt, 'r', encoding='gbk', errors='ignore') as f:
                con += f.read()
        except Exception:
            with open(Fpath + txt, 'r', encoding='utf-8', errors='ignore') as f:
                con += f.read()
    # print(con)
    return con
'''
#空格空行
def kk(rel):
    strinfo = re.compile(' ')
    rel = strinfo.sub('', rel)
    rel = re.sub('\n', '', rel)
    return rel

#read file
def Read():
    Fpath = './train/C4-Literature/'
    fpath = os.listdir(Fpath)
    con = ''
    for txt in fpath:
        try:
            with open(Fpath + txt, 'r', encoding='gbk', errors='ignore') as f:
                con += kk(f.read()) + '\n'
        except Exception:
            with open(Fpath + txt, 'r', encoding='utf-8', errors='ignore') as f:
                con += kk(f.read()) + '\n'
    # print(con)
    return con

#过滤
def Filter():
    #忽略收听人数小于阈值Ｆ 的用户的消息 x
    #忽略带有“＠用户”格式的消息 x
    #删除消息中以“＃话题名＃”为格式的部分
    # print("请输入：\n1-->读取整个文件 or 直接输入文件路径")
    # flag = input()
    # con = ReadFile(flag)
    con = Read()
    rel = re.sub('#[^#]*?#', '', con)
    '''
    #去除空格空行
    strinfo = re.compile(' ')
    rel = strinfo.sub('', rel)
    rel = re.sub('\n', '', rel)
    '''
    # test = 'aa#aaaa#bb#aaaa#cc##a###dd'
    # rel = re.sub('#[^#]*?#', '', test)
    # print(rel)
    return rel



if __name__ == '__main__':
    Read()
    # ReadTrain()
