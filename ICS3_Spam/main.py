from scipy.constants import precision
import time
import math
import sys
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
from numpy import *
from im import improt_data_with_bool, improt_data_with_num
from sklearn import svm
from sklearn.model_selection import GridSearchCV
#import Pretreatment
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import MultinomialNB



# def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
#     p1=sum(vec2Classify*p1Vec)+log(pClass1)
#     p0=sum(vec2Classify*p0Vec)+log(1-pClass1)
#     if p1>p0:
#         return 1
#     else:
#         return 0
#
#

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
    p1 = sum(vec2Classify * p1Vec) + log(pClass1)    #element-wise mult
    p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else:
        return 0

def trainNB0(trainMatrix,trainCategory):#文档矩阵和文档类型标签
    numtTrainDocs=len(trainMatrix)#一共有几个档
    #print(numtTrainDocs)
    numWordS=len(trainMatrix[0])#这个文档有几个词
    #print(numWordS)
    pAbusive=sum(trainCategory)/float(numtTrainDocs)#垃圾邮箱总占比
    #print(pAbusive)
    p0Num=ones(numWordS)#返回一个用1填充的数组
    p1Num=ones(numWordS)
    p0Denom=2.0
    p1Denom=2.0
    for i in range(numtTrainDocs):
        if trainCategory[i]==1:
            p1Num+=trainMatrix[i]
            p1Denom+=sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect=log(p1Num/p1Denom)
    p0Vect =log(p0Num / p0Denom)
    return p0Vect,p1Vect,pAbusive

# def testingNB(X_train, X_test, y_train, y_test):
    #贝努利模型的测试集和训练集的划分
    #trainMatrix,trainCatrgory=Pretreatment.Bernoulli_model()
    #X是文章，y是文章所属类别
    # 改变random_state的值会改变测试集的选取，取0是每次都随机选取测试集
    #朴素贝叶斯训练函数
    # results=[]
    # for xxx in X_test:
    #     p0Vect, p1Vect, pAbusive = trainNB0(X_train, y_train)
    #     results.append(classifyNB(xxx, p0Vect, p1Vect, pAbusive))
    #precision recall f1-score三列分别为各个类别的精确度/召回率及F1值
    # target_names = ['class 0', 'class 1']
    # print(classification_report(y_test, results, target_names=target_names))

# def testingNB1(X_train, X_test, y_train, y_test):
    #多项式模型的测试集和训练集的划分
    #trainMatrix,trainCatrgory=Pretreatment.Polynomial_model()
    #X是文章，y是文章所属类别
    #改变random_state的值会改变测试集的选取，取0是每次都随机选取测试集
    #朴素贝叶斯训练函数
    # results=[]
    # for xxx in X_test:
    #     p0Vect, p1Vect, pAbusive = trainNB0(X_train, y_train)
    #     results.append(classifyNB(xxx, p0Vect, p1Vect, pAbusive))
    # precision recall f1-score三列分别为各个类别的精确度/召回率及F1值
    # target_names = ['class 0', 'class 1']
    # print(classification_report(y_test, results, target_names=target_names))
def train_byes(x_train,y_train):
    '''
    :param x_train:
    :param y_train:
    :return:
        P_c1    垃圾邮件的概率
        p_w     p(w0)*p(w1)*p(w2*)...*p(wn)
        p_w_c1: p(w0|c1)*p(w1|c1)*p(w2|c1)...*p(wn|c1)
    '''
    train_sum = len(y_train)
    num_word = len(x_train[0])
    p_c1 = sum(y_train)/float(train_sum)#垃圾邮件的概率
    pw_times=np.ones(num_word)
    pwc1_times=np.ones(num_word)

def train_bayes(trainMatrix, trainCategory):
    numTrainDocs = len(trainMatrix)
    numWords = len(trainMatrix[0])
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    p0Num = ones(numWords); p1Num = ones(numWords)
    p0Denom = 2.0; p1Denom = 2.0
    for i in range(numTrainDocs):
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom += sum(trainMatrix[i])
        else:
            p0Num += trainMatrix[i]
            p0Denom += sum(trainMatrix[i])
    p1Vect = log(p1Num/p1Denom)          #change to log()
    p0Vect = log(p0Num/p0Denom)          #change to log()
    return p0Vect,p1Vect,pAbusive



def main_bayes(x_train, x_test, y_train, y_test):
    # 0代表正常 1代表垃圾
    p0V, p1V, pClass1 = train_bayes(array(x_train), array(y_train))
    y_predict=[]
    for test in x_test:
        y_predict.append(classifyNB(test, p0V, p1V, pClass1))
    print(classification_report(y_test, y_predict))

def knn(x_train,x_test,y_train,y_test):
    param_grid = [
        {
            'weights': ['uniform'],
            'n_neighbors':[i for i in range(1,11)]
        },
        {
            'weights':['distance'],
            'n_neighbors':[i for i in range(1,11)],
            'p':[i for i in range(1,6)]
        }
    ]

    knn_clf=KNeighborsClassifier()
    grid_search=GridSearchCV(knn_clf,param_grid) #这个相当于代替之前的两个for循环
    grid_search.fit(x_train,y_train)  #传入相应的参数进行拟合
    knn_clf = grid_search.best_estimator_
    y_pre = knn_clf.predict(x_test)
    print(classification_report(y_test,y_pre))

#
# def main_svm(x_train, x_test, y_train, y_test):
#     parameters = [{'C': [1, 5, 10, 50, 100, 250, 500]}]
#     grid = GridSearchCV(svm.SVC(kernel='linear'), parameters, cv=10)
#     grid.fit(x_train, y_train)
#     y_predict = grid.predict(x_test)
#     print(classification_report(y_test, y_predict))




if __name__ == '__main__':
    all,label=improt_data_with_bool()
    x_train, x_test, y_train, y_test = train_test_split(all, label, test_size=0.2)
    print("朴素贝叶斯的精确度，召回率：")
    main_bayes(x_train, x_test, y_train, y_test)

    print("knn模型的精确度，召回率：")
    knn(x_train, x_test, y_train, y_test)

    # print("贝努力模型的精确度，召回率：")
    # testingNB(x_train, x_test, y_train, y_test)
    #
    # print("多项式模型的精确度，召回率：")
    # testingNB1(x_train, x_test, y_train, y_test)
    #
    # print("SVM分类器的精确度，召回率：")
    # main_svm(x_train, x_test, y_train, y_test)