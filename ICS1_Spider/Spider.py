
import requests
import os
from bs4 import BeautifulSoup as bs


#欢迎
def Hello():
    print('Hello')

#获取网页原代码
def GetHtml(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
    except requests.RequestException:
        return None
'''
#解析，这里采用beautifulsoup
def GetResult():
    html = GetHtml(url)
    soup = bs(html, 'html.parser')
    all_img = soup.find('ul',class_='pli').find_all('img')
    return all_img
   # bb = bs(html)
'''
#将结果写入与Spider.py同级文件夹中的Result.txt
def SaveResult():
    html = GetHtml(url)
    soup = bs(html, 'html.parser')
    all_img = soup.find('ul', class_='pli').find_all('img')
    root = '/home/wzx/Desktop/ICS1_Spider/'
    for img in all_img:
        src = img['src']
        img_url = src
        print(img_url)
        path = root + img_url.split('/')[-1]
        try:
            if not os.path.exists(root):
                os.mkdir(root)
            if not os.path.exists(path):
                r = requests.get(img_url)
                with open(path, 'wb') as f:
                    f.write(r.content)
                    f.close()
                    print("文件保存成功")
            else:
                print("文件已存在")
        except:
            print("爬取失败")
        '''
        print(path)
        with open(path,'wb') as f:
            r = requests.get('http:'+img_url)
            f.write(r.content)
            f.close()
            print("文件保存成功")
        '''
#主函数
def main():
    Hello()
    SaveResult()


if __name__ == '__main__':
    url = 'https://www.ivsky.com/bizhi/yourname_v39947/'
    main()