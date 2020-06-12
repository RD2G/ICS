'''
对文本进行针对性分词，统计人物在本文中的出场次数。
以段落为单位进行划分，统计每段中的人物，两两配对后计数，形成粗略的人物关系统计。
用gephi来绘制图的节点和边数据
'''
import os
import sys
import csv
import jieba
import codecs
from jieba import posseg as pseg

#对剧本进行分词处理，统计人物在本文中的出场次数
def CutAndCount():
    jieba.load_userdict(ppath)  # 加载人物表
    with codecs.open(tpath, mode='r',encoding='utf-8',errors='ignore') as f:
        for line in f.readlines():
            poss = pseg.cut(line)  # 分词，返回词性
            lineNames.append([])  # 为本段增加一个人物列表
            for w in poss:
                if w.word in stopwords:  # 去掉某些停用词
                    continue
                if w.flag != 'nr' or len(w.word) < 2:
                    if w.word not in replace_words:
                        continue  # 当分词长度小于2或该词词性不为nr（人名）时认为该词不为人名
                if w.word in replace_words:  # 将某些在文中人物的昵称替换成正式的名字
                    w.word = replace_words[w.word]
                if names.get(w.word) is None:  # 如果某人物（w.word）不在人物字典中
                    names[w.word] = 0
                    relationships[w.word] = {}
                names[w.word] += 1
                lineNames[-1].append(w.word)  # 为当前段增加一个人物

                # 输出人物出现次数统计结果
    # for name, times in names.items():
    #    print(name, times)



#以段落为单位进行划分，统计每段中的人物，两两配对后计数，形成粗略的人物关系统计
def CalRelationship():
    # 对于 lineNames 中每一行，我们为该行中出现的所有人物两两相连。如果两个人物之间尚未有边建立，则将新建的边权值设为 1，
    # 否则将已存在的边的权值加 1。这种方法将产生很多的冗余边，这些冗余边将在最后处理。
    for line in lineNames:
        for name1 in line:
            for name2 in line:
                if name1 == name2:
                    continue
                if relationships[name1].get(name2) is None:
                    relationships[name1][name2] = 1
                else:
                    relationships[name1][name2] = relationships[name1][name2] + 1   #如果两个人已经出现过，则亲密度加1

                    # 由于分词的不准确会出现很多不是人名的“人名”，从而导致出现很多冗余边，
                    # 为此可设置阈值为10，即当边出现10次以上则认为不是冗余

    with codecs.open("People_node.csv", "w", "utf8") as f:
        f.write("ID Label Weight\r\n")
        for name, times in names.items():
            if times > 10:
                f.write(name + " " + name + " " + str(times) + "\r\n")

    with codecs.open("People_edge.csv", "w", "utf8") as f:
        f.write("Source Target Weight\r\n")
        for name, edges in relationships.items():
            for v, w in edges.items():
                if w > 10:
                    f.write(name + " " + v + " " + str(w) + "\r\n")



if __name__ == '__main__':
    tpath = './rmdmy.txt'    #文本路径
    ppath = './zyrw.txt'    #人物词典路径
    names = {}  # 保存人物，键为人物名称，值为该人物在全文中出现的次数
    relationships = {}  # 保存人物关系的有向边，键为有向边的起点，值为一个字典 edge ，edge 的键为有向边的终点，值是有向边的权值
    lineNames = []  # 缓存变量，保存对每一段分词得到当前段中出现的人物名称
    stopwords = ['吕州', '林城', '银行卡', '明白', '白云', '嗡嗡嘤嘤','阴云密布', '雷声', '陈大', '谢谢您', '安置费', '任重道远',
                 '孤鹰岭', '阿庆嫂', '岳飞', '师生', '养老院', '段子', '老总', '大力支持', '司法公正', '扬言', '维持秩序','陈述',
                 '言辞', '许诺', '安抚', '寒暄', '殷勤', '冷笑']
    replace_words = {'师母': '吴慧芬', '陈老': '陈岩石', '老赵': '赵德汉', '达康': '李达康', '高总': '高小琴',
                     '猴子': '侯亮平', '老郑': '郑西坡', '小艾': '钟小艾', '老师': '高育良', '同伟': '祁同伟',
                     '赵公子': '赵瑞龙', '郑乾': '郑胜利', '孙书记': '孙连城', '赵总': '赵瑞龙', '昌明': '季昌明',
                     '沙书记': '沙瑞金', '郑董': '郑胜利', '宝宝': '张宝宝', '小高': '高小凤', '老高': '高育良',
                     '伯仲': '杜伯仲', '老杜': '杜伯仲', '老肖': '肖钢玉', '刘总': '刘新建', "美女老总": "高小琴"}
    CutAndCount()
    CalRelationship()