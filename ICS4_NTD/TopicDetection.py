#话题检测系统主要分为数据获取、预处理、分词和词频统计、主题词检测，以及话题聚类这５个步骤
import pynlpir
import jieba
import jieba.analyse
import pandas
import codecs
from scipy.cluster.hierarchy import ward, dendrogram, linkage
import matplotlib.pyplot as plt
from sklearn import feature_extraction
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import CountVectorizer
from im import *
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import TfidfVectorizer

'''
#ICTCLAS分词系统，从2009年开始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共享平台，调整命名为NLPIR分词系统。
def ICTCLAS():
    pynlpir.open(encoding='utf-8')
    # txt = Filter()
    txt = 'NLPIR分词系统前身为2000年发布的ICTCLAS词法分析系统，从2009年开始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共享平台，调整命名为NLPIR分词系统。'
    rslt = pynlpir.segment(txt) #LicenseError: Your license appears to have expired.居然换换不了license。。unable to fetch newest license
    key_wrd = pynlpir.get_key_words(txt, weighted = True)
    print(rslt)
    print(key_wrd)
    pynlpir.close()
'''

#jieba分词
def Jieba_Cut():
    txt = Filter()
    # txt = 'NLPIR分词系统前身为2000年发布的ICTCLAS词法分析系统，从2009年开始，为了和以前工作进行大的区隔，并推广NLPIR自然语言处理与信息检索共享平台，调整命名为NLPIR分词系统。'

    cuts = jieba.cut(txt)
    rslt = []
    sw = StpWrd()
    for cut in cuts:    #停止词
        if cut in sw:
            continue
        else:
            rslt.append(cut)
    t = ' '.join(rslt)
    # print(t)
    '''
    # TF-IDF
    a = ''
    for i in t.split(' '):
        a += i
    keywords = jieba.analyse.extract_tags(a, topK=20, withWeight=True, allowPOS=('n', 'nr', 'ns'))
    with open('./fenci_result.txt', mode = 'w', encoding='utf-8') as f1:
        f1.write(t)
    with open('./tfidf_result.txt',mode='w',encoding='utf-8') as f2:
        for item in keywords:
            f2.write((item[0] + ' ' + str(item[1]) + '\n'))
    '''


#主题词检测聚类
def Det():
    files = []
    titles = []
    with open('./fenci_result.txt','r') as f:
        for line in f.readlines():
            # print(line)
            line = re.sub('\d\d\d+.*标题( +)','',line)
            title = re.match(' *[\u4e00-\u9fa5]+',line).group()
            title = re.sub(' *','',title)
            print(title)
            # print(line)
            titles.append(title)
            files.append(line.strip())
        # print(lst)
        #tfidf
        '''
        # 将文本中的词语转换为词频矩阵 矩阵元素a[i][j] 表示j词在i类文本下的词频
        vectorizer = CountVectorizer()

        # 该类会统计每个词语的tf-idf权值
        transformer = TfidfTransformer()

        # 第一个fit_transform是计算tf-idf 第二个fit_transform是将文本转为词频矩阵
        tfidf = transformer.fit_transform(vectorizer.fit_transform(files))

        # 获取词袋模型中的所有词语
        word = vectorizer.get_feature_names()

        # 将tf-idf矩阵抽取出来，元素w[i][j]表示j词在i类文本中的tf-idf权重
        weight = tfidf.toarray()
        with open('./tfidf_result.txt',mode='w',encoding='utf-8') as r:
            for j in range(len(word)):
                r.write(word[j] + ' ')
            r.write('\r\n\r\n')
            # 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
            for i in range(len(weight)):
                u"-------这里输出第", i, u"类文本的词语tf-idf权重------"
                for j in range(len(word)):
                    r.write(str(weight[i][j]) + ' ')
                r.write('\r\n\r\n')
        '''
        #聚类Kmeans
        # max_df: When building the vocabulary ignore terms that have a document frequency strictly higher than the given threshold (corpus-specific stop words). If float, the parameter represents a proportion of documents, integer absolute counts. This parameter is ignored if vocabulary is not None.
        # min_df: When building the vocabulary ignore terms that have a document frequency strictly lower than the given threshold. This value is also called cut-off in the literature. If float, the parameter represents a proportion of documents, integer absolute counts. This parameter is ignored if vocabulary is not None.
        tfidf_vectorizer = TfidfVectorizer(max_df=0.9, max_features=200000,
                                           min_df=0.1, stop_words='english',
                                           use_idf=True, tokenizer=Jieba_Cut())
        # terms is just a 集合 of the features used in the tf-idf matrix. This is a vocabulary
        # terms = tfidf_vectorizer.get_feature_names()

        #获得Tf-idf矩阵
        tfidf_matrix = tfidf_vectorizer.fit_transform(files)  # fit the vectorizer to synopses
        print(tfidf_matrix.shape)
        dist = 1 - cosine_similarity(tfidf_matrix)#(33, 283)

        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 用来正常显示中文标签
        # Perform Ward's linkage on a condensed distance matrix.
        # linkage_matrix = ward(dist) #define the linkage_matrix using ward clustering pre-computed distances
        # Method 'ward' requires the distance metric to be Euclidean
        linkage_matrix = linkage(dist, method='ward', metric='euclidean', optimal_ordering=False)
        # Z[i] will tell us which clusters were merged, let's take a look at the first two points that were merged
        # We can see that ach row of the resulting array has the format [idx1, idx2, dist, sample_count]
        print(linkage_matrix)
        for index, title in enumerate(titles):
            print(index, title)
        





if __name__ == '__main__':
    # ICTCLAS()
    Jieba_Cut()
    Det()
    print(
        'hello world'
    )