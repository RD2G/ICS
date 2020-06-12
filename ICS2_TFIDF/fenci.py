'''
TF也就是我们前面说到的词频，我们之前做的向量化也就是做了文本中各个词的出现频率统计，并作为文本特征，这个很好理解。关键是后面的这个IDF，即“逆文本频率”如何理解。在上一节中，我们讲到几乎所有文本都会出现的"to"其词频虽然高，但是重要性却应该比词频低的"China"和“Travel”要低。我们的IDF就是来帮助我们来反应这个词的重要性的，进而修正仅仅用词频表示的词特征值。
概括来讲， IDF反应了一个词在所有文本中出现的频率，如果一个词在很多的文本中出现，那么它的IDF值应该低，比如上文中的“to”。而反过来如果一个词在比较少的文本中出现，那么它的IDF值应该高。比如一些专业的名词如“Machine Learning”。这样的词IDF值应该高。一个极端的情况，如果一个词在所有的文本中都出现，那么它的IDF值应该为0。
'''

import jieba
from zhon.hanzi import punctuation
import jieba.analyse
import re

#分词函数
def Cut():
    #官方示例
    '''
    seg_list = jieba.cut("我来到北京清华大学", cut_all=True)
    print("Full Mode: " + "/ ".join(seg_list))  # 全模式
    seg_list = jieba.cut("我来到北京清华大学", cut_all=False)
    print("Default Mode: " + "/ ".join(seg_list))  # 精确模式
    seg_list = jieba.cut("他来到了网易杭研大厦")  # 默认是精确模式
    print(", ".join(seg_list))
    seg_list = jieba.cut_for_search("小明硕士毕业于中国科学院计算所，后在日本京都大学深造")  # 搜索引擎模式
    print(", ".join(seg_list))
    '''
    # 对文本进行分词预处理
    with open('./1_b.txt', encoding='GBK') as f:
        doc = f.read()
        # print(doc)
        doc_cuts = jieba.cut(doc)
        '''
        for doc_cut in doc_cuts:
            doc_cut = doc_cut.encode('utf-8')
            #print(doc_cut)
            if doc_cut in list:
                print(doc_cut)
        #print(doc_cut)
        #print(''.join(doc_cut))
        #print(doc_lst)
        '''
        return doc_cuts
#读取&输出文本
def File():
    # 去除暂停词表
    with open('./stop_words.txt', 'r') as f:
        stpwrd_content = f.read()
        # 将停用词表转换为list
        stpwrdlst = stpwrd_content.splitlines()
        #print(stpwrdlst)
    #首先去除原文本中的空行和标点
    f1 = open('./1.txt', 'r', encoding='GBK')  # 要去掉空行的文件
    f2 = open('./1_b.txt', 'w', encoding='GBK')  # 生成没有空行的文件
    for line in f1.readlines():
        if line == '\n':
            #print(line)
            #line = re.sub(r'[^\w\s]', '', line)
            #print(line)
            line = line.strip("\n")
        line = line.encode('utf-8')
        line = re.sub(r"[%s]+" % punctuation, "", line.decode("utf-8"))
        #print(line)
        f2.write(line)
    f1.close()
    f2.close()
    # 对文本进行分词
    t = Cut()
    a = '/'.join(t)
    '''
    for i in result.split('/'):
        if i in stpwrdlst:
            i = '@'
        #print(i)
    #print(result)
    '''
    #去除停用词
    result = ''
    for i in a.split('/'):
        if i in stpwrdlst:
            pass
        else:
            result += i+'/'
    #TF-IDF
    aa = ''
    for ii in result.split('/'):
        aa += ii
    keywords = jieba.analyse.extract_tags(aa, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    #for item in keywords:
     #   print(item[0], item[1])
    #对文本进行储存
    with open('./1result.txt',mode='w',encoding='GBK') as ff:
        ff.write(result)
    with open('./1tfidf.txt',mode='w',encoding='utf-8') as ft:
        for item in keywords:
            ft.write((item[0] + ' ' + str(item[1]) + '\n'))



if __name__ == '__main__':
    #Cut()
    File()