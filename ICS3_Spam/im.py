import os
import os.path
#import shutil
#import jieba
import string


# 获取邮件列表
def get_mail():
    mailst = []
    label = []
    hamPath = './email/ham/'
    hamLists = os.listdir(hamPath)  # 列出文件夹下所有的目录与文件
    spamPath = './email/spam/'
    spamLists = os.listdir(spamPath)  # 列出文件夹下所有的目录与文件
    for txt in hamLists:
        try:
            f = open(hamPath + txt, 'r', encoding='utf-8')  # 返回一个文件对象
            mail = f.read()  # 读取全部内容
            for c in string.punctuation:
                mail = mail.replace(c, '')
            mailst.append(mail)
            label.append(0)
        except:
            continue
    for txt in spamLists:
        try:
            f = open(spamLists + txt, 'r', encoding='utf-8')  # 返回一个文件对象
            mail = f.read()  # 读取全部内容
            for c in string.punctuation:
                 mail = mail.replace(c, '')
            mailst.append(mail)
            label.append(1)
        except:
            continue
    return mailst,label

# 制作停止词表
def stopword():
    stpwrd = []
    f = open('stop_words.txt', 'r')
    for wrd in f:
        wrd = wrd.strip()
        stpwrd.append(wrd)
    return stpwrd

# 获取词袋
def get_bag(mail_list):
    wrd_bag = []
    for mails in mail_list:
        wrd_list = mails.split()
        for wrd in wrd_list:
            if len(wrd)>1:
                if wrd not in wrd_bag:
                    if wrd not in stopword():
                        wrd_bag.append(wrd)
    return wrd_bag

# 获取所有bool向量
def get_bool(mail_list,word_bag,label):
    word_bool = []
    for mail in mail_list:
        mail_bool = []
        word_list = mail.split()
        for i in word_bag:
            if i in word_list:
                mail_bool.append(1)
            else:
                mail_bool.append(0)
        word_bool.append(mail_bool)
    return word_bool,label


# 获取所有数量向量
def get_num(mail_list,word_bag,label):
    word_num = []
    for mail in mail_list:
        mail_num = []
        word_list = mail.split()
        for i in word_bag:
            if i in word_list:
                mail_num.append(word_list.count(i))
            else:
                mail_num.append(0)
        word_num.append(mail_num)
    return word_num,label


def improt_data_with_bool():
    mail_list, label = get_mail()
    word_bag = get_bag(mail_list)
    return get_bool(mail_list, word_bag, label)

def improt_data_with_num():
    mail_list, label = get_mail()
    word_bag = get_bag(mail_list)
    return get_num(mail_list, word_bag, label)


#
# if __name__ == '__main__':
#     mail_list,label = get_mail()
#     word_bag = get_bag(mail_list)
#     print(get_num(mail_list,word_bag,label))
#     print(get_bool(mail_list,word_bag,label))

